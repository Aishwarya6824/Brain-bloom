# 🐾 Brain Bloom (Deep Learning)

This project is a **Deep Learning–based Cognitive Retraining Tool** designed to assist children with disabilities in improving **memory, attention, and language skills** through gamified exercises.

---

##  Overview
The toolkit combines **Computer Vision (CNN)** and **Language-based tasks (Sentence Building)** in a playful and engaging GUI.  
Children interact with animals, objects, and simple sentences in a way that encourages learning through **repetition, recall, and positive reinforcement**.

---

##  Features
1. **Tutorial Phase**  
   - Shows animal images with their names to build recognition.

2. **Classification Quiz**  
   - Child guesses the correct class → immediate feedback (✅ Correct / ❌ Incorrect).

3. **Timed Recall**  
   - Image shown briefly → hidden → child recalls from options.

4. **Sentence Builder**  
   - Words shuffled → child reconstructs simple sentences.  
   - Helps improve grammar, sequencing, and vocabulary.

5. **Performance Tracker**  
   - Logs each session in SQLite.  
   - Plots accuracy trends to monitor progress.

---

## Dataset
Animal image dataset (5 classes: **cat, dog, cow, deer, lion**) and child-friendly sentences.

Download dataset from Google Drive:  
[📥 Dataset Link](https://drive.google.com/drive/folders/1h53dtNDbMotvzJFER9fXXNDePuFhFU1b?usp=sharing )  

After download, place it like this:
```
cog_retrain/
├─ data/
│ ├─ images/
│ │ ├─ cat/
│ │ ├─ dog/
│ │ ├─ cow/
│ │ ├─ deer/
│ │ └─ lion/
│ └─ sentences/
│ └─ sentences.csv
```

---

## Installation

### 1. Install Python
Download & install Python 3.10+ from [python.org](https://www.python.org/downloads/).  
During installation, check **"Add Python to PATH"**.

### 2. Install dependencies
```bash
pip install tensorflow keras pillow matplotlib scikit-learn spacy
python -m spacy download en_core_web_sm
```

---

## Usage

### 1. Train the CNN model
```bash
python train_cnn.py
```
This will:

- Train a CNN on your dataset.

- Save model → models/cnn_model.h5

- Save class mapping → models/class_mapping.json

### 2. Run the application
```bash
python app/main_app.py
```
