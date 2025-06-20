from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
import os
import shutil
import kagglehub
from keras.models import load_model
from keras.preprocessing import image
import numpy as np

app = Flask(__name__)
app.secret_key = 'supersecretkey'

DATASET_NAME = 'krsanjeev333/alphabets-digits'
DATASET_BASE_PATH = 'static/dataset/dataset/dataset'
MODEL_DIR = "static/model"
MODEL_FILENAME = "nums_model.keras"
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILENAME)
loaded_model = None

def download_and_extract_dataset():
    alphabet_sample = os.path.join(DATASET_BASE_PATH, 'alphabet-dataset', 'alphabet-dataset', 'Train', 'A')
    digit_sample = os.path.join(DATASET_BASE_PATH, 'digit-dataset', 'digit-dataset', '0')

    if not (os.path.isdir(alphabet_sample) and os.path.isdir(digit_sample)):
        print("📥 Downloading dataset from Kaggle...")
        import kaggle
        kaggle.api.dataset_download_files(DATASET_NAME, path=DATASET_BASE_PATH, unzip=True)
        print("✅ Dataset downloaded.")
    else:
        print("✅ Dataset already exists. Skipping download.")

# Run at startup
download_and_extract_dataset()

@app.route('/', methods=['GET', 'POST'])
def index():
    dataset_type = request.form.get('dataset_type')
    selected_label = request.form.get('label')
    image_paths = []

    base_path = None
    if dataset_type == 'alphabet':
        base_path = os.path.join(DATASET_BASE_PATH, 'alphabet-dataset', 'alphabet-dataset', 'Train')
    elif dataset_type == 'digit':
        base_path = os.path.join(DATASET_BASE_PATH, 'digit-dataset', 'digit-dataset')

    if base_path and selected_label:
        folder_path = os.path.join(base_path, selected_label.upper())
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    rel_path = os.path.relpath(os.path.join(folder_path, file), 'static')
                    image_paths.append(rel_path.replace("\\", "/"))

    return render_template(
        'index.html',
        dataset_type=dataset_type,
        selected_label=selected_label,
        image_paths=image_paths
    )

@app.route('/delete', methods=['POST'])
def delete_images():
    selected_images = request.form.getlist('selected_images')
    dataset_type = request.form.get('dataset_type')
    selected_label = request.form.get('label')

    for rel_path in selected_images:
        abs_path = os.path.join('static', rel_path.replace("/", os.sep))
        if os.path.exists(abs_path):
            try:
                os.remove(abs_path)
                print(f"Deleted: {abs_path}")
            except Exception as e:
                print(f"Error deleting {abs_path}: {e}")

    return redirect(url_for('index'), code=307)

@app.route('/download_model', methods=['POST'])
def download_model():
    data = request.get_json()
    try:
        if os.path.exists(MODEL_PATH):
            return jsonify({'message': '✅ Model already exists.'})

        model_path = kagglehub.model_download("pragament/digit-classifier-100-accuracy/keras/default")
        os.makedirs(MODEL_DIR, exist_ok=True)
        downloaded_model_file = os.path.join(model_path, MODEL_FILENAME)

        if os.path.exists(downloaded_model_file):
            shutil.copy(downloaded_model_file, MODEL_PATH)
            return jsonify({'message': '✅ Model downloaded successfully.'})
        else:
            return jsonify({'message': '❌ Model file not found after download.'})
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        return jsonify({'message': '❌ Error during model download.'})

from flask import jsonify
import tensorflow as tf
from PIL import Image
import numpy as np

# Load model once globally
model = None
MODEL_PATH = "static/model/nums_model.keras"

def load_model():
    global model
    if model is None and os.path.exists(MODEL_PATH):
        model = tf.keras.models.load_model(MODEL_PATH)
        print("✅ Model loaded.")
    elif not os.path.exists(MODEL_PATH):
        print("❌ Model file not found.")

def preprocess_image(img_path):
    # Load as grayscale
    img = Image.open(os.path.join("static", img_path)).convert("L")

    # Resize to 224x224
    img = img.resize((224, 224))

    # Convert to RGB (model was trained on RGB)
    img = img.convert("RGB")

    # Convert to numpy and normalize to [0, 1]
    img_array = np.array(img).astype("float32") / 255.0

    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route('/test_images', methods=['POST'])
def test_images():
    try:
        data = request.get_json()
        image_paths = data.get('images', [])
        predictions = {}

        load_model()  # Ensure model is loaded
        if model is None:
            return jsonify({img: "❌ Model not found" for img in image_paths})

        for img_rel_path in image_paths:
            try:
                img_array = preprocess_image(img_rel_path)
                prediction = model.predict(img_array)
                predicted_label = str(np.argmax(prediction[0]))
                predictions[img_rel_path] = predicted_label
                print(f"🖼️ {img_rel_path} → {predicted_label}")
            except Exception as e:
                predictions[img_rel_path] = "❌ Error"
                print(f"❌ Error with {img_rel_path}: {e}")

        return jsonify(predictions)

    except Exception as e:
        print("❌ Failed to process test images:", e)
        return jsonify({'error': 'Internal server error'}), 500




if __name__ == '__main__':
    app.run(debug=True)
