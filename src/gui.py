import tkinter as tk
from time import time
from tkinter import ttk
from random import choice

from word import Word, WordManager
from score_manager import ScoreManager
from CountdownManager import Countdown


from readonlytext import ReadonlyText


class Layout:
    """
    Class containing tkinter layout logic.
    """

    def __init__(self, test_length_ms: int) -> None:
        """
        Parameters:
        test_length: An int; the length of the test in milliseconds
        out of time, or the user typing all the displayed words
        """
        self.score_mgmt = ScoreManager()
        self.word_mgmt = WordManager()
        self.countdown = Countdown(test_length_ms // 1000)
        self.tick_length = 1000
        self.textbox_start_offset_int = 0
        self.test_length_ms = test_length_ms
        self.create_root_window()
        self.create_widgets(is_new_test=False)
        self.configure_grid()

    def create_root_window(self):
        """Creates the root tkinter window"""
        self.root = tk.Tk()
        self.root.title("Typing Speed Test")

    def create_widgets(self, is_new_test):
        """Creates all the widgets used in the test GUI"""
        self.word_frame = ttk.Frame(self.root)
        self.countdown_frame = ttk.Frame(self.root)
        self.typing_frame = ttk.Frame(self.root)
        self.countdown_label = ttk.Label(
            self.countdown_frame, text=f"{self.countdown.seconds_remaining} sec"
        )
        self.typing_box = ReadonlyText(self.typing_frame, height=10, width=50)
        self.typing_box.bind("<space>", self.on_space)
        self.exit_button = ttk.Button(self.root, text="Quit", command=exit)
        self.render_score(is_new_test=is_new_test)
        self.show_word_box()

        self.end_options_frame = ttk.Frame(self.root)
        self.final_results_frame = ttk.Frame(self.root)
        self.accuracy_label = ttk.Label(
            self.final_results_frame, text=f"Accuracy: {self.score_mgmt.accuracy}"
        )
        self.restart_button = ttk.Button(
            self.end_options_frame, text="restart", command=self.restart_test
        )
        self.exit_button = ttk.Button(self.root, text="Quit", command=exit)
        self.wpm_label = ttk.Label(self.final_results_frame, text="wpm")

    def configure_grid(self) -> None:
        """Places all widgets in the grid for the testing state"""
        self.root.grid_columnconfigure(0, weight=1)
        self.word_frame.grid(column=0, row=0)
        self.countdown_frame.grid(column=0, row=0, sticky="W")
        self.typing_frame.grid(column=0, row=1)
        self.typing_box.grid(column=1, row=1, columnspan=3)
        self.countdown_label.grid(column=0, row=3)
        self.exit_button.grid(column=0, row=4)
        self.configure_grid_score(frame_pos=(2, 0))

    def configure_grid_score(
        self,
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

    def begin_countdown(self):
        """
        Function initiates the countdown if there is text in the box
        """
        if self.user_has_typed():
            self.tick()
        else:
            self.root.after(self.tick_length, self.begin_countdown)

    def user_has_typed(self) -> bool:
        self.box_content = self.typing_box.get(0.1, tk.END).strip("\n")
        text_in_box = len(self.box_content) > 0
        if text_in_box:
            self.start = time()
            return True
        return False

    def update_time_remaining(self):
        """Decreases countdown label by 1 every 1000ms"""
        self.countdown.decrement_countdown()
        self.countdown_label.configure(text=f"{self.countdown.seconds_remaining} sec")

    def tick(self) -> None:
        """
        Actions that occur every $self.tick_length ms
        """
        print(self.countdown.seconds_remaining)
        self.update_time_remaining()
        if self.countdown.seconds_remaining < 0:
            print(self.typing_box.get("1.0", tk.END))
            print(len(self.typing_box.get("1.0", tk.END)))
            self.score_mgmt.update_typed_chars(self.typing_box.get("1.0", tk.END))
            self.terminate_grid()
            self.show_end_screen()
        else:
            self.root.after(self.tick_length, self.tick)

    def update_score(self):
        """Displays up to date statistics as the user types"""
        self.missed_word_count.configure(text=self.score_mgmt.missed_words)
        self.accurate_word_count.configure(text=self.score_mgmt.correct_words)
        self.error_count.configure(text=self.score_mgmt.missed_chars)
        self.chars_count.configure(text=self.score_mgmt.typed_chars)

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
        self.missed_word_count = ttk.Label(
            self.score_frame, text=scores["missed_words"]
        )
        self.accurate_word_count = ttk.Label(
            self.score_frame, text=scores["correct_words"]
        )
        self.error_count = ttk.Label(self.score_frame, text=scores["missed_chars"])
        self.chars_count = ttk.Label(self.score_frame, text=scores["typed_chars"])

    def on_space(self, *args):
        """
        Function called every time the user hits a space (representing the end
        of a word). It keeps tracks of offset into the text box where the user
        last hit space. The characters between the last 2 spaces are compared
        to the current word in the word box in order to determine whether it
        was typed correctly.
        """
        target_word_index = self.word_mgmt.current_word_index
        target_word_val = self.word_mgmt.word_objects[target_word_index].word_value
        self.textbox_start_position = f"1.{self.textbox_start_offset_int}"
        if target_word_index < len(self.word_mgmt.word_objects) - 1:
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
        if target_word_val == last_typed_word:
            self.word_mgmt.recolor_word(
                self.word_mgmt.word_objects,
                self.word_mgmt.current_word_index,
                "green",
            )
            self.score_mgmt.increase_correct_count(last_typed_word)
        else:
            self.score_mgmt.increase_missed_count(
                target_word=target_word_val, typed_word=last_typed_word
            )
            self.word_mgmt.recolor_word(
                self.word_mgmt.word_objects,
                self.word_mgmt.current_word_index,
                "red",
            )
        self.word_mgmt.current_word_index += 1
        self.update_score()

    def show_word_box(self) -> None:
        """
        Renders a grid of Word objects, this is the text the user will be
        typing during the test.
        """
        row = 0
        col = 0
        the_words = self.word_mgmt.choose_random_words()
        for idx, word in enumerate(the_words):
            some_word = Word(self.word_frame, word)
            if idx % 5 == 0 and idx > 0:
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

    def restart_test(self):
        self.terminate_grid()
        self.countdown.seconds_remaining = self.countdown.starting_value
        self.create_widgets(is_new_test=True)
        self.configure_grid()
        self.begin_countdown()

    def show_end_screen(self):
        self.score_mgmt.count_errors(self.word_mgmt.word_list, self.typing_box.get("1.0", tk.END).split())

        self.chars_typed_label = ttk.Label(self.root, text=f"{self.score_mgmt.typed_chars} characters typed")
        self.final_results_frame.grid(column=0, row=0)
        self.end_options_frame.grid(column=0, row=1)
        self.accuracy_label.grid(column=0, row=0)
        self.wpm_label.configure(text=f"{self.score_mgmt.calculate_gross_wpm(self.test_length_ms)} wpm")
        self.wpm_label.grid(column=0, row=1)
        self.chars_typed_label.update()
        self.chars_typed_label.grid(column=0, row=2)
        self.restart_button.grid(column=0, row=0)
        self.exit_button.grid(column=0, row=3)
        # self.configure_grid_score(frame_pos=(0, 0))
