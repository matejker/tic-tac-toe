from tic_tac_toe.game import whois_winner
from tic_tac_toe.utils.ternary import Ternary


def test_whois_winner():
    x_is_winner = Ternary("221002020")
    o_is_winner = Ternary("210202011")
    no_winner_yet = Ternary("210102020")
    draw = Ternary("221211211")

    assert whois_winner(x_is_winner) == 2
    assert whois_winner(o_is_winner) == 1
    assert whois_winner(draw) == 0
    assert whois_winner(no_winner_yet) == -1
