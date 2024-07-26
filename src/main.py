from gui import Layout
from score_manager import ScoreManager
from word import WordManager


TEST_LENGTH_MS = 60000


gui = Layout(ScoreManager, WordManager, TEST_LENGTH_MS)


def main() -> None:
    gui.root.after(1000, gui.decrement_countdown)
    gui.root.after(TEST_LENGTH_MS, gui.terminate_grid)
    gui.root.mainloop()


if __name__ == "__main__":
    main()
