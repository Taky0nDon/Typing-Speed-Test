import tkinter as tk
from random import choice
from tkinter import ttk


class Word:
    def __init__(self, frame: ttk.Frame, word: str) -> None:
        self.word = word
        self.word_label = tk.Label(frame, text=self.word)


root = tk.Tk()
root.title("Typing Speed Test")

wordframe = ttk.Frame(root)
textbox_frame = ttk.Frame(root)

wordframe.grid(column=0, row=0)
textbox_frame.grid(column=0, row=1)

with open("../assets/words.txt") as words:
    word_pool = words.read().strip().split("\n")
col = 0
row = 0
for _ in range(50):
    current_word = choice(word_pool)
    some_word = Word(wordframe, current_word)
    if _ % 5 == 0 and _ > 0:
        row += 1
        col = 0
    some_word.word_label.grid(column=col, row=row)
    col += 1

typing_box_label = ttk.Label(textbox_frame, text="Start typing!")
typing_box = ttk.Entry(textbox_frame)

typing_box_label.grid(column=0, row=0)
typing_box.grid(column=1, row=1)

exit_button = ttk.Button(root, text="Quit", command=exit)
exit_button.grid(column=0, row=2)

root.mainloop()

