from flask import Flask, render_template, Response
from picamera_reader import PiCameraReader

width = input("Enter the width of the frame (leave empty for default): ")
height = None
if width != "" and width.isdigit():
    width = int(width)
else:
    width = None

camera = PiCameraReader(width=width)
app = Flask(__name__)

def update_frames():
    while True:
        frame = camera.read()  # Read the next frame from the PiCameraReader
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(update_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)