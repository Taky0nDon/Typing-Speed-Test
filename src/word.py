import os
import tkinter as tk
from pathlib import Path
from os import getcwd
from tkinter import ttk


WORD_FILE_DIR = os.path.dirname(os.path.realpath(__file__))
WORD_FILE_PATH = Path(Path(WORD_FILE_DIR).parent/'assets/words.txt')
class Word:
    def __init__(self, frame: ttk.Frame, word: str) -> None:
        self.word_value = word.lower()
        self.word_label = tk.Label(frame, text=self.word_value)
        self.word_label.configure(foreground="black")

class WordManager:
    def __init__(self) -> None:
        self.word_value_list = self.generate_words()
        self.current_word_index = 0
        self.word_objects = []

    def recolor_word(self,
                     word_list: list['Word'],
                     word_index: int,
                     new_color: str):
        """excepts a list of Word objects, the index of the Word to alter, and
        the new color for the Word foreground"""
        word_list[word_index].word_label.configure(foreground=new_color)


    def generate_words(self) -> list[str]:
        """ Returns a list of random words chosen from the word file"""
        with open(WORD_FILE_PATH) as words:
            word_pool = words.read().strip().split("\n")
        return word_pool




