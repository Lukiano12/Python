import tkinter as tk
import time
import random
from tkinter import messagebox

class ReactionTimeTest:
    def __init__(self, master):
        self.master = master
        self.master.title("Reaction Time Test")
        self.master.geometry("600x400")
        self.state = 'start'  # Possible states: start, wait, go
        self.click_count = 0
        self.times = []
        self.start_time = 0

        self.label = tk.Label(master, text="Click to Start", font=("Helvetica", 24))
        self.label.pack(expand=True, fill='both')

        self.master.configure(bg='grey')
        self.label.configure(bg='grey')

        self.master.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        if self.state == 'start':
            self.start_test()
        elif self.state == 'go':
            self.record_reaction()
        elif self.state == 'wait':
            self.too_soon()

    def start_test(self):
        self.state = 'wait'
        self.master.configure(bg='red')
        self.label.configure(bg='red')
        self.label.config(text="Wait for Green...")
        wait_time = random.uniform(2, 5)  # Wait between 2 to 5 seconds
        self.master.after(int(wait_time * 1000), self.change_to_green)

    def change_to_green(self):
        self.state = 'go'
        self.master.configure(bg='green')
        self.label.configure(bg='green')
        self.label.config(text="Click now!")
        self.start_time = time.time()

    def record_reaction(self):
        reaction_time = (time.time() - self.start_time) * 1000  # in milliseconds
        self.times.append(reaction_time)
        self.click_count += 1
        if self.click_count < 5:
            self.reset_test()
        else:
            self.show_results()

    def too_soon(self):
        messagebox.showinfo("Too Soon!", "You clicked too soon! Wait for green.")
        self.reset_test()

    def reset_test(self):
        self.state = 'start'
        self.master.configure(bg='grey')
        self.label.configure(bg='grey')
        self.label.config(text="Click to Start")

    def show_results(self):
        average = sum(self.times) / len(self.times)
        results = "\n".join([f"Attempt {i+1}: {t:.2f} ms" for i, t in enumerate(self.times)])
        message = f"Your Reaction Times:\n{results}\n\nAverage Reaction Time: {average:.2f} ms"
        messagebox.showinfo("Results", message)
        self.master.quit()

def main():
    root = tk.Tk()
    app = ReactionTimeTest(root)
    root.mainloop()

if __name__ == "__main__":
    main()
