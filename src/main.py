from tkinter import ttk
from time import sleep

from word import Word, WordManager
from gui import Layout
from score_manager import ScoreManager

TEST_LENGTH_MS = 10000


score_manager = ScoreManager()
gui = Layout(score_manager,
             WordManager()
             )

def end_test():
        words_typed = score_manager.missed + score_manager.correct
        print(f"You typed {words_typed} "
          f"words! You missed {score_manager.missed} of them. Your score " 
          f"is {round(score_manager.correct / words_typed, 2) * 100}%!"
          )

def main() -> None:
    gui.root.after(TEST_LENGTH_MS, end_test)
    gui.root.mainloop()
         


if __name__ == "__main__":
    main()










