from collections.abc import Callable
import tkinter as tk
from tkinter import ttk
from random import choice

from word import Word, WordManager
from score_manager import ScoreManager


from readonlytext import ReadonlyText


class Layout:
    def __init__(
        self,
        score_mgr: ScoreManager,
        word_mgr: WordManager,
        test_length: int,
        end_func: Callable,
    ) -> None:
        self.score_mgmt = score_mgr
        self.end_test = end_func
        self.word_mgmt = word_mgr
        self.seconds_remaining = test_length / 1000
        self.create_root_window()
        self.textbox_start_offset_int = 0
        self.create_widgets()
        self.initialize_score()
        self.configure_grid()

    def create_root_window(self):
        self.root = tk.Tk()
        self.root.title("Typing Speed Test")

    def create_widgets(self):
        self.word_frame = ttk.Frame(self.root)
        self.show_word_box(self.word_mgmt.word_value_list)
        self.countdown_frame = ttk.Frame(self.root)
        self.typing_frame = ttk.Frame(self.root)
        self.countdown_label = ttk.Label(
            self.countdown_frame, text=f"{self.seconds_remaining} sec"
        )

        self.typing_box = ReadonlyText(self.typing_frame, height=10, width=50)
        self.typing_box.bind("<space>", self.on_space)
        self.exit_button = ttk.Button(self.root, text="Quit", command=exit)

    def configure_grid(self) -> None:
        self.root.grid_columnconfigure(0, weight=1)
        self.word_frame.grid(column=0, row=0)
        self.countdown_frame.grid(column=0, row=0, sticky="W")
        self.typing_frame.grid(column=0, row=1)
        self.score_frame.grid(column=1, row=0)

        self.typing_box.grid(column=1, row=1, columnspan=3)

        self.countdown_label.grid(column=0, row=3)

        self.missed_word_label.grid(column=0, row=0)
        self.correct_word_label.grid(column=0, row=1)
        self.error_label.grid(column=0, row=2)
        self.missed_word_count.grid(column=1, row=0)
        self.accurate_word_count.grid(column=1, row=1)
        self.error_count.grid(column=1, row=2)

        self.exit_button.grid(column=0, row=2)

    def decrement_countdown(self):
        self.seconds_remaining -= 1
        self.countdown_label.configure(text=f"{self.seconds_remaining} sec")
        if self.seconds_remaining == 0:
            self.end_test()
        self.root.after(1000, self.decrement_countdown)

    def get_window_width(self):
        self.root.update()

    def initialize_score(self):
        self.score_frame = ttk.Frame(self.root)
        self.missed_word_label = ttk.Label(self.score_frame, text="Missed: ")
        self.correct_word_label = ttk.Label(self.score_frame, text="Correct: ")
        self.error_label = ttk.Label(self.score_frame, text="Errors:")
        self.missed_word_count = ttk.Label(
            self.score_frame, text=self.score_mgmt.missed_words
        )
        self.accurate_word_count = ttk.Label(
            self.score_frame, text=self.score_mgmt.correct_words
        )
        self.error_count = ttk.Label(
            self.score_frame, text=self.score_mgmt.missed_chars
        )

    def on_space(self, event):
        word_index = self.word_mgmt.current_word_index
        current_word_val = self.word_mgmt.word_objects[word_index].word_value
        self.textbox_start_position = f"1.{self.textbox_start_offset_int}"
        cursor_min = None
        if event.keysym == "space":
            if word_index < len(self.word_mgmt.word_objects) - 1:
                self.word_mgmt.recolor_word(
                    self.word_mgmt.word_objects,
                    self.word_mgmt.current_word_index + 1,
                    "white",
                )
            else:
                print("You typed all the words!")
            last_typed_word = self.typing_box.get(
                self.textbox_start_position, tk.END
            ).strip()
            self.textbox_start_offset_int += len(last_typed_word) + 1
            if current_word_val == last_typed_word:
                self.word_mgmt.recolor_word(
                    self.word_mgmt.word_objects,
                    self.word_mgmt.current_word_index,
                    "green",
                )
                self.score_mgmt.increase_correct_count(last_typed_word)
            else:
                self.score_mgmt.increase_missed_count(
                    target_word=current_word_val, typed_word=last_typed_word
                )
                self.word_mgmt.recolor_word(
                    self.word_mgmt.word_objects,
                    self.word_mgmt.current_word_index,
                    "red",
                )
            self.word_mgmt.current_word_index += 1
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
        self.word_mgmt.recolor_word(
            self.word_mgmt.word_objects, self.word_mgmt.current_word_index, "white"
        )

    def update_score(self):
        self.missed_word_count.configure(text=self.score_mgmt.missed_words)
        self.accurate_word_count.configure(text=self.score_mgmt.correct_words)
        self.error_count.configure(text=self.score_mgmt.missed_chars)
