import json
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import PhotoImage

class CodeEvaluationApp:
    def __init__(self, root: tk.Tk):
        """
        Initializes the Code Evaluation App.

        Args:
            root (tk.Tk): The root window of the Tkinter application.

        Attributes:
            root (tk.Tk): The root window of the Tkinter application.
            data (list): A list to store the JSON data.
            current_index (int): The current index of the data being evaluated.
            scores (list): A list to store the scores for each evaluation.
            empty_star (PhotoImage): The image for an empty star.
            filled_star (PhotoImage): The image for a filled star.

        Methods:
            load_data(): Loads the JSON data for evaluation.
            create_widgets(): Creates the GUI layout and widgets.
            create_star_rating(label_text, score_key): Creates a star rating widget.
            set_star_rating(score_key, rating, star_buttons): Sets the star rating for a metric.
            display_sample(): Displays the current sample for evaluation.
            save_scores(): Saves the scores for the current sample.
            next_sample(): Displays the next sample for evaluation.
            previous_sample(): Displays the previous sample for evaluation.
            save_scores_to_file(): Saves the scores to a JSON file.
        """
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
        """
        Prompts the user to select a JSON file and loads its content into the `data` attribute.
        
        This method uses a file dialog to allow the user to select a JSON file from their filesystem.
        Once a file is selected, it reads the file and loads its content as JSON into the `data` attribute.
        Additionally, it initializes the `scores` attribute as a list of empty dictionaries, with one
        dictionary for each item in the loaded data.
        """
        file_path = filedialog.askopenfilename(title="Select JSON File", filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, 'r') as f:
                self.data = json.load(f)
                self.scores = [{} for _ in self.data]  # Placeholder for scores
    
    def create_widgets(self):
        """
        Initializes and packs all the widgets in the GUI.
        This method creates and arranges the following widgets:
        - A label and text box for displaying the context (prefix + suffix).
        - A label and text box for displaying the correct middle value.
        - A label and text box for displaying the generated middle value.
        - Star rating widgets for various metrics including overall satisfaction, similarity to the true value, completeness, and error count.
        - Navigation buttons for moving to the previous or next sample.
        - A button for saving scores to a file.
        Additionally, it loads and displays the first sample upon initialization.
        """
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

    def create_star_rating(self, label_text: str, score_key: str):
        """
        Creates a star rating widget with a label and star buttons.
        Args:
            label_text (str): The text to display as the label for the star rating.
            score_key (str): The key used to store the star rating score and buttons.
        This method creates a label and a row of five star buttons. Each star button
        can be clicked to set the rating score. The star buttons and the score are
        stored as attributes of the instance using the provided score_key.
        """
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

    def set_star_rating(self, score_key: str, rating: int, star_buttons):
        """
        Sets the star rating for a given score key and updates the star button images accordingly.
        Args:
            score_key (str): The key associated with the score to be updated.
            rating (int): The rating value to be set, typically between 0 and 5.
            star_buttons (list): A list of button widgets representing the star ratings.
        Returns:
            None
        """
        setattr(self, f"{score_key}_score", rating)
        
        for i in range(5):
            if i < rating:
                star_buttons[i].config(image=self.filled_star)
            else:
                star_buttons[i].config(image=self.empty_star)

    def display_sample(self):
        """
        Displays the current sample's context, correct middle value, and generated middle value
        in the respective text widgets. Also loads and sets the previous star ratings if available.
        The method performs the following steps:
        1. Checks if the current index is within the valid range of the data list.
        2. Retrieves the sample at the current index.
        3. Updates the context text widget with the sample's prefix and suffix, separated by a placeholder.
        4. Updates the correct text widget with the sample's correct middle value.
        5. Updates the generated text widget with the sample's generated middle value.
        6. Loads and sets the previous star ratings for satisfaction, similarity, completeness, and errors.
        Returns:
            None
        """
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
        """
        Save the evaluation scores for the current index into the scores dictionary.

        The scores dictionary is updated with the following keys:
        - 'satisfaction': The satisfaction score.
        - 'similarity': The similarity score.
        - 'completeness': The completeness score.
        - 'errors': The errors score.
        - 'prefix': The prefix part of the data at the current index.
        - 'suffix': The suffix part of the data at the current index.
        - 'correct_middle': The correct middle part of the data at the current index.
        - 'generated_middle': The generated middle part of the data at the current index.
        """
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
        """
        Advances to the next sample in the dataset.

        This method saves the scores of the current sample, increments the current index,
        and displays the next sample. If the current index exceeds the length of the data,
        it is reset to the last valid index.
        """
        self.save_scores()  # Save current sample's scores
        self.current_index += 1
        if self.current_index >= len(self.data):
            self.current_index = len(self.data) - 1
        self.display_sample()

    def previous_sample(self):
        """
        Navigate to the previous sample in the dataset.

        This method decreases the current sample index by one and updates the display
        to show the previous sample. If the current sample is the first one, it will 
        display an informational message and keep the index at zero. Before navigating 
        to the previous sample, it saves the scores of the current sample.

        Returns:
            None
        """
        self.save_scores()  # Save current sample's scores
        self.current_index -= 1
        if self.current_index < 0:
            self.current_index = 0
            messagebox.showinfo("Info", "This is the first sample.")
        self.display_sample()

    def save_scores_to_file(self):
        """
        Prompts the user to select a location and filename to save the scores as a JSON file.
        
        Uses a file dialog to ask the user for a save location and filename with a .json extension.
        If a valid file path is provided, the method writes the scores to the specified file in JSON format.
        Displays a message box to inform the user that the scores have been saved successfully.
        
        Returns:
            None
        """
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(self.scores, f, indent=4)
            messagebox.showinfo("Info", "Scores saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeEvaluationApp(root)
    root.mainloop()
