
# python_flask_kaggle_hand_writing_management

A Python Flask web application for managing, viewing, testing, and deleting handwritten digit and alphabet datasets. Users can interactively select dataset types, download pretrained models from Kaggle, and test handwritten digit images using a pre-trained deep learning model.

---

## 🚀 Features

- 📁 View datasets (Alphabets & Digits)
- ✅ Select & test specific images
- 🧠 Download a Kaggle-hosted digit recognition model (`nums_model.keras`)
- 📸 Predict digits from uploaded/tested images using the model
- ❌ Delete selected dataset images
- ⚡ Dynamic frontend using Flask & JavaScript


---

## 🛠️ Setup Instructions

### 1. Clone this Repository
```bash
git clone https://github.com/yourusername/python_flask_kaggle_hand_writing_management.git
cd python_flask_kaggle_hand_writing_management
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Kaggle API
- Place your `kaggle.json` API key in:
  ```bash
  C:\Users\<YourUsername>\.kaggle\kaggle.json
  ```
- Or set the environment variable:
  ```bash
  export KAGGLE_USERNAME=your_username
  export KAGGLE_KEY=your_key
  ```

---

## ▶️ Run the App

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

---

## 📦 Downloading the Model

The model used (`nums_model.keras`) is downloaded from:

- https://www.kaggle.com/models/pragament/digit-classifier-100-accuracy

It will be saved under `static/model/` and automatically checked for existence to prevent redownload.

---

## 🧪 Testing Digits

- Select digit images and click "🧪 Test Selected"
- The model will return predictions for selected images
- Predictions are shown beside each image

---

## 📂 Dataset Source

- Kaggle Dataset: https://www.kaggle.com/datasets/krsanjeev333/alphabets-digits

---

## 📋 requirements.txt

```
Flask
tensorflow
Pillow
kaggle
kagglehub
```

---

## 📄 License

This project is under the MIT License.
