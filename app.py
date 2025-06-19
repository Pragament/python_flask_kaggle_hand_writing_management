from flask import Flask, render_template, request
import os
import kaggle

app = Flask(__name__)

# Dataset from: https://www.kaggle.com/datasets/krsanjeev333/alphabets-digits
DATASET_NAME = 'krsanjeev333/alphabets-digits'
DATASET_BASE_PATH = 'static/dataset/dataset/dataset'

def download_and_extract_dataset():
    alphabet_sample = os.path.join(DATASET_BASE_PATH, 'alphabet-dataset', 'alphabet-dataset', 'Train', 'A')
    digit_sample = os.path.join(DATASET_BASE_PATH, 'digit-dataset', 'digit-dataset', '0')

    if not (os.path.isdir(alphabet_sample) and os.path.isdir(digit_sample)):
        print("📥 Downloading dataset from Kaggle...")
        print(f"Dataset URL: https://www.kaggle.com/datasets/krsanjeev333/alphabets-digits")
        kaggle.api.dataset_download_files(DATASET_NAME, path=DATASET_BASE_PATH, unzip=True)
        print("✅ Download complete and extracted.")
    else:
        print("✅ Dataset already exists. Skipping download.")


# 🟩 Run once when app starts
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
                print(f"🗑️ Deleted: {abs_path}")
            except Exception as e:
                print(f"❌ Error deleting {abs_path}: {e}")

    # Rebuild image list
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

if __name__ == '__main__':
    app.run(debug=True)
