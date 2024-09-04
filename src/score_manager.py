from os import stat


class ScoreManager():
    """
    This class keeps track of how many words were typed correctly, and how
    many contained errors. It has methods for incrementing each count.
    """
    def __init__(self) -> None:
       self.char_errors = 0
       self.typed_entries = 0
       self.accuracy = "0.00%"

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
                self.char_errors += 1
            idx +=1 

        self.char_errors += len_difference

    def update_typed_entries(self, typed_content: str) -> int:
        self.typed_entries = len(typed_content)
        return len(typed_content)

    def calculate_gross_wpm(self, time_ms: int) -> float:
        entries = self.typed_entries
        print(f"{time_ms=}")
        print(f"{self.typed_entries=}")
        length_of_time_min = (time_ms) / (10**3 * 60)
        words = entries / 5
        wpm = round((words / length_of_time_min), 2)
        print(f"{length_of_time_min=}")
        print(f" gross {wpm=:.2f}")
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
        self.char_errors = errors
        return errors

    def update_accuracy(self) -> float:
        print("HERE~!!!!!!!!!!")
        print(f"{self.char_errors=}, {self.typed_entries=}")
        correct_chars = self.typed_entries - self.char_errors
        accuracy = correct_chars / self.typed_entries
        accuracy_str = f"{accuracy: .2f}%"
        self.accuracy = accuracy_str
        return accuracy

