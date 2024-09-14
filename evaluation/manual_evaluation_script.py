import json
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import PhotoImage

class CodeEvaluationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Evaluation App")
        self.data = []
        self.current_index = 0
        self.scores = []

        # Load JSON data
        self.load_data()

        # Load star images
        self.empty_star = PhotoImage(file="images/empty_star.png")  # Path to empty star image
        self.filled_star = PhotoImage(file="images/full_star.png")  # Path to filled star image

        # GUI Layout
        self.create_widgets()

    def load_data(self):
        file_path = filedialog.askopenfilename(title="Select JSON File", filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, 'r') as f:
                self.data = json.load(f)
                self.scores = [{} for _ in self.data]  # Placeholder for scores
    
    def create_widgets(self):
        # Display prefix + suffix with a placeholder
        self.context_label = tk.Label(self.root, text="Context (Prefix + Suffix):")
        self.context_label.pack()
        self.context_text = tk.Text(self.root, height=12, wrap=tk.WORD)
        self.context_text.pack()

        # Display correct middle value
        self.correct_label = tk.Label(self.root, text="True Middle Value:")
        self.correct_label.pack()
        self.correct_text = tk.Text(self.root, height=6, wrap=tk.WORD)
        self.correct_text.pack()

        # Display generated middle value
        self.generated_label = tk.Label(self.root, text="Guessed Middle Value:")
        self.generated_label.pack()
        self.generated_text = tk.Text(self.root, height=6, wrap=tk.WORD)
        self.generated_text.pack()

        # Star Rating for each metric
        self.create_star_rating("Overall satisfaction:", 'satisfaction')
        self.create_star_rating("Similarity to the true value:", 'similarity')
        self.create_star_rating("Completeness:", 'completeness')
        self.create_star_rating("Does it contains few/many errors? (the higher the fewer):", 'errors')

        # Navigation Buttons
        self.prev_button = tk.Button(self.root, text="Previous", command=self.previous_sample)
        self.prev_button.pack(side=tk.LEFT)
        self.next_button = tk.Button(self.root, text="Next", command=self.next_sample)
        self.next_button.pack(side=tk.RIGHT)
        
        self.save_button = tk.Button(self.root, text="Save Scores", command=self.save_scores_to_file)
        self.save_button.pack()

        # Load first sample
        self.display_sample()

    def create_star_rating(self, label_text, score_key):
        label = tk.Label(self.root, text=label_text)
        label.pack()
        
        stars_frame = tk.Frame(self.root)
        stars_frame.pack()

        star_buttons = []
        for i in range(5):
            star_button = tk.Button(stars_frame, image=self.empty_star, bd=0, command=lambda i=i: self.set_star_rating(score_key, i+1, star_buttons))
            star_button.grid(row=0, column=i)
            star_buttons.append(star_button)

        setattr(self, f"{score_key}_stars", star_buttons)
        setattr(self, f"{score_key}_score", 0)

    def set_star_rating(self, score_key, rating, star_buttons):
        setattr(self, f"{score_key}_score", rating)
        
        for i in range(5):
            if i < rating:
                star_buttons[i].config(image=self.filled_star)
            else:
                star_buttons[i].config(image=self.empty_star)

    def display_sample(self):
        if self.current_index < 0 or self.current_index >= len(self.data):
            return
        
        sample = self.data[self.current_index]
        
        # Display prefix + suffix with placeholder
        self.context_text.delete(1.0, tk.END)
        context = f"{sample['prefix']} <...> {sample['suffix']}"
        self.context_text.insert(tk.END, context)

        # Display correct middle value
        self.correct_text.delete(1.0, tk.END)
        self.correct_text.insert(tk.END, sample['correct_middle'])

        # Display generated middle value
        self.generated_text.delete(1.0, tk.END)
        self.generated_text.insert(tk.END, sample['generated'])

        # Load previous star ratings if available
        for score_key in ['satisfaction', 'similarity', 'completeness', 'errors']:
            rating = self.scores[self.current_index].get(score_key, 0)
            self.set_star_rating(score_key, rating, getattr(self, f"{score_key}_stars"))

    def save_scores(self):
        self.scores[self.current_index] = {
            'satisfaction': getattr(self, 'satisfaction_score'),
            'similarity': getattr(self, 'similarity_score'),
            'completeness': getattr(self, 'completeness_score'),
            'errors': getattr(self, 'errors_score'),
            'prefix': self.data[self.current_index]['prefix'],
            'suffix': self.data[self.current_index]['suffix'],
            'correct_middle': self.data[self.current_index]['correct_middle'],
            'generated_middle': self.data[self.current_index]['generated']
        }

    def next_sample(self):
        self.save_scores()  # Save current sample's scores
        self.current_index += 1
        if self.current_index >= len(self.data):
            self.current_index = len(self.data) - 1
        self.display_sample()

    def previous_sample(self):
        self.save_scores()  # Save current sample's scores
        self.current_index -= 1
        if self.current_index < 0:
            self.current_index = 0
            messagebox.showinfo("Info", "This is the first sample.")
        self.display_sample()

    def save_scores_to_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(self.scores, f, indent=4)
            messagebox.showinfo("Info", "Scores saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeEvaluationApp(root)
    root.mainloop()
