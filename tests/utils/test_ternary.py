from tic_tac_toe.utils.ternary import (
    Ternary,
    convert_decimal_to_ternary,
    convert_game_to_ternary,
    convert_ternary_to_x_o,
)


def test_convert_decimal_to_ternary():
    ternary_number = convert_decimal_to_ternary(10)

    assert ternary_number.number == "000000101"
    assert ternary_number.decimal == 10
    assert isinstance(ternary_number, Ternary)


def test_convert_game_to_ternary():
    game = "03128"
    assert convert_game_to_ternary(game).number == "221100002"


def test_convert_ternary_to_x_o():
    ternary_number = Ternary("221100002")
    assert convert_ternary_to_x_o(ternary_number) == ["X", "X", "O", "O", " ", " ", " ", " ", "X"]
