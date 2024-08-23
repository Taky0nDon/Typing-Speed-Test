import sys

from time import time

from gui import Layout


def main() -> None:
    if len(sys.argv) > 1:
        TEST_LENGTH_MS = int(sys.argv[1]) * 1000
    else:
        TEST_LENGTH_MS = 60 * 1000

    gui = Layout(TEST_LENGTH_MS)
    gui.begin_countdown()
    gui.root.mainloop()


if __name__ == "__main__":
    main()

