class ScoreManager:
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

    def increase_missed_count(self, target_word: str, typed_word: str):
        self.missed_words += 1
        self.calculate_char_errors(target=target_word, typed=typed_word)


    def increase_correct_count(self, typed_word: str):
        self.correct_words += 1
        self.correct_chars = len(typed_word) + 1  # Need to add 1  to account
                                                  # for space

    def calculate_char_errors(self, target: str='', typed: str='') -> None:
        """
        Calculates number of  incorrect characters typed by counting number of
        mismatched characters, and adding the difference in length of the strings.
        """
        if not target or not typed:
            return
        if len(typed) < len(target):
            base, other = typed, target
        else:
            base, other = target, target

        len_difference = len(other) - len(base)
        idx = 0
        for char in base:
            if char != other[idx]:
                self.missed_chars += 1
            idx +=1 

        self.missed_chars += len_difference

    def update_typed_chars(self, chars_typed: int) -> None:
        self.typed_chars = chars_typed

    def show_stats(self):
        """This function is called when the test ends, either due to all words
        being typed, or time running out.
        Parameters:
        """
        words_typed = self.missed_words + self.correct_words
        print(
            f"You typed {words_typed} "
            f"words! You missed {self.missed_words} of them. Your score "
            f"is {round(self.correct_words / words_typed, 2) * 100}%!"
        )


