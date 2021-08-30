import numpy as np
from typing import Optional, List


class Ternary:
    def __init__(self, number: str, decimal: Optional[int] = None) -> None:
        if isinstance(number, int):
            number = int(number)

        self.number = "0" * (9 - len(number)) + number
        self.decimal = decimal or int(number, 3)

    def __repr__(self) -> str:
        return self.number

    def __sub__(self, other):
        a = np.array([int(i) for i in self.number])
        b = np.array([int(i) for i in other.number])
        diff = a - b

        return "".join([str(abs(i)) for i in diff])


def convert_decimal_to_ternary(decimal_number: int) -> Ternary:
    def _convert(d: int) -> str:
        quotient = d / 3
        remainder = d % 3
        if quotient == 0:
            return ""
        else:
            return _convert(int(quotient)) + str(int(remainder))

    ternary_number = _convert(decimal_number)

    return Ternary(ternary_number, decimal_number)


def convert_game_to_ternary(game: str) -> Ternary:
    number = ["0"] * 9

    for i, s in enumerate(game):
        # Even positions are X's turns (2), odd are O's (1)
        number[int(s)] = str(((i + 1) % 2) + 1)

    return Ternary("".join(number))


def convert_ternary_to_x_o(ternary_number: Ternary) -> List[str]:
    mapping = {"0": " ", "1": "O", "2": "X"}
    return [mapping[m] for m in str(ternary_number.number)]
