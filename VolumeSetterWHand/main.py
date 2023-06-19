import cv2
import mediapipe as mp
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

cap = cv2.VideoCapture(0)  # Check for camera

mpHands = mp.solutions.hands  # Detect hand/finger
hands = mpHands.Hands()  # Complete the initialization configuration of hands
mpDraw = mp.solutions.drawing_utils

# Access the speaker through the pycaw library
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volbar = 400
volper = 0

volMin, volMax = volume.GetVolumeRange()[:2]


while True:
    success, img = cap.read()  # If the camera works, capture an image
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB

    # Collection of gesture information
    results = hands.process(imgRGB)  # Complete the image processing.

    lmList = []  # Empty list
    if results.multi_hand_landmarks:  # List of all hands detected.
        # By accessing the list, we can get the information of each hand's corresponding flag bit
        for hand_landmark in results.multi_hand_landmarks:
            for id, lm in enumerate(hand_landmark.landmark):  # Adding counter and returning it
                # Get finger joint points
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])  # Adding to the empty list 'lmList'
            mpDraw.draw_landmarks(img, hand_landmark, mpHands.HAND_CONNECTIONS)

    if lmList:
        # Getting the value at a point
        x1, y1 = lmList[4][1], lmList[4][2]  # Thumb
        x2, y2 = lmList[8][1], lmList[8][2]  # Index finger
        # Creating circles at the tips of the thumb and index finger
        cv2.circle(img, (x1, y1), 13, (255, 0, 0), cv2.FILLED)  # Image, position, radius, RGB
        cv2.circle(img, (x2, y2), 13, (255, 0, 0), cv2.FILLED)  # Image, position, radius, RGB
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)  # Create a line between the tips of the index finger and thumb

        length = hypot(x2 - x1, y2 - y1)  # Distance between the tips using the hypotenuse
        # Convert hand range to volume range (-63.5 to 0)
        vol = np.interp(length, [30, 350], [volMin, volMax])
        volbar = np.interp(length, [30, 350], [400, 150])
        volper = np.interp(length, [30, 350], [0, 100])

        print(vol, int(length))
        volume.SetMasterVolumeLevel(vol, None)

        # Hand range: 30 - 350, Volume range: -63.5 - 0.0
        # Create volume bar for volume level
        cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 255), 4)  # Image, initial position, ending position, RGB, thickness
        cv2.rectangle(img, (50, int(volbar)), (85, 400), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, f"{int(volper)}%", (10, 40), cv2.FONT_ITALIC, 1, (0, 255, 98), 3)
        # Tell the volume percentage, location, font of text, length, RGB color, thickness

    cv2.imshow('Image', img)  # Show the video
    if cv2.waitKey(1) & 0xFF == ord(' '):  # Use spacebar to stop
        break

cap.release()  # Stop the camera
cv2.destroyAllWindows()  # Close the window
