import tkinter as tk
from pathlib import Path
from os import getcwd
from tkinter import ttk


WORD_FILE = Path(Path(getcwd()).parent/'assets/words.txt')
class Word:
    def __init__(self, frame: ttk.Frame, word: str) -> None:
        self.word = word.lower()
        self.word_label = tk.Label(frame, text=self.word)
        self.word_label.configure(foreground="black")


    @staticmethod
    def generate_words() -> list[str]:
        with open(WORD_FILE) as words:
            word_pool = words.read().strip().split("\n")
        return word_pool




