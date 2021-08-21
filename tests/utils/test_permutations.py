from tic_tac_toe.utils.ternary import Ternary
from tic_tac_toe.utils.permutations import get_all_symmetries_for_board


def test_get_all_symmetries_for_board():
    board = Ternary("221100002")
    symmetries = get_all_symmetries_for_board(board)
    expected_symmetries = {"200002112", "200022110", "200112200", "202211000", "210000221", "211220000", "222000011"}

    for s in symmetries:
        assert s.number in expected_symmetries
