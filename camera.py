import subprocess
import cv2

def get_available_cameras():
    available_cameras = []
    try:
        # Execute the v4l2-ctl command to list devices
        output = subprocess.check_output(['v4l2-ctl', '--list-devices'], universal_newlines=True)
        
        # Split the output into lines
        lines = output.strip().split('\n')

        # Iterate over the lines to extract camera indices
        for line in lines:
            if '/dev/video' in line:
                # Extract the camera index from the line
                index = int(line.split('/dev/video')[1].split(':')[0])
                available_cameras.append(index)
    except subprocess.CalledProcessError as e:
        print("Error:", e)
    
    return available_cameras

def get_frame(camera_index):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_index}")
        return None
    
    ret, frame = cap.read()
    cap.release()
    if ret:
        return frame
    else:
        print(f"Error: Could not read frame from camera {camera_index}")
        return None

if __name__ == "__main__":
    cameras = get_available_cameras()
    if cameras:
        for camera_index in cameras:
            frame = get_frame(camera_index)
            if frame is not None:
                print(f"Camera {camera_index}: Frame shape:", frame.shape)
                break
    else:
        print("No cameras available.")
