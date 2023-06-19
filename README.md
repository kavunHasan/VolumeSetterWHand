# Gesture-Controlled Volume using Hand Tracking

This project enables gesture-controlled system volume using hand tracking. It utilizes the `mediapipe` library to detect and track hand landmarks, calculates the distance between specific landmarks to determine the volume level, and adjusts the system volume accordingly using the `pycaw` library.

## Requirements

- Python 3.x
- OpenCV (`pip install opencv-python`)
- Mediapipe (`pip install mediapipe`)
- Numpy (`pip install numpy`)
- Pycaw (`pip install pycaw`)
- Comtypes (`pip install comtypes`)

## Usage

1. Connect a webcam to your system.
2. Run the `gesture_volume_control.py` script.
3. A video window will open, showing the webcam feed.
4. Extend your hand in front of the webcam, ensuring it is clearly visible.
5. Make a gesture by touching your thumb to the tip of your index finger. The distance between these two points controls the system volume.
6. As you change the distance between your thumb and index finger, the volume level will adjust accordingly.
7. The current volume level and percentage will be displayed on the video window.

To stop the program, press the spacebar.

## Acknowledgements

This project is based on the following libraries:

- [Mediapipe](https://github.com/google/mediapipe)
- [Pycaw](https://github.com/AndreMiras/pycaw)

## Additional Notes

- The code assumes that your default audio output device is the system speakers. If you have a different audio output device, you may need to modify the code accordingly.
- Adjust the hand gesture range and volume range in the code (`[30, 350]` and `[-63.5, 0]`) based on your hand size and desired volume range.
- Ensure your hand is well-illuminated and not obstructed by any objects for accurate hand tracking.

Please note that this project is intended for educational purposes and may require further customization for production environments.
