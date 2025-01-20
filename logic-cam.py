
"""
- Created on Mon jAN 30 12:43:37 2025
-Contact:ds.info4ll@gmail.com/+4792348813
- @author: Abdulrazzag Alewy

- @Topic: CONTROLL CAMERA  AND TAKE PIC VIA WEBSERVER
"""


from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Initialize the camera (0 for default webcam, change to another number for other cameras, 1 for external web-cam)
camera = cv2.VideoCapture(1)

def gen_frames():
    while True:
        success, frame = camera.read()  # Read frame from the camera
        if not success:
            break
        else:
            # Convert the frame to JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame to the browser
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture')
def capture():
    success, frame = camera.read()
    if success:
        # Save the captured image
        cv2.imwrite('captured_image.jpg', frame)
        return "Image Captured Successfully!"
    return "Failed to Capture Image"

if __name__ == '__main__':
    
    app.run(host='your localhost/webserver', port='your poer-number')
