from typing import Union

from tic_tac_toe.utils.ternary import Ternary, convert_game_to_ternary, convert_ternary_to_x_o


def plot(game: Union[str, Ternary]) -> str:
    template = " {1} | {2} | {3} \n" "---+---+---\n" " {8} | {0} | {4} \n" "---+---+---\n" " {7} | {6} | {5} "

    if not isinstance(game, Ternary):
        board = convert_game_to_ternary(game)
    else:
        board = game

    x_o = convert_ternary_to_x_o(board)
    return template.format(*x_o)
