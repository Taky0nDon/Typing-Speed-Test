import tkinter as tk
from tkinter import ttk, StringVar
from random import choice

from word import Word, WordManager
from score_manager import ScoreManager


from test_helpers import get_widget_width, get_widget_height


class Layout:
    def __init__(self,
                 score_mgr: ScoreManager,
                 word_mgr: WordManager) -> None:
        self.score_mgmt = score_mgr
        self.word_mgmt = word_mgr
        self.create_root_window()
        self.textbox_start_offset_int=0
        self.create_widgets()
        self.initialize_score()
        self.configure_grid()
        self.root.mainloop()


    def create_root_window(self):
        self.root = tk.Tk()
        self.root.title("Typing Speed Test")

    def create_widgets(self):
        self.word_frame = ttk.Frame(self.root)
        self.show_word_box(self.word_mgmt.word_value_list)
        self.typing_frame = ttk.Frame(self.root)
        self.typing_box = tk.Text(self.typing_frame,
                                  height=10,
                                  width=50)
        self.typing_box.bind("<space>", self.on_space)
        self.exit_button = ttk.Button(self.root, text="Quit", command=exit)


    def configure_grid(self) -> None:
        self.root.grid_columnconfigure(0, weight=1)
        self.word_frame.grid(column=0, row=0)
        self.typing_frame.grid(column=0, row=1)
        self.typing_box.grid(column=1, row=1, columnspan=3)

        self.score_frame.grid(column=1, row=0) 
        self.missed_label.grid(column=0, row=0)
        self.correct_label.grid(column=0, row=1)
        self.missed_count.grid(column=1, row=0)
        self.accurate_count.grid(column=1, row=1)

        self.exit_button.grid(column=0, row=2)


    def get_window_width(self):
        self.root.update()
        print(f"window width: {self.root.winfo_width()}")


    def initialize_score(self):
        self.score_frame = ttk.Frame(self.root)
        self.missed_label = ttk.Label(self.score_frame, text="Missed: ")
        self.correct_label = ttk.Label(self.score_frame, text="Correct: ")
        self.missed_count = ttk.Label(self.score_frame, text=self.score_mgmt.missed)
        self.accurate_count = ttk.Label(self.score_frame, text=self.score_mgmt.correct)


    def on_space(self, event):
        word_index = self.word_mgmt.current_word_index
        current_word_val = self.word_mgmt.word_objects[word_index].word_value
        self.textbox_start_position = f"1.{self.textbox_start_offset_int}"
        if event.keysym == "space":
            if word_index < len(self.word_mgmt.word_objects) - 1:
                self.word_mgmt.recolor_word(self.word_mgmt.word_objects,
                                            self.word_mgmt.current_word_index+1,
                                            "white")
            else:
                pass # End the test.
            last_typed_word = self.typing_box.get(self.textbox_start_position,tk.END).strip()
            self.textbox_start_offset_int += len(last_typed_word) + 1
            print(f"_{last_typed_word}_")
            print(f"{self.textbox_start_offset_int}")
            print(f"{self.textbox_start_position=}")
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

    def update_score(self):
        self.missed_count.configure(text=self.score_mgmt.missed)
        self.accurate_count.configure(text=self.score_mgmt.correct)



