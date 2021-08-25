from tic_tac_toe.utils.ternary import Ternary
from tic_tac_toe.utils.permutations import get_all_symmetries_for_board, whois_winner


def test_get_all_symmetries_for_board():
    board = "221100002"
    symmetries = get_all_symmetries_for_board(board)
    expected_symmetries = {
        "200001122",
        "200022110",
        "200112200",
        "202211000",
        "210000221",
        "211220000",
        "222000011",
        "221100002",
    }

    for s in symmetries:
        assert s in expected_symmetries


def test_whois_winner():
    x_is_winner = Ternary("221002020")
    o_is_winner = Ternary("210202011")
    no_winner_yet = Ternary("210102020")
    draw = Ternary("221211211")

    assert whois_winner(x_is_winner) == 2
    assert whois_winner(o_is_winner) == 1
    assert whois_winner(draw) == 0
    assert whois_winner(no_winner_yet) == -1
