from enum import Enum

class EnumTrainPrice(Enum):
    OPEN = 2
    HIGH = 3
    LOW = 4
    CLOSE = 5
    VOLUME = 6

    def __int__(self):
        return self.value