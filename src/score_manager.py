class ScoreManager():
    """
    This class keeps track of how many words were typed correctly, and how
    many contained errors. It has methods for incrementing each count.
    """
    def __init__(self) -> None:
       self.missed_words = 0
       self.missed_chars = 0
       self.correct_words = 0
       self.correct_chars = 0
       self.typed_chars = 0
       self.accuracy = "0.00%"

    def update_accuracy(self) -> str:
        """
        Returns a float representing the number of correct characters divided
        by total characters
        """
        print("Updating accuracy...",
              f"{self.correct_chars=}, {self.typed_chars=}")
        self.accuracy = f"{(self.correct_chars / self.typed_chars) * 100:.2f}%"
        return self.accuracy

    def increase_missed_count(self, target_word: str, typed_word: str):
        self.missed_words += 1
        self.calculate_char_errors(target=target_word, typed=typed_word)

    def increase_correct_count(self, typed_word: str):
        self.correct_words += 1
        self.correct_chars += len(typed_word)

    def calculate_char_errors(self, target: str='', typed: str='') -> None:
        """
        Calculates number of  incorrect characters typed by counting number of
        mismatched characters, and adding the difference in length of the strings.
        """
        if not target or not typed:
            return
        if len(typed) < len(target):
            shorter, longer = typed, target
        else:
            shorter, longer = target, target

        len_difference = len(longer) - len(shorter)
        idx = 0
        for char in shorter:
            if char != longer[idx]:
                print("You missed.")
                self.missed_chars += 1
            else:
                print("here")
                self.correct_chars += 1
            idx +=1 

        self.missed_chars += len_difference

    def update_typed_chars(self, typed_content: str) -> None:
        self.typed_chars = len(typed_content.replace(" ", "").strip("\n"))

