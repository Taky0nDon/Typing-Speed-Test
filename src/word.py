import tkinter as tk
from pathlib import Path
from os import getcwd
from tkinter import ttk


WORD_FILE_PATH = Path(Path(getcwd()).parent/'assets/words.txt')
class Word:
    def __init__(self, frame: ttk.Frame, word: str) -> None:
        self.word_value = word.lower()
        self.word_label = tk.Label(frame, text=self.word_value)
        self.word_label.configure(foreground="black")


    @staticmethod
    def recolor_word(word_list: list['Word'], word_index: int, new_color: str):
        word_list[word_index].word_label.configure(foreground=new_color)


    @staticmethod
    def generate_words() -> list[str]:
        """ Returns a list of random words chosen from the word file"""
        with open(WORD_FILE_PATH) as words:
            word_pool = words.read().strip().split("\n")
        return word_pool




