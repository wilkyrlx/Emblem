import cv2

class CameraSwitcher:
    def __init__(self):
        self.current_camera_index = 1
        self.cap = cv2.VideoCapture(self.current_camera_index)

        if not self.cap.isOpened():
            raise Exception("Error: Could not open initial webcam.")

    def switch_camera(self):
        """
        Switch to the next camera.
        0: generally the default webcam
        1: if Camo Studio webcam (or other) connected
        """
        self.cap.release()  
        self.current_camera_index = (self.current_camera_index + 1) % 2     # 0 or 1
        self.cap = cv2.VideoCapture(self.current_camera_index)

    def run(self):
        """Run the camera feed display loop."""
        print("Press 's' to switch camera, 'q' to quit.")
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print(f"Error: Could not read frame from camera {self.current_camera_index}.")
                break

            cv2.imshow("Camera Feed", frame)

            # User Input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # Quit the loop
                break
            elif key == ord('s'):  # Switch camera
                self.switch_camera()

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        camera_switcher = CameraSwitcher()
        camera_switcher.run()
    except Exception as e:
        print(e)
