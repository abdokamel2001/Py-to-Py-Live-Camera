import cv2

def test_camera():
    # Initialize the camera
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Unable to open camera")
        return

    # Read and display frames from the camera
    while True:
        ret, frame = cap.read()

        # Check if frame is captured successfully
        if not ret:
            print("Error: Unable to capture frame")
            break
        else:
            print("Frame captured successfully")

        # Display the frame
        cv2.imshow("Camera Test", frame)


        # Wait for the 'q' key to be pressed to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_camera()
