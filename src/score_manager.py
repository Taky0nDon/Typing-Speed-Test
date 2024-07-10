class ScoreManager:
    def __init__(self) -> None:
       self.missed = 0
       self.correct = 0

    def increase_missed(self):
        self.missed += 1

    def increase_correct(self):
        self.correct += 1
