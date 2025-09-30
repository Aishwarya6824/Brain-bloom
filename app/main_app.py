import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import os, random, time, json, sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Paths
DATA_DIR = "D:/cog_retrain/data/images"
SENT_PATH = "D:/cog_retrain/data/sentences/sentences.csv"
MODEL_PATH = "D:/cog_retrain/models/cnn_model.h5"
MAPPING_PATH = "D:/cog_retrain/models/class_mapping.json"
LOG_DB = "D:/cog_retrain/logs/sessions.db"

# Colors & styles
BG_COLOR = "#f0f8ff"
BTN_COLOR = "#aed6f1"
BTN_ACTIVE = "#5dade2"
TITLE_FONT = ("Comic Sans MS", 20, "bold")
TEXT_FONT = ("Arial", 14, "bold")

# Load classes
CLASS_LIST = os.listdir(DATA_DIR) if os.path.exists(DATA_DIR) else []
print("DEBUG - Looking for images in:", os.path.abspath(DATA_DIR))
print("DEBUG - Found classes:", CLASS_LIST)

# Load sentences
SENTENCES = []
if os.path.exists(SENT_PATH):
    df = pd.read_csv(SENT_PATH)
    if "sentence" in df.columns:
        SENTENCES = df["sentence"].dropna().tolist()

# Init DB
os.makedirs(os.path.dirname(LOG_DB), exist_ok=True)
conn = sqlite3.connect(LOG_DB)
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS attempts
             (id INTEGER PRIMARY KEY, user_id TEXT, session_date TEXT,
              feature TEXT, item_id TEXT, user_response TEXT,
              correct INTEGER, model_confidence REAL, duration REAL)''')
conn.commit()


# ---------------- Main App ----------------
class CogTrainerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🐾 Cognitive Retraining Toolkit")
        self.root.configure(bg=BG_COLOR)
        self.user_id = simpledialog.askstring("User", "Enter child name:") or "child_1"

        tk.Label(root, text=f"Welcome {self.user_id} 🎈",
                 font=TITLE_FONT, bg=BG_COLOR, fg="#2e4053").pack(pady=20)
        tk.Label(root, text="Choose a feature below to begin ⬇️",
                 font=TEXT_FONT, bg=BG_COLOR).pack(pady=10)

        # Feature buttons
        btns = [
            ("📚 Tutorial Phase", self.tutorial),
            ("🐾 Classification Quiz", self.quiz),
            ("⏱ Timed Recall", self.timed_recall),
            ("✍️ Sentence Builder", self.sentence_builder),
            ("📊 Performance Tracker", self.tracker)
        ]
        for text, cmd in btns:
            tk.Button(root, text=text, command=cmd,
                      font=TEXT_FONT, width=22, height=2,
                      bg=BTN_COLOR, activebackground=BTN_ACTIVE).pack(pady=8)

    # Feature A: Tutorial
    def tutorial(self):
        top = tk.Toplevel(self.root, bg=BG_COLOR)
        tk.Label(top, text="📚 Tutorial Phase", font=TITLE_FONT, bg=BG_COLOR).pack(pady=10)
        lbl = tk.Label(top, font=TEXT_FONT, bg=BG_COLOR)
        lbl.pack()
        img_label = tk.Label(top, bg=BG_COLOR)
        img_label.pack(pady=10)

        def show_next():
            cls = random.choice(CLASS_LIST)
            files = os.listdir(os.path.join(DATA_DIR, cls))
            img_path = os.path.join(DATA_DIR, cls, random.choice(files))
            img = Image.open(img_path).resize((250, 250))
            tk_img = ImageTk.PhotoImage(img)
            img_label.config(image=tk_img)
            img_label.image = tk_img
            lbl.config(text=f"👉 This is a {cls}")

        tk.Button(top, text="Next ➡️", command=show_next,
                  font=TEXT_FONT, bg=BTN_COLOR, activebackground=BTN_ACTIVE).pack(pady=5)
        show_next()

    # Feature B: Quiz
    def quiz(self):
        top = tk.Toplevel(self.root, bg=BG_COLOR)
        tk.Label(top, text="🐾 Classification Quiz", font=TITLE_FONT, bg=BG_COLOR).pack(pady=10)
        score_var = tk.StringVar(value="Score: 0/0 ⭐")
        tk.Label(top, textvariable=score_var, font=TEXT_FONT, bg=BG_COLOR, fg="#117864").pack()

        img_label = tk.Label(top, bg=BG_COLOR)
        img_label.pack(pady=15)
        btn_frame = tk.Frame(top, bg=BG_COLOR)
        btn_frame.pack()
        feedback = tk.Label(top, text="", font=TEXT_FONT, bg=BG_COLOR)
        feedback.pack(pady=8)

        stats = {"score": 0, "total": 0}

        def next_q():
            cls = random.choice(CLASS_LIST)
            img_path = os.path.join(DATA_DIR, cls, random.choice(os.listdir(os.path.join(DATA_DIR, cls))))
            img = Image.open(img_path).resize((250, 250))
            tk_img = ImageTk.PhotoImage(img)
            img_label.config(image=tk_img)
            img_label.image = tk_img
            feedback.config(text="")
            for w in btn_frame.winfo_children(): w.destroy()
            options = random.sample(CLASS_LIST, min(4, len(CLASS_LIST)))
            if cls not in options: options[0] = cls
            random.shuffle(options)
            for opt in options:
                tk.Button(btn_frame, text=opt, width=12, height=2,
                          font=TEXT_FONT, bg=BTN_COLOR, activebackground=BTN_ACTIVE,
                          command=lambda o=opt, truth=cls: check(o, truth)).pack(side=tk.LEFT, padx=6)

        def check(choice, truth):
            stats["total"] += 1
            if choice == truth:
                stats["score"] += 1
                feedback.config(text="🎉 Correct!", fg="green")
            else:
                feedback.config(text=f"❌ Oops! It was {truth}", fg="red")
            score_var.set(f"Score: {stats['score']}/{stats['total']} ⭐")
            top.after(1500, next_q)

        next_q()

    # Feature C: Timed Recall
    def timed_recall(self):
        top = tk.Toplevel(self.root, bg=BG_COLOR)
        tk.Label(top, text="⏱ Timed Recall", font=TITLE_FONT, bg=BG_COLOR).pack(pady=10)
        img_label = tk.Label(top, bg=BG_COLOR)
        img_label.pack(pady=15)
        feedback = tk.Label(top, text="", font=TEXT_FONT, bg=BG_COLOR)
        feedback.pack(pady=8)

        def start_round():
            cls = random.choice(CLASS_LIST)
            img_path = os.path.join(DATA_DIR, cls, random.choice(os.listdir(os.path.join(DATA_DIR, cls))))
            img = Image.open(img_path).resize((250, 250))
            tk_img = ImageTk.PhotoImage(img)
            img_label.config(image=tk_img)
            img_label.image = tk_img
            feedback.config(text="Look carefully 👀")
            top.after(3000, lambda: ask(cls))

        def ask(truth):
            img_label.config(image="")
            feedback.config(text="What did you see?")
            options = random.sample(CLASS_LIST, min(4, len(CLASS_LIST)))
            if truth not in options: options[0] = truth
            random.shuffle(options)
            for opt in options:
                tk.Button(top, text=opt, width=12, height=2,
                          font=TEXT_FONT, bg=BTN_COLOR, activebackground=BTN_ACTIVE,
                          command=lambda o=opt: check(o, truth)).pack(side=tk.LEFT, padx=6)

        def check(choice, truth):
            if choice == truth:
                feedback.config(text="🎉 Great memory!", fg="green")
            else:
                feedback.config(text=f"❌ It was {truth}", fg="red")

        tk.Button(top, text="Start ▶️", command=start_round,
                  font=TEXT_FONT, bg=BTN_COLOR, activebackground=BTN_ACTIVE).pack(pady=8)

    # Feature D: Sentence Builder
    def sentence_builder(self):
        if not SENTENCES:
            messagebox.showerror("Error", "No sentences found.")
            return
        top = tk.Toplevel(self.root, bg=BG_COLOR)
        tk.Label(top, text="✍️ Sentence Builder", font=TITLE_FONT, bg=BG_COLOR).pack(pady=10)
        frame = tk.Frame(top, bg=BG_COLOR)
        frame.pack()
        feedback = tk.Label(top, text="", font=TEXT_FONT, bg=BG_COLOR)
        feedback.pack(pady=8)

        def next_sent():
            truth = random.choice(SENTENCES)
            words = truth.split()
            random.shuffle(words)
            for w in frame.winfo_children(): w.destroy()
            for word in words:
                tk.Button(frame, text=word, font=TEXT_FONT,
                          bg=BTN_COLOR, activebackground=BTN_ACTIVE,
                          command=lambda w=word: pick(w, truth)).pack(side=tk.LEFT, padx=4)
            top.selected = []
            feedback.config(text="")

        def pick(word, truth):
            top.selected.append(word)
            built = " ".join(top.selected)
            feedback.config(text=f"Constructed: {built}")
            if len(top.selected) == len(truth.split()):
                if built.lower() == truth.lower():
                    feedback.config(text="🎉 Correct Sentence!", fg="green")
                else:
                    feedback.config(text=f"❌ Wrong! Correct: {truth}", fg="red")
                top.after(2000, next_sent)

        next_sent()

    # Feature E: Performance Tracker
    def tracker(self):
        df = pd.read_sql_query("SELECT feature, correct FROM attempts", conn)
        if df.empty:
            messagebox.showinfo("Info", "No data yet.")
            return
        agg = df.groupby("feature")["correct"].mean() * 100
        fig, ax = plt.subplots()
        agg.plot(kind="bar", ax=ax, color="#5dade2")
        ax.set_ylabel("Accuracy %")
        ax.set_title(f"Performance of {self.user_id}")
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = CogTrainerApp(root)
    root.mainloop()
