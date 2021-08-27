import numpy as np
from typing import List, Tuple, Set

from tic_tac_toe.utils.ternary import Ternary

"""
  Symmetries of tic-tac-toe are equivalent to the symmetries of a square, often noted as D_4 with total 8 symmetries.
               A   t_y    D
  1 | 2 | 3     \ | | | /  t_AD
 ---+---+---   ---+---+---         • reflections about horizontal and vertical x and y axes
  4 | 0 | 5     - | + | - t_x      • reflections about diagonal AC and BD axes
 ---+---+---   ---+---+---         • three rotational symmetries about the center for 90°, 180° and 270°
  6 | 7 | 8     / | | | \ t_AC
              B           C
  However, the center is fixed for all symmetries we can simply ignore it in the permutations and consider only
  1-8 positions.
"""  # noqa

SYMMETRY_PERMUTATIONS = [
    np.array([0, 1, 2, 3, 4, 5, 6, 7, 8]),  # identity
    np.array([0, 7, 8, 1, 2, 3, 4, 5, 6]),  # r - 90° rotation about 0
    np.array([0, 5, 6, 7, 8, 1, 2, 3, 4]),  # r - 180° rotation about 0
    np.array([0, 3, 4, 5, 6, 7, 8, 1, 2]),  # r - 270° rotation about 0
    np.array([0, 7, 6, 5, 4, 3, 2, 1, 8]),  # t_x - reflection about the x axis
    np.array([0, 3, 2, 1, 8, 7, 6, 5, 4]),  # t_y - reflection about the y axis
    np.array([0, 1, 8, 7, 6, 5, 4, 3, 2]),  # t_AC - reflection about the AC axis
    np.array([0, 5, 4, 3, 2, 1, 8, 7, 6]),  # t_BD - reflection about the BD axis
]


def get_all_symmetries_for_board(board: str) -> List[str]:
    board_array = np.array(list(board))

    symmetry_list = []
    for p in SYMMETRY_PERMUTATIONS:
        symmetry = list(board_array[p])
        symmetry_str = "".join([str(s) for s in symmetry])
        symmetry_list.append(symmetry_str)

    return symmetry_list


def get_all_boards(starting_player: int = 2) -> Tuple[List[List[str]], List[Set[str]]]:
    possible_boards = [set(), set(), set(), set(), set(), set(), set(), set()]
    board_classes = [[], [], [], [], [], [], [], []]
    possible_boards[0].add("000000000")
    board_classes[0].append("000000000")

    for r in range(1, 8):
        player = int((r + starting_player) % 2 + 1)
        for s in board_classes[r - 1]:
            possible_moves = np.where(np.array(list(s)) == "0")[0]
            for a in possible_moves:
                temp_board = list(s)
                temp_board[int(a)] = str(player)
                board = "".join(temp_board)

                # Game has ended on this board
                if whois_winner(Ternary(board)) >= 0:
                    continue

                # Board already exists in the set
                # If <A> ∩ <B> ≠ ∅ <=> <A> = <B>
                if board in possible_boards[r]:
                    continue

                board_symmetries = get_all_symmetries_for_board(board)
                possible_boards[r].update(board_symmetries)
                board_classes[r].append(board)

    return board_classes, possible_boards


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
