from abc import ABCMeta, abstractmethod
from typing import Tuple

CoordinateType = Tuple[int, int, int]


class Base(metaclass=ABCMeta):

    @abstractmethod
    def go(self):
        pass


    @property
    @abstractmethod
    def position(self) -> CoordinateType:
        """The current position, as a list"""

class Sangaboard(Base):
    def go(self):
        print("vroom vroom go....")
    def position(self):
        a = [0,0,0]
        return a

board = Sangaboard()
board.go
p = board.position()
print(p)