from tkinter import ttk
from time import sleep

from word import Word, WordManager
from gui import Layout
from score_manager import ScoreManager


def end_test():
    """This function is called when the test ends, either due to all words
    being typed, or time running out.
    """
    words_typed = score_manager.missed_words + score_manager.correct_words
    print(
        f"You typed {words_typed} "
        f"words! You missed {score_manager.missed_words} of them. Your score "
        f"is {round(score_manager.correct_words / words_typed, 2) * 100}%!"
    )


TEST_LENGTH_MS = 60000


score_manager = ScoreManager()
gui = Layout(score_manager, WordManager(), TEST_LENGTH_MS, end_test)


def main() -> None:
    gui.root.after(1000, gui.decrement_countdown)
    gui.root.after(TEST_LENGTH_MS, end_test)
    gui.root.mainloop()


if __name__ == "__main__":
    main()
