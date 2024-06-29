from tkinter import ttk
from time import sleep

from word import Word
from gui import Layout



RANDOM_WORDS = Word.generate_words()
def detect_typed_word(textbox: ttk.Entry, wordlist: list[str]) -> str:
    content = typing_box.get()
    words = content.strip().split(" ")
    wordlist.append(words[-1])
    return wordlist[-1]


def main() -> None:
    gui = Layout()
         


if __name__ == "__main__":
    main()










