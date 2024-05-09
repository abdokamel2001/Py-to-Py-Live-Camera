from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
# camera = cv2.VideoCapture(0)

width = input("Enter the width of the frame (leave empty for default): ")
height = None
if width != "" and width.isdigit():
    width = int(width)
    height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT) * width / camera.get(cv2.CAP_PROP_FRAME_WIDTH))
else:
    width = None

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        print("Original frame dimensions:", frame.shape)  # Print original frame dimensions
        
        if width:
            frame = cv2.resize(frame, (width, height))
            print("Resized frame dimensions:", frame.shape)  # Print resized frame dimensions

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