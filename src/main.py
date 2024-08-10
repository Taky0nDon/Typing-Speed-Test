from time import time

from gui import Layout


#TODO: Make test length on optional terminal argument
TEST_LENGTH_MS = 60000


gui = Layout(TEST_LENGTH_MS)


def main() -> None:
    gui.begin_countdown()
    gui.root.after(TEST_LENGTH_MS, gui.terminate_grid)
    gui.root.mainloop()


if __name__ == "__main__":
    main()
