from typing import Optional, List


class Ternary:
    def __init__(self, number: int, decimal: Optional[int] = None) -> None:
        self.number = number
        self.decimal = decimal or int(str(number), 3)

    def __repr__(self) -> str:
        return str(self.number)


def convert_decimal_to_ternary(decimal_number: int) -> Ternary:
    def _convert(d: int) -> str:
        quotient = d / 3
        remainder = d % 3
        if quotient == 0:
            return ""
        else:
            return _convert(int(quotient)) + str(int(remainder))

    ternary_number = int(_convert(decimal_number))

    return Ternary(ternary_number, decimal_number)


def convert_game_to_ternary(game: str) -> Ternary:
    number = ["0"] * 9

    for i, s in enumerate(game):
        # Even positions are X's turns (2), odd are O's (1)
        number[int(s)] = str(((i + 1) % 2) + 1)

    return Ternary(int("".join(number)))


def convert_ternary_to_x_o(ternary_number: Ternary) -> List[str]:
    mapping = {"0": " ", "1": "O", "2": "X"}
    return [mapping[m] for m in str(ternary_number.number)]
