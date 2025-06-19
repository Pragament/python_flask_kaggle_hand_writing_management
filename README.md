# python_flask_kaggle_hand_writing_management
This Flask-based web application allows you to manage handwritten image datasets (digits and alphabets), delete selected images, download a pre-trained digit classification model from Kaggle, and run predictions on selected digit images using that model.

---

## 💡 Features

- 📥 **Download Dataset**: Automatically fetches from Kaggle (`krsanjeev333/alphabets-digits`)
- 👁️ **View Images**: Filter images by dataset type (digit/alphabet) and label (0-9 or A-Z)
- 🗑️ **Delete Images**: Select and remove unwanted images directly from the UI
- 🤖 **Download Model**: One-click download of a pre-trained digit classifier (`nums_model.keras`)
- 🧪 **Test Digits**: Run predictions on selected digit images using the downloaded model
- 🧠 **Inline Predictions**: Shows predicted digit next to each image after testing

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd handwritten-digit-classifier
```

### 2. Install Python Dependencies

```bash
pip install flask tensorflow pillow kagglehub
```

### 3. Configure Kaggle API

Download your Kaggle API key from your [Kaggle account](https://www.kaggle.com/account) and place the `kaggle.json` in the appropriate directory:

```bash
# Windows:
C:\Users\<YourUsername>\.kaggle\kaggle.json

# macOS/Linux:
~/.kaggle/kaggle.json
```

---

## 🚀 Run the App

```bash
python app.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## 🧠 Model Info

The model is downloaded from:

- [🔗 pragament/digit-classifier-100-accuracy](https://www.kaggle.com/models/pragament/digit-classifier-100-accuracy/Keras/default?select=nums_model.keras)

**Model input:** `224x224 RGB`  
If the image is grayscale or a different size, it is automatically preprocessed.

---

## 🧪 Testing Flow

- Select one or more digit images
- Click **🧪 Test Selected**
- The app preprocesses the image and feeds it to the model
- The prediction is shown next to each image like:  
  ✅ Predicted: 3

> ⚠️ Currently optimized for **digit recognition only** (0–9)

---
