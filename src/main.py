import tkinter as tk
from random import choice
from tkinter import ttk


class Word:
    def __init__(self, frame: ttk.Frame, word: str) -> None:
        self.label_content = word
        self.word = tk.Label(frame, text=self.label_content)


root = tk.Tk()
root.title("Typing Speed Test")

mainframe = ttk.Frame(root)
wordframe = ttk.Frame(mainframe)

mainframe.grid(column=0, row=0)
with open("../assets/words.txt") as words:
    word_pool = words.read().strip().split("\n")
col = 0
row = 0
for _ in range(50):
    current_word = choice(word_pool)
    some_word = Word(mainframe, current_word)
    if _ % 5 == 0 and _ > 0:
        row += 1
        col = 0
    some_word.word.grid(column=col, row=row)
    col += 1

root.mainloop()

