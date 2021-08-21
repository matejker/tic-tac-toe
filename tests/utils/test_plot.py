from tic_tac_toe.utils.ternary import Ternary
from tic_tac_toe.utils.plot import plot


def test_plot():
    board_ternary = Ternary("210102020")
    game = "01735"

    expected_board = " O |   | O \n---+---+---\n   | X |   \n---+---+---\n X |   | X "

    assert plot(board_ternary) == expected_board
    assert plot(game) == expected_board
