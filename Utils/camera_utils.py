from picamera2 import Picamera2
import numpy as np

class Camera(Picamera2):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(self.create_preview_configuration())
        self.start()
    
    def read_rgb(self):
        frame = self.capture_array("main")
        if frame is None or frame.size == 0:
            return None
        frame = np.array(frame)[:,:,:3]
        return frame
    
    def read_bgr(self):
        frame = self.capture_array("main")
        if frame is None or frame.size == 0:
            return None
        frame = np.array(frame)[:,:,[2,1,0]]
        return frame
    
    def read_img(self):
        return self.capture_image("main")
    

class CameraHandler:
    def __init__(self, camera: Camera):
        self.camera = camera
        
    def __enter__(self):
        return self.camera
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.camera.close()
        if exc_type is KeyboardInterrupt:
            print("Camera connection closed due to KeyboardInterrupt.")
        elif exc_type:
            print(f"An error occurred: {exc_val}")
        else:
            print("Camera connection closed.")
            
    def __del__(self):
        self.camera.close()
        print("Camera connection closed.")
