class Countdown:
    def __init__(self, time_sec: int):
        self.starting_value = time_sec
        self.seconds_remaining = time_sec

    def decrement_countdown(self):
        self.seconds_remaining -= 1
