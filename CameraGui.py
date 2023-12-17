import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

class CameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Create a frame to hold the camera feed and additional space
        self.frame = tk.Frame(window)
        self.frame.pack()

        # Create a label to display the camera feed
        self.label = tk.Label(self.frame)
        self.label.grid(row=0, column=0, padx=250, pady=0)  # Position the camera feed

        # Create a blank label for additional white space
        self.space_label = tk.Label(self.frame, bg="white")
        self.space_label.grid(row=0, column=1, padx=250, pady=0)  # Position the white space

        # Button to close the camera
        self.close_button = tk.Button(window, text="Exit", command=self.close_camera)
        self.close_button.pack()

        self.capture()

    def capture(self):
        cap = cv2.VideoCapture(0)  # 0 is phone cam, 1 is web cam

        while True:
            ret, frame = cap.read()
            if ret:
                # Convert the frame from BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Convert the frame to ImageTk format
                img = Image.fromarray(frame_rgb)
                img_tk = ImageTk.PhotoImage(image=img)

                # Update the label with the new frame
                self.label.img_tk = img_tk
                self.label.configure(image=img_tk)

                self.window.update()

            # Break the loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def close_camera(self):
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root, "Poker Bot")
    root.mainloop()
