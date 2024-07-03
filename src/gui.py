import tkinter as tk
from tkinter import ttk, StringVar
from random import choice
from time import sleep

from word import Word




class Layout:
    def __init__(self, word_list: list[str]) -> None:
        self.root = tk.Tk()
        self.root.title("Typing Speed Test")
        self.current_word_index = 0
        self.fails = 0
        #self.words = self.generate_word_list
        self.words: list[Word]= []
        self.word_frame = ttk.Frame(self.root)
        self.typing_frame = ttk.Frame(self.root)
        self.user_input = StringVar()
        self.typing_box_label = ttk.Label(self.typing_frame, text="Start typing!")
        self.typing_box_entry = ttk.Entry(self.typing_frame, textvariable=self.user_input)
        self.exit_button = ttk.Button(self.root, text="Quit", command=exit)
        self.score_counter()
        self.configure_grid()
        self.show_word_box(word_list)
        self.configure_word_box()
        self.configure_text_entry_box()
        self.root.mainloop()

    def configure_word_box(self):
        Word.recolor_word(self.words, self.current_word_index, "white")

    def score_counter(self):
        self.score_frame = ttk.Frame(self.root)
        self.missed_label = ttk.Label(self.score_frame, text="Missed: ")
        self.correct_label = ttk.Label(self.score_frame, text="Correct: ")

    def configure_text_entry_box(self):
        self.typing_box_entry.bind("<KeyPress>", self.on_space)

    def on_space(self, event):
        current_word_val = self.words[self.current_word_index].word_value
        if event.keysym == "space":
            if self.current_word_index < len(self.words) - 1:
                Word.recolor_word(self.words, self.current_word_index+1, "white")
            else:
                pass # End the test.
            last_typed_word = self.user_input.get().split(' ')[-1]
            if current_word_val == last_typed_word:
                Word.recolor_word(self.words, self.current_word_index, "green")
            else:
                self.fails += 1
                Word.recolor_word(self.words, self.current_word_index, "red")
            self.current_word_index +=1 



    def show_word_box(self, word_bank) -> None:
        row = 0
        col = 0
        for _ in range(50):
            current_word_value = choice(word_bank)
            some_word = Word(self.word_frame, current_word_value)
            if _ % 5 == 0 and _ > 0:
                row += 1
                col = 0
            some_word.word_label.grid(column=col, row=row)
            col += 1
            self.words.append(some_word)


    def configure_grid(self) -> None:
        self.word_frame.grid(column=0, row=0)
        self.typing_frame.grid(column=0, row=1)
        self.score_frame.grid(column=1, row=0)
        self.missed_label.grid(column=0, row=0)
        self.correct_label.grid(column=0, row=1)
        self.exit_button.grid(column=0, row=2)
        self.typing_box_label.grid(column=0, row=0)
        self.typing_box_entry.grid(column=1, row=1)
