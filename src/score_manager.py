from os import stat


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
        if self.typed_chars > 0:
            self.accuracy = f"{(self.correct_chars / self.typed_chars) * 100:.2f}%"
            return self.accuracy
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
                self.missed_chars += 1
            else:
                self.correct_chars += 1
            idx +=1 

        self.missed_chars += len_difference

    def update_typed_chars(self, typed_content: str) -> int:
        self.typed_chars = len(typed_content)
        return len(typed_content)

    def calculate_gross_wpm(self, length_of_time_ms: int) -> float:
        print(f"{length_of_time_ms=}")
        print(f"{self.typed_chars=}")
        length_of_time_min = (length_of_time_ms) / (10**3 * 60)
        wpm = ((self.typed_chars / 5) / length_of_time_min)
        print(f"{length_of_time_min=}")
        print(f"{wpm=}")
        return wpm

    def count_errors(self, target_words: list[str], typed_words: list[str]) -> int:
        errors = 0
        word_pairs = zip(target_words, typed_words)
        print(f"{target_words=}")
        for pair in word_pairs:
            sorted_by_len = [
                    (word, len(word)) for word in sorted(pair, key=lambda x: len(x))
                    ]
            if len(sorted_by_len) > 1:
                longer_word = sorted_by_len[1][0]
                shorter_word = sorted_by_len[0][0]
                errors += sorted_by_len[1][1] - sorted_by_len[0][1]
                for i, char in enumerate(shorter_word):
                    conjugate_char = longer_word[i]
                    if char != conjugate_char:
                        errors += 1
            print(f"{pair=},\n{sorted_by_len=}\n{errors=}")
        return errors
