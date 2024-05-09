import picamera
import cv2

def capture_frames():
    # Initialize the camera
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)  # Set the resolution
        camera.framerate = 30  # Set the framerate

        # Capture frames continuously
        with picamera.array.PiRGBArray(camera) as stream:
            for _ in camera.capture_continuous(stream, format='bgr', use_video_port=True):
                # Convert the raw RGB data to cv2 format
                frame = stream.array

                # Process the frame (you can perform any cv2 operations here)

                # Display the frame
                cv2.imshow('Camera', frame)

                # Clear the stream in preparation for the next frame
                stream.seek(0)
                stream.truncate()

                # Wait for the 'q' key to exit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    # Close the OpenCV windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_frames()
