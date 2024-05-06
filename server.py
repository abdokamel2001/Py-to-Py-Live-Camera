from flask import Flask, render_template, Response
from picamera2 import PiCamera
import numpy as np
import cv2
import io

app = Flask(__name__)
camera = PiCamera()

width = input("Enter the width of the frame (leave empty for default): ")
height = None
if width != "" and width.isdigit():
    width = int(width)
    height = int(camera.resolution[1] * int(width) / int(camera.resolution[0]))
else:
    width = None

def update_frames():
    stream = io.BytesIO()
    for _ in camera.capture_continuous(stream, format='jpeg'):
        stream.seek(0)
        frame = cv2.imdecode(np.frombuffer(stream.read(), dtype=np.uint8), 1)
        
        if frame is None:
            continue
            
        if width:
            frame = cv2.resize(frame, (width, height))

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        stream.seek(0)
        stream.truncate()

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/video')
def video():
    """Stream video frames"""
    return Response(update_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)