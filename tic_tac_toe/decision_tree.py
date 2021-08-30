import numpy as np
from typing import Tuple, Dict

from tic_tac_toe.utils.ternary import Ternary
from tic_tac_toe.utils.plot import plot
from tic_tac_toe.utils.permutations import whois_winner, get_all_boards, get_all_symmetries_for_board

np.set_printoptions(suppress=True)
TREE: Dict = {"up": {}, "down": {}}
RESULTS: Dict = {}
BOARD_CLASSES, _ = get_all_boards(exclude_winners=False)


def create_decision_tree() -> None:
    def generation(n: int) -> None:
        for a in BOARD_CLASSES[n]:
            TREE["up"][a] = []
            RESULTS[a] = whois_winner(Ternary(a))
            for b in BOARD_CLASSES[n - 1]:
                diff = Ternary(a) - Ternary(b)
                not_null = np.where(np.array(list(diff)) != "0")[0]
                if len(not_null) == 1:
                    TREE["up"][a].append(b)
                    if TREE["down"].get(a):
                        TREE["down"][b].append(a)
                    else:
                        TREE["down"][b] = [a]

    for i in range(10):
        generation(i)


def prune_tree(player: int = 2) -> None:
    for board, winner in RESULTS.items():
        if winner not in [player, 0, -1]:
            for perv_step in TREE["up"][board]:
                if board in TREE["down"][perv_step]:
                    TREE["down"][perv_step].remove(board)

            del TREE["up"][board]

    def prune_generation(n: int) -> None:
        for a in BOARD_CLASSES[n]:
            if not TREE["down"].get(a):
                for b in TREE["up"].get(a, []):
                    if b in TREE["up"].get(a):
                        TREE["up"][a].remove(b)

    for i in reversed(range(9)):
        prune_generation(i)


def human_player(board: Ternary, player: int = 1) -> Tuple[Ternary, int]:
    board_list = list(board.number)
    action = int(input("Human turn (0-8): "))
    while action not in np.where(np.array(list(board.number)) == "0")[0]:
        action = int(input(f"Action {action} is already used, try new (0-9): "))

    board_list[action] = str(player)
    return Ternary("".join(board_list)), action


if __name__ == "__main__":
    create_decision_tree()
    prune_tree()

    play_again = True
    while play_again:
        _board = Ternary("0" * 9)
        _winner = -1
        _turn = 1

        while _winner < 0:
            _player = _turn % 2 + 1
            if _player == 2:
                if _board.number in TREE["down"]:
                    symmetrical_board = _board.number
                else:
                    for b in get_all_symmetries_for_board(_board.number):
                        if b in TREE["down"]:
                            symmetrical_board = b
                            break
                print(TREE["down"][symmetrical_board])
                _board = Ternary(TREE["down"][symmetrical_board][0])

            else:
                print(plot(_board))
                _board, _ = human_player(_board)

            _winner = whois_winner(_board)
            _turn += 1

        print(f"\nWinner: {_winner}\n")
        print(plot(_board))

        play_again = input("Play again [y/n]: ") == "y"
