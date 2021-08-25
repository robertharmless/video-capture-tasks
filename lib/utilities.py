"""
utility classes
"""
# Built-in
from datetime import datetime

# Special

# App


class Timer:
    """
    Simple way to measure time

    ''''
    __init__() -> start timer
    finished() -> end timer and return message

    """

    start = None
    end = None
    duration = None

    def __init__(self) -> None:
        self.start = datetime.now()

    def finished(self) -> str:
        self.end = datetime.now()
        self.duration = self.end - self.start

        message = f"Duration {str(self.duration).split('.')[0]}"
        print(message)

        return message
