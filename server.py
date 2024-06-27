from flask import Flask, render_template, Response
from Utils.camera_utils import CameraHandler
import cv2

app = Flask(__name__)

def generate_frames():
    with CameraHandler() as camera:
        while True:
            frame = camera.read_bgr()
            if frame is None:
                break
            
            print("Original frame dimensions:", frame.shape)
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
    
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/video')
def video():
    """Stream video frames"""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)