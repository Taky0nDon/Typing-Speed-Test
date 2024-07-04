import tkinter as tk
from tkinter import ttk, StringVar
from random import choice
from time import sleep

from word import Word, WordManager
from score_manager import ScoreManager



class Layout:
    def __init__(self,
                 score_mgr: ScoreManager,
                 word_mgr: WordManager) -> None:
        self.score_mgmt = score_mgr
        self.word_mgmt = word_mgr
        self.root = tk.Tk()
        self.root.title("Typing Speed Test")
        self.word_frame = ttk.Frame(self.root)
        self.typing_frame = ttk.Frame(self.root)
        self.user_input = StringVar()
        self.typing_box_label = ttk.Label(self.typing_frame, text="Start typing!")
        self.typing_box_entry = ttk.Entry(self.typing_frame, textvariable=self.user_input)
        self.typing_box_entry.bind("<space>", self.on_space)
        self.exit_button = ttk.Button(self.root, text="Quit", command=exit)
        self.initialize_score()
        self.configure_grid()
        self.show_word_box(self.word_mgmt.word_value_list)
        self.root.mainloop()


    def initialize_score(self):
        self.score_frame = ttk.Frame(self.root)
        self.missed_label = ttk.Label(self.score_frame, text="Missed: ")
        self.correct_label = ttk.Label(self.score_frame, text="Correct: ")
        self.missed_count = ttk.Label(self.score_frame, text=self.score_mgmt.missed)
        self.accurate_count = ttk.Label(self.score_frame, text=self.score_mgmt.correct)

    def update_score(self):
        self.missed_count.configure(text=self.score_mgmt.missed)
        self.accurate_count.configure(text=self.score_mgmt.correct)


    def on_space(self, event):
        word_index = self.word_mgmt.current_word_index
        current_word_val = self.word_mgmt.word_objects[word_index].word_value
        if event.keysym == "space":
            if word_index < len(self.word_mgmt.word_objects) - 1:
                self.word_mgmt.recolor_word(self.word_mgmt.word_objects,
                                            self.word_mgmt.current_word_index+1,
                                            "white")
            else:
                pass # End the test.
            last_typed_word = self.user_input.get().split(' ')[-1]
            if current_word_val == last_typed_word:
                self.word_mgmt.recolor_word(self.word_mgmt.word_objects,
                                            self.word_mgmt.current_word_index,
                                            "green")
                self.score_mgmt.increase_correct()
            else:
                self.score_mgmt.increase_missed()
                self.word_mgmt.recolor_word(self.word_mgmt.word_objects,
                                            self.word_mgmt.current_word_index, 
                                            "red")
            self.word_mgmt.current_word_index +=1     
            self.update_score()



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
            self.word_mgmt.word_objects.append(some_word)
            col += 1
        self.word_mgmt.recolor_word(self.word_mgmt.word_objects,
                                    self.word_mgmt.current_word_index,
                                    "white")

    def configure_grid(self) -> None:
        self.word_frame.grid(column=0, row=0)
        self.typing_frame.grid(column=0, row=1)
        self.typing_box_label.grid(column=0, row=0)
        self.typing_box_entry.grid(column=1, row=1)

        self.score_frame.grid(column=1, row=0)
        self.missed_label.grid(column=0, row=0)
        self.correct_label.grid(column=0, row=1)
        self.missed_count.grid(column=1, row=0)
        self.accurate_count.grid(column=1, row=1)

        self.exit_button.grid(column=0, row=2)
