import subprocess
import cv2

def get_camera_index():
    try:
        output = subprocess.check_output(['v4l2-ctl', '--list-devices'], universal_newlines=True)
        lines = output.strip().split('\n')
        for line in lines:
            if '/dev/video' in line:
                camera_index = int(line.split('/dev/video')[1].split(':')[0])
                return camera_index
    except subprocess.CalledProcessError as e:
        print("Error:", e)
    return None

def main():
    camera_index = get_camera_index()
    if camera_index is not None:
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            print(f"Error: Could not open camera {camera_index}")
            return
        ret, frame = cap.read()
        cap.release()
        if ret:
            print(f"Frame shape: {frame.shape}")
        else:
            print(f"Error: Could not read frame from camera {camera_index}")
    else:
        print("No cameras available.")

if __name__ == "__main__":
    main()
