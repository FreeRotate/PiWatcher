#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : server.py
# @Author: LauTrueyes
# @Date  : 2024/2/27 15:19
import cv2
from flask import Flask, render_template, Response

app = Flask(__name__)
camera = cv2.VideoCapture(0)  # 0表示调用第一个相机设备，你可以根据需要更改

def generate_frames():
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
