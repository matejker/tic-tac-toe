from tic_tac_toe.utils.ternary import Ternary


def whois_winner(board: Ternary) -> int:
    winning_ways = [
        board.number[1] + board.number[0] + board.number[5],  # diagonal \
        board.number[3] + board.number[0] + board.number[7],  # diagonal /
        board.number[1] + board.number[8] + board.number[7],  # column |
        board.number[2] + board.number[0] + board.number[6],  # column |
        board.number[3] + board.number[4] + board.number[5],  # column |
        board.number[1] + board.number[2] + board.number[3],  # row -
        board.number[8] + board.number[0] + board.number[4],  # row -
        board.number[7] + board.number[6] + board.number[5],  # row -
    ]

    # Checks if X or O is the winner
    for winner, s in enumerate(["111", "222"]):
        for ww in winning_ways:
            if s == ww:
                return winner + 1

    # Draw
    if "0" not in board.number:
        return 0

    # Game hasn't end yet
    return -1
