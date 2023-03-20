import os
from flask import Flask, request, jsonify
app = Flask(__name__)
@app.route('/')
def index():
    return 'YOLOv5 Object Detection API'
@app.route('/detect', methods=['POST'])
def detect():
    file = request.files['image']
    file.save('image.jpg')
    os.system('python detect.py --source image.jpg --weights yolov5s.pt --conf 0.4 --iou 0.5 --device cpu')
    with open('results.txt') as f:
        results = f.read()
    return jsonify({'results': results})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
