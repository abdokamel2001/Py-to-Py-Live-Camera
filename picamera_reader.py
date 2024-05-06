from picamera2 import PiCamera
import numpy as np
import io

class PiCameraReader:
    def __init__(self, width=None):
        self.camera = PiCamera()
        if width is None:
            self.camera.resolution = self.camera.MAX_RESOLUTION
        else:
            self.camera.resolution = self.calculate_resolution(width)
        self.stream = io.BytesIO()
        self.frame = None

    def read(self):
        if self.frame is None:
            self.frame = self.capture_frame()
        return self.frame

    def capture_frame(self):
        self.stream.seek(0)
        self.camera.capture(self.stream, format='jpeg')
        self.stream.seek(0)
        frame = np.frombuffer(self.stream.getvalue(), dtype=np.uint8)
        self.stream.seek(0)
        self.stream.truncate()
        return frame

    def calculate_resolution(self, width):
        max_width, max_height = self.camera.MAX_RESOLUTION
        if max_width < width:
            raise ValueError("Requested width exceeds maximum resolution")
        ratio = width / max_width
        height = int(max_height * ratio)
        return (width, height)

    def release(self):
        self.camera.close()

if __name__ == "__main__":
    reader = PiCameraReader(width=640)
    frame = reader.read()
    print("Frame shape:", frame.shape)
    reader.release()
