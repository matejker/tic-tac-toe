import numpy as np
from typing import List

from tic_tac_toe.utils.ternary import Ternary

"""
  Symmetries of tic-tac-toe are equivalent to symmetries of square, often noted as D_4 with total 8 symmetries.
               A   t_y    D
  1 | 2 | 3     \ | | | /  t_AD
 ---+---+---   ---+---+---         • reflections about horizontal and vertical x and y axes
  4 | 0 | 5     - | + | - t_x      • reflections about diagonal AC and BD axes
 ---+---+---   ---+---+---         • three rotational symmetries about the center for 90°, 180° and 270°
  6 | 7 | 8     / | | | \ t_AC
              B           C
  However, the center is fixed for all symmetries we can simply ignore it in the permutations and consider only
  1-9 positions.
"""  # noqa

SYMMETRY_PERMUTATIONS = [
    np.array([0, 7, 8, 1, 2, 3, 5, 6, 7]),  # r - 90° rotation
    np.array([0, 5, 6, 7, 8, 1, 2, 3, 4]),  # r - 180° rotation
    np.array([0, 3, 4, 5, 6, 7, 8, 1, 2]),  # r - 270° rotation
    np.array([0, 7, 6, 5, 4, 1, 2, 3, 8]),  # t_x - reflection about the x axis
    np.array([0, 3, 2, 1, 8, 7, 6, 5, 4]),  # t_y - reflection about the y axis
    np.array([0, 1, 8, 7, 6, 5, 4, 3, 2]),  # t_AC - reflection about the AC axis
    np.array([0, 5, 4, 3, 2, 1, 8, 7, 6]),  # t_BD - reflection about the BD axis
]


def get_all_symmetries_for_board(board: Ternary) -> List[Ternary]:
    board_str = str(board.number)
    n = len(board_str)
    board_extended = "0" * (9 - n) + board_str
    board_array = np.array(list(board_extended))

    symmetry_list = []
    for p in SYMMETRY_PERMUTATIONS:
        symmetry = list(board_array[p])
        symmetry_str = "".join([str(s) for s in symmetry])
        symmetry_ternary = Ternary(int(symmetry_str))
        symmetry_list.append(symmetry_ternary)

    return list(set(symmetry_list))
