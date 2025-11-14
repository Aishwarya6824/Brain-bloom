# 🌸Brain Bloom – Deep Learning–Based Cognitive Retraining Tool

Brain Bloom is an interactive cognitive retraining application designed to help children improve visual recognition, memory, sequencing, and language skills.
It integrates MobileNetV2-based image classification, gamified cognitive tasks, and SQLite performance tracking into a single user-friendly system.

---

##  Overview
The toolkit combines **Computer Vision (CNN)** and **Language-based tasks (Sentence Building)** in a playful and engaging GUI.

Brain Bloom uses:

  - Deep Learning (MobileNetV2 CNN model) for classification tasks

  - Python + Tkinter GUI for child-friendly interactions

  - SQLite database for personalized progress tracking

Children interact with animals, objects, and simple sentences in a way that encourages learning through **repetition, recall, and positive reinforcement**.

---

##  Features
1. **Tutorial Phase**  
   - Displays animal images with labels to develop recognition skills.

2. **Classification Quiz**  
   - The child guesses the correct class → receives real-time feedback.
   - All attempts are stored in the database.

3. **Timed Recall**  
   - Shows an image briefly → hides it → child recalls what they saw.
   - Helps in improving visual memory.

4. **Sentence Builder**  
   - Shuffled words → child reconstructs the correct sentence.
   - Enhances language comprehension, ordering, and grammar.

5. **Performance Tracker**  
   - Retrieves data from SQLite (sessions.db) and plots accuracy per module based on real usage.

---

## Model Information

  - Architecture: MobileNetV2 (pretrained on ImageNet)

  - Image Size: 160×160

  - Best Training Accuracy: 99.56%

  - Best Validation Accuracy: 97.83%

  - Optimized for: Lightweight, fast real-time inference for offline systems

---

## Project Structure
```bash
Brain-Bloom/
├─ data/
│  ├─ images/
│  │  ├─ cat/
│  │  ├─ dog/
│  │  ├─ cow/
│  │  ├─ deer/
│  │  └─ lion/
│  └─ sentences/
│     └─ sentences.csv
│
├─ app/
│  └─ main_app.py
│
├─ models/ ##created after running train_cnn.py
│  ├─ cnn_model.h5
│  └─ class_mapping.json
│
├─ logs/  ##created and updated in realtime
│  └─ sessions.db
│
├─ train_cnn.py
└─ requirements.txt
```

---

## Dataset
Animal image dataset (5 classes: cat, dog, cow, deer, lion) and a sentence dataset for language tasks.
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

#### 1. Install Python
Download & install Python 3.10+ from [python.org](https://www.python.org/downloads/).  
During installation, check **"Add Python to PATH"**.

#### 2. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Usage

#### 1. Train the CNN model
```bash
python train_cnn.py
```
This will:

- Train a CNN on your dataset.

- Save model → models/cnn_model.h5

- Save class mapping → models/class_mapping.json

#### 2. Run the application
```bash
python app/main_app.py
```

The GUI will launch with modules:

  - Tutorial

  - Classification Quiz

  - Timed Recall

  - Sentence Builder

  - Performance Tracker

---

## Performance Tracking

Each attempt is stored in:
```bash
logs/sessions.db
```
The Performance Tracker displays:

  - Classification Accuracy

  - Recall Accuracy

  - Sentence Builder Accuracy

based on real user interactions.

---

## Future Enhancements
  - Adaptive difficulty levels

  - Speech-based input

  - Cloud-based progress syncing

  - Expanded cognitive categories

  - Personalized reinforcement learning system

---
