import tkinter as tk
from random import choice
from tkinter import StringVar, ttk


from word import Word

def detect_typed_word(textbox: ttk.Entry, wordlist: list[str]) -> str:
    content = typing_box.get()
    words = content.strip().split(" ")
    wordlist.append(words[-1])
    return wordlist[-1]


root = tk.Tk()
root.title("Typing Speed Test")

wordframe = ttk.Frame(root)
textbox_frame = ttk.Frame(root)

wordframe.grid(column=0, row=0)
textbox_frame.grid(column=0, row=1)

col = 0
row = 0
words_shown = []
words_typed = []
for _ in range(50):
    current_word = choice(Word.generate_words())
    some_word = Word(wordframe, current_word)
    words_shown.append(some_word)
    if _ % 5 == 0 and _ > 0:
        row += 1
        col = 0
    some_word.word_label.grid(column=col, row=row)
    col += 1

user_input = StringVar()

typing_box_label = ttk.Label(textbox_frame, text="Start typing!")
typing_box = ttk.Entry(textbox_frame, textvariable=user_input)

typing_box_label.grid(column=0, row=0)
typing_box.grid(column=1, row=1)

exit_button = ttk.Button(root, text="Quit", command=exit)
exit_button.grid(column=0, row=2)

print(typing_box.get())




root.mainloop()

