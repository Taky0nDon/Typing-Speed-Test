import os
import tkinter as tk
from pathlib import Path
from os import getcwd
from tkinter import ttk
from random import choice


WORD_FILE_DIR = os.path.dirname(os.path.realpath(__file__))
WORD_FILE_PATH = Path(Path(WORD_FILE_DIR).parent/'assets/words.txt')
class Word:
    def __init__(self, frame: ttk.Frame, word: str) -> None:
        self.word_value = word.lower()
        self.word_label = tk.Label(frame, text=self.word_value)
        self.word_label.configure(foreground="black")

class WordManager():
    def __init__(self) -> None:
        self.word_value_list = self.generate_word_bank()
        self.current_word_index = 0
        self.word_objects = []

    def recolor_word(self,
                     word_list: list['Word'],
                     word_index: int,
                     new_color: str):
        """excepts a list of Word objects, the index of the Word to alter, and
        the new color for the Word foreground"""
        word_list[word_index].word_label.configure(foreground=new_color)


    def generate_word_bank(self) -> list[str]:
        """ Returns a list of random words chosen from the word file"""
        print("Generating word...")
        with open(WORD_FILE_PATH) as words:
            word_pool = words.read().strip().split("\n")
        print(f"{word_pool=}\n{type(word_pool)=}")
        return word_pool

    def choose_random_words(self, list_length=50) -> list[str]:
        random_words = []
        for _ in range(list_length):
            current_word = choice(self.generate_word_bank())
            random_words.append(current_word)
        return random_words




