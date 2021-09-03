import numpy as np
from typing import Tuple, Dict, List

from tic_tac_toe.utils.ternary import Ternary
from tic_tac_toe.utils.plot import plot, plot_values
from tic_tac_toe.utils.permutations import (
    whois_winner,
    get_all_boards,
    get_all_symmetries_for_board,
    SYMMETRY_PERMUTATIONS,
)

np.set_printoptions(suppress=True)

# D. Michie used 4, 3, 2, 1 / 8, 4, 2, 1
REPLICAS_PER_STAGE = [8, 4, 2, 1]
REWARDS = {"won": 3, "draw": 1, "lost": -1}
MENACE_MEMORY: Dict = {0: {}, 1: {}}


class MenaceException(Exception):
    pass


def get_possible_actions(board_classes: List, board: str, stage: int) -> List:
    if stage == 7:
        return np.where(np.array(list(board)) == "0")[0]

    actions = []

    for b in board_classes[stage + 1]:
        diff = Ternary(board) - Ternary(b)
        not_null = np.where(np.array(list(diff)) != "0")[0]

        if len(not_null) == 1:
            actions.append(not_null[0])

    return np.array(actions)


def initiate_menace_memory():
    board_classes, _ = get_all_boards()
    for stage, boards in enumerate(board_classes[:-2]):
        turn = stage // 2

        for b in boards:
            actions = np.where(np.array(list(b)) == "0")[0] if stage > 0 else np.array([0, 1, 2])

            MENACE_MEMORY[stage % 2][b] = []

            for a in actions:
                MENACE_MEMORY[stage % 2][b].extend([int(a)] * REPLICAS_PER_STAGE[turn])


def menace_make_turn(board: Ternary, player: int = 2) -> Tuple[Ternary, int, str, Dict]:
    board_list = list(board.number)
    actions = np.where(np.array(board_list) == "0")[0]

    if len(actions) == 1:
        board_list[actions[0]] = str(player)
        return Ternary("".join(board_list)), actions[0], board.number, {a: 0 for a in range(9)}

    symmetry_class = None
    symmetry_element = SYMMETRY_PERMUTATIONS[0]

    if board.number in MENACE_MEMORY[player % 2]:
        symmetry_class = board.number
    else:
        for e, s in enumerate(get_all_symmetries_for_board(board.number)):
            if s in MENACE_MEMORY[player % 2]:
                symmetry_class = s
                symmetry_element = SYMMETRY_PERMUTATIONS[e]

    if symmetry_class is None:
        raise MenaceException(f"Any symmetry class found for {board.number} in MENACE's memory")

    try:
        action = np.random.choice(MENACE_MEMORY[player % 2][symmetry_class])
    except ValueError:
        raise MenaceException("MENACE's memory dies out 😭")

    action_on_original_board = symmetry_element[action]
    board_list[action_on_original_board] = str(player)

    action_histogram = {
        a: len(np.where(np.array(MENACE_MEMORY[player % 2][symmetry_class]) == a)[0]) + 0.1 for a in range(9)
    }
    return Ternary("".join(board_list)), action, symmetry_class, action_histogram


def menace_learn(history: List, winner: int, player: int = 2) -> None:
    if len(history) == 5:
        history = history[:-1]

    # Game hasn't ended yet
    if winner < 0:
        return

    if winner not in [player, 0]:
        for action, symmetry_class in history:
            for _ in range(abs(REWARDS["lost"])):
                MENACE_MEMORY[player % 2][symmetry_class].remove(action)

        return

    result = "won" if winner == player else "draw"
    for action, symmetry_class in history:
        MENACE_MEMORY[player % 2][symmetry_class].extend([action] * REWARDS[result])

    return


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


def train(num_rounds=100):
    for r in range(1, num_rounds + 1):
        board = Ternary("0" * 9)
        winner = -1
        turn = 1
        menace_actions = []

        while winner < 0:
            player = turn % 2 + 1
            if player == 2:
                board, action, symmetry_class, _ = menace_make_turn(board)
                menace_actions.append((action, symmetry_class))
            else:
                board, _ = random_player(board)

            turn += 1

            winner = whois_winner(board)
            menace_learn(menace_actions, winner)

        # Logging
        if r % (num_rounds // 10) == 0:
            action_histogram = {a: len(np.where(np.array(MENACE_MEMORY[0]["0" * 9]) == a)[0]) for a in range(9)}
            print(plot_values(Ternary("0" * 9), action_histogram, decimal=False))


if __name__ == "__main__":
    initiate_menace_memory()
    print("Training...")
    train()
    print("Training finished!")
    print("-------------------------")
    print("Human vs Menace")

    play_again = True
    while play_again:
        _board = Ternary("0" * 9)
        _winner = -1
        _turn = 1
        _menace_actions = []
        _action_values = {a: len(np.where(np.array(MENACE_MEMORY[0]["0" * 9]) == a)[0]) for a in range(9)}

        while _winner < 0:
            _player = _turn % 2 + 1
            if _player == 2:
                print(_action_values)
                print(plot_values(_board, _action_values, decimal=False))
                _board, _action, _symmetry_class, _action_values = menace_make_turn(_board)
                _menace_actions.append((_action, _symmetry_class))

            else:
                print(plot(_board))
                _board, _ = human_player(_board)

            _winner = whois_winner(_board)
            _turn += 1

        menace_learn(_menace_actions, _winner)

        print(f"\nWinner: {_winner}\n")
        print(plot(_board))

        play_again = input("Play again [y/n]: ") == "y"
