import os
import numpy as np
import tensorflow as tf
from flask import Flask, request, render_template, jsonify
from PIL import Image
import base64
from io import BytesIO

app = Flask(__name__)

# 配置
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 类别名称
CLASS_NAMES = [
    'airplane', 'automobile', 'bird', 'cat', 'deer',
    'dog', 'frog', 'horse', 'ship', 'truck'
]

# 加载模型
try:
    model = tf.keras.models.load_model('my_model.h5')
    print("模型加载成功")
except Exception as e:
    print(f"模型加载失败: {e}")
    model = None


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def preprocess_image(image):
    img = image.convert('RGB').resize((32, 32))
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)


def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"success": False, "error": "模型未加载"})

    if 'file' not in request.files:
        return jsonify({"success": False, "error": "未上传文件"})

    file = request.files['file']

    if file.filename == '':
        return jsonify({"success": False, "error": "未选择文件"})

    if file and allowed_file(file.filename):
        try:
            image = Image.open(file.stream)
            processed_image = preprocess_image(image)
            predictions = model.predict(processed_image)[0]

            results = []
            for i, score in enumerate(predictions):
                results.append({
                    "class_name": CLASS_NAMES[i],
                    "probability": float(score * 100)
                })

            results.sort(key=lambda x: x["probability"], reverse=True)
            top3_results = results[:3]
            img_base64 = image_to_base64(image)

            return jsonify({
                "success": True,
                "image_data": img_base64,
                "main_prediction": top3_results[0],
                "predictions": top3_results
            })

        except Exception as e:
            return jsonify({"success": False, "error": f"处理错误: {str(e)}"})

    return jsonify({"success": False, "error": "不支持的文件格式"})


if __name__ == '__main__':
    app.run(debug=True)
