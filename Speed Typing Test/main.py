import tkinter as tk
import time
import threading
import random

class TypeSpeedGUI :

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Typing Speed Application")
        self.root.geometry("800x600")

        # Load the texts from file and split by newline
        self.texts = open("texts.txt", "r").read().split("\n")

        self.frame = tk.Frame(self.root)

        # Display the random sample text
        self.sample_label = tk.Label(self.frame, text = random.choice(self.texts), font = ("Helvetica", 18))
        self.sample_label.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 10)

        # Input field for user typing
        self.input_entry = tk.Entry(self.frame, width = 40, font = ("Helvetica", 24))
        self.input_entry.grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 10)
        self.input_entry.bind("<KeyRelease>", self.start)

        # Label to display speed stats
        self.speed_label = tk.Label(self.frame, text = "Speed : \n0.00 CPS \n0.00 CPM\n0.00 WPS\n0.00 WPM", font=("Helvetica", 18))
        self.speed_label.grid(row = 2, column = 0, columnspan = 2, padx = 5, pady = 10)

        # Label to display accuracy
        self.accuracy_label = tk.Label(self.frame, text = "Accuracy: 0.00%", font=("Helvetica", 18))
        self.accuracy_label.grid(row = 3, column = 0, columnspan = 2, padx = 5, pady = 10)

        # Reset button
        self.reset_button = tk.Button(self.frame, text = "Reset", command = self.reset, font=("Helvetica", 24))
        self.reset_button.grid(row = 4, column = 0, columnspan = 2, padx = 5, pady = 10)

        self.frame.pack(expand = True)

        self.counter = 0               # Timer counter
        self.running = False           # Timer state

        self.root.mainloop()

    def start(self, event):
        # Start timing on first valid key
        if not self.running:
            if not event.keycode in [16, 17, 18]:  # Ignore Shift, Ctrl, Alt
                self.running = True
                t = threading.Thread(target = self.time_thread)
                t.start()

        # Compare typed input with sample text
        if not self.sample_label.cget('text').startswith(self.input_entry.get()):
            self.input_entry.config(fg = "red")  # Incorrect so far
        else :
            self.input_entry.config(fg = "black")  # Correct so far

        # If the input matches the text (minus newline at end), stop timing
        if self.input_entry.get() == self.sample_label.cget('text')[:-1]:
            self.running = False
            self.input_entry.config(fg = "green")  # Completed text

    def time_thread(self):
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1

            typed = self.input_entry.get()
            sample = self.sample_label.cget('text')

            # Calculate correct characters
            correct_chars = 0
            for i in range(min(len(typed), len(sample))):
                if typed[i] == sample[i]:
                    correct_chars += 1

            # Avoid division by zero
            accuracy = (correct_chars / len(typed) * 100) if typed else 0.0

            # Typing speed calculations
            cps = len(typed) / self.counter
            cpm = cps * 60
            wps = len(typed.split(" ")) / self.counter
            wpm = wps * 60

            # Update GUI
            self.speed_label.config(text = f"Speed : \n{cps:.2f} CPS\n{cpm:.2f} CPM\n{wps:.2f} WPS\n{wpm:.2f} WPM")
            self.accuracy_label.config(text = f"Accuracy: {accuracy:.2f}%")

    def reset(self):
        # Reset all stats and input
        self.running = False
        self.counter = 0
        self.speed_label.config(text = "Speed : \n0.00 CPS \n0.00 CPM\n0.00 WPS\n0.00 WPM")
        self.accuracy_label.config(text = "Accuracy: 0.00%")
        self.sample_label.config(text = random.choice(self.texts))
        self.input_entry.delete(0, tk.END)

# Run the app
TypeSpeedGUI()
