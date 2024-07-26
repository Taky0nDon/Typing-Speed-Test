from collections.abc import Callable
import tkinter as tk
from tkinter import ttk
from random import choice

from word import Word, WordManager
from score_manager import ScoreManager


from readonlytext import ReadonlyText


class Layout:
    """
    Class containing tkinter layout logic.
    Parameters:
        score_mgr : A ScoreManager object that handles keeping track of and
        calculate various statistics related to the user's performance
        word_mgr; A WordManager object responsible for creating Word objects
        managing their state, and generating a list of random words
        test_length: An int; the length of the test in milliseconds
        out of time, or the user typing all the displayed words
    """
    def __init__(
        self,
        score_mgr: ScoreManager,
        word_mgr: WordManager,
        test_length: int,
    ) -> None:
        self.score_mgmt = score_mgr()
        self.word_mgmt = word_mgr()
        self.test_length_sec = test_length / 1000
        self.seconds_remaining = self.test_length_sec
        self.textbox_start_offset_int = 0
        self.create_root_window()
        self.create_widgets(is_new_test=False)
        self.configure_grid()

    def create_root_window(self):
        """ Creates the root tkinter window """
        self.root = tk.Tk()
        self.root.title("Typing Speed Test")

    def create_widgets(self, is_new_test):
        """ Creates all the widgets used in the test GUI """
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
        self.render_score(is_new_test=is_new_test)

    def configure_grid(self) -> None:
        """ Places all widgets in the grid for the testing state """
        self.root.grid_columnconfigure(0, weight=1)
        self.word_frame.grid(column=0, row=0)
        self.countdown_frame.grid(column=0, row=0, sticky="W")
        self.typing_frame.grid(column=0, row=1)
        self.typing_box.grid(column=1, row=1, columnspan=3)
        self.countdown_label.grid(column=0, row=3)
        self.exit_button.grid(column=0, row=2)
        self.configure_grid_score(frame_pos=(2, 0))

    def configure_grid_score(self,
                             frame_pos: tuple[int, int],
                             ):
        self.score_frame.grid(column=frame_pos[0], row=frame_pos[1])
        self.missed_word_label.grid(column=0, row=0)
        self.correct_word_label.grid(column=0, row=1)
        self.error_label.grid(column=0, row=2)
        self.chars_label.grid(column=0, row=3)
        self.missed_word_count.grid(column=1, row=0)
        self.accurate_word_count.grid(column=1, row=1)
        self.error_count.grid(column=1, row=2)
        self.chars_count.grid(column=1, row=3)

    def decrement_countdown(self):
        """ Decreases countdown label by 1 every 1000ms """
        self.seconds_remaining -= 1
        self.countdown_label.configure(text=f"{self.seconds_remaining} sec")
        if self.seconds_remaining == 50:
            self.terminate_grid()
        self.root.after(1000, self.decrement_countdown)

    def render_score(self, is_new_test: bool):
        """
        Creates the frame containing all widgets related to displaying the
        score. Displays final score for end of state, and 0's for new tests.
        """
        self.score_frame = ttk.Frame(self.root)
        if is_new_test:
            scores = {
                    "missed_words": 0,
                    "correct_words": 0,
                    "missed_chars": 0,
                    "typed_chars": 0,
                    }
        else:
            scores = {
                    "missed_words": self.score_mgmt.missed_words,
                    "correct_words": self.score_mgmt.correct_words,
                    "missed_chars": self.score_mgmt.missed_chars,
                    "typed_chars": self.score_mgmt.typed_chars,
                    }
        self.missed_word_label = ttk.Label(self.score_frame, text="Missed: ")
        self.correct_word_label = ttk.Label(self.score_frame, text="Correct: ")
        self.error_label = ttk.Label(self.score_frame, text="Errors: ")
        self.chars_label = ttk.Label(self.score_frame, text="Typed: ")
        self.missed_word_count = ttk.Label(self.score_frame,
                                           text=scores["missed_words"])
        self.accurate_word_count = ttk.Label(self.score_frame,
                                             text=scores["correct_words"])
        self.error_count = ttk.Label(self.score_frame,
                                     text=scores["missed_chars"])
        self.chars_count = ttk.Label(self.score_frame,
                                     text=scores["typed_chars"])

    def on_space(self, *args):
        """
        Function called every time the user hits a space (representing the end
        of a word). It keeps tracks of offset into the text box where the user
        last hit space. The characters between the last 2 spaces are compared
        to the current word in the word box in order to determine whether it 
        was typed correctly.
        """
        word_index = self.word_mgmt.current_word_index
        current_word_val = self.word_mgmt.word_objects[word_index].word_value
        self.textbox_start_position = f"1.{self.textbox_start_offset_int}"
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
        """
        Renders a grid of Word objects, this is the text the user will be
        typing during the test.
        """
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

    def terminate_grid(self):
        for child in self.root.winfo_children():
            child.grid_remove()
        self.show_end_screen()

    def restart_test(self):
        for child in self.root.winfo_children():
            child.grid_remove()
        self.seconds_remaining = self.test_length_sec
        self.create_widgets(is_new_test=True)
        self.configure_grid()

    def show_end_screen(self):
        self.end_options_frame = ttk.Frame(self.root)
        self.end_options_frame.grid(column=0, row=1)
        restart_button = ttk.Button(self.end_options_frame, text="restart", command=self.restart_test)
        self.exit_button = ttk.Button(self.end_options_frame, text="Quit", command=exit)
        restart_button.grid(column=0, row=1)
        self.exit_button.grid(column=0, row=2)
        self.configure_grid_score(frame_pos=(0,0))


    def update_score(self):
        """ Displays up to date statistics as the user types """
        self.missed_word_count.configure(text=self.score_mgmt.missed_words)
        self.accurate_word_count.configure(text=self.score_mgmt.correct_words)
        self.error_count.configure(text=self.score_mgmt.missed_chars)
        self.chars_count.configure(text=self.score_mgmt.typed_chars)
