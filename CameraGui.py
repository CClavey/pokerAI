import cv2
import numpy as np

def display_camera():
    cap = cv2.VideoCapture(0)#0 is phone cam 1 is web cam

    while True:
        ret, frame = cap.read()
        if ret:
            # Create a larger blank image with white background
            height, width, _ = frame.shape
            larger_frame = np.ones((height, width + 500, 3), np.uint8) * 255

            # Paste the camera feed on the left side of the larger frame
            larger_frame[:, :width] = frame

            # Display the modified frame
            cv2.imshow('Camera Feed', larger_frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    display_camera()
