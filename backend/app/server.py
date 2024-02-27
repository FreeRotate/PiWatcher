#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : server.py
# @Author: LauTrueyes
# @Date  : 2024/2/27 15:19
import cv2
from flask import Flask, render_template, Response

app = Flask(__name__)

def get_camera():
    for i in range(10):  # Try up to 10 devices
        camera = cv2.VideoCapture(i)
        if camera.isOpened():
            return camera
    raise Exception("Unable to find a connected camera device.")

def generate_frames():
    camera = get_camera()
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)