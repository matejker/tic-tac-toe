import numpy as np
from typing import Tuple, Dict
from copy import deepcopy

from tic_tac_toe.utils.ternary import Ternary
from tic_tac_toe.utils.plot import plot, plot_values
from tic_tac_toe.utils.permutations import whois_winner, get_all_boards, get_all_symmetries_for_board, SYMMETRY_PERMUTATIONS

np.set_printoptions(suppress=True)

# D. Michie used 4, 3, 2, 1
REPLICAS_PER_STAGE = [8, 4, 2, 1]
REWARDS = {"won": 3, "draw": 1, "lost": -1}
MENACE_MEMORY: Dict = {0: {}, 1: {}}


class MenaceException(Exception):
    pass


def initiate_menace_memory():
    board_classes, _ = get_all_boards()
    for stage, boards in enumerate(board_classes):
        turn = stage // 2

        for b in boards:
            actions = np.where(np.array(list(b)) == "0")[0]

            if stage % 2:
                MENACE_MEMORY[stage % 2][b] = []
            else:
                MENACE_MEMORY[stage % 2][b] = []

            for a in actions:
                if stage % 2:
                    MENACE_MEMORY[stage % 2][b].extend([int(a)] * REPLICAS_PER_STAGE[turn])
                else:
                    MENACE_MEMORY[stage % 2][b].extend([int(a)] * REPLICAS_PER_STAGE[turn])


def menace_make_turn(board: Ternary, player: int = 2) -> Tuple[Ternary, int, list]:
    board_list = list(board.number)
    actions = np.where(np.array(board_list) == "0")[0]

    if len(actions) == 1:
        board_list[actions[0]] = str(player)
        return Ternary("".join(board_list)), actions[0], [0] * 9

    symmetry_class = None
    symmetry_element = SYMMETRY_PERMUTATIONS[0]

    if board.number in MENACE_MEMORY[player % 2]:
        symmetry_class = board.number
    else:
        for e, s in enumerate(get_all_symmetries_for_board(board.number)):
            if s in MENACE_MEMORY[player % 2]:
                symmetry_class = s
                symmetry_element = SYMMETRY_PERMUTATIONS[player % 2][e]

    if symmetry_class is None:
        raise MenaceException(f"Any symmetry class found for {board.number} in MENACE's memory")

    try:
        action = np.random.choice(MENACE_MEMORY[player % 2][symmetry_class])
    except ValueError:
        raise MenaceException("MENACE's memory dies out 😭")

    action_on_original_board = symmetry_element[action]
    board_list[action_on_original_board] = str(player)

    action_histogram = [len(np.where(np.array(MENACE_MEMORY[player % 2][symmetry_class]) == a)[0]) for a in range(9)]
    return Ternary("".join(board_list)), action, action_histogram


def random_player(board: Ternary, player: int = 1) -> Tuple[Ternary, int]:
    board_list = list(board.number)
    actions = np.where(np.array(board_list) == "0")[0]
    action = np.random.choice(actions)
    board_list[action] = str(player)
    return Ternary("".join(board_list)), action


def human_player(board: Ternary, player: int = 1) -> Tuple[Ternary, int]:
    board_list = list(board.number)
    action = int(input("Human turn (0-8): "))
    while action not in np.where(np.array(list(board.number)) == "0")[0]:
        action = int(input(f"Action {action} is already used, try new (0-9): "))

    board_list[action] = str(player)
    return Ternary("".join(board_list)), action


if __name__ == "__main__":
    initiate_menace_memory()
    player_type = human_player
    menace_actions = []

    play_again = True
    while play_again:
        _board = Ternary("0" * 9)
        _winner = -1
        _turn = 1

        while _winner < 0:
            _player = _turn % 2 + 1
            if _player == 2:
                _board, _action, _action_values = menace_make_turn(_board)
                menace_actions.append(_action)

                print(plot_values(_board, _action_values))
            else:
                print(plot(_board))
                _board, _ = human_player(_board)

            _winner = whois_winner(_board)
            _turn += 1

        print(f"\nWinner: {_winner}\n")
        print(plot(_board))

        play_again = input("Play again [y/n]: ") == "y"
