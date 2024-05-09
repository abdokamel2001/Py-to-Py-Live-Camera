from picamera2 import Picamera2
import io

class PiCameraReader:
    def __init__(self, width=None):
        self.picamera = Picamera2()
        if width:
            original_width, original_height = self.picamera.global_camera_info()
            height = int(width * original_height / original_width)
            self.picamera.configure(main={"size": (width, height)})
        self.stream = io.BytesIO()
        self.picamera.start()

    def get_frame(self):
        self.stream.seek(0)
        self.picamera.capture_array_(self.stream)
        self.stream.seek(0)
        frame_bytes = self.stream.getvalue()
        return frame_bytes

    def release(self):
        self.picamera.stop()