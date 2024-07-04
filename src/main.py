from tkinter import ttk
from time import sleep

from word import Word, WordManager
from gui import Layout
from score_manager import ScoreManager



def main() -> None:
    gui = Layout(ScoreManager(),
                 WordManager())
         


if __name__ == "__main__":
    main()










