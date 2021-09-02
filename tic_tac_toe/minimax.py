import numpy as np
from typing import Dict, Tuple

from tic_tac_toe.utils.plot import plot
from tic_tac_toe.utils.ternary import Ternary
from tic_tac_toe.utils.permutations import whois_winner


def get_score(board: Ternary, depth: int, player: int = 2) -> Tuple[int, bool]:
    winner = whois_winner(board)

    if winner == player:
        return 10 - depth, True
    elif winner < 1:
        return 0, winner == 0
    else:
        return depth - 10, True


def minimax(board: Ternary, depth: int = 0, player: int = 2) -> Tuple[Ternary, int]:
    score, ended = get_score(board, depth, player)
    if score != 0 or ended:
        return board, score

    depth += 1
    scored_actions: Dict = {}
    actions = np.where(np.array(list(board.number)) == "0")[0]
    active_player = len(actions) % 2 + 1

    for a in actions:
        action_board = list(board.number)
        action_board[a] = str(active_player)
        new_board = "".join(action_board)
        _, scored_actions[new_board] = minimax(Ternary(new_board), depth, player)

    if player == active_player:
        max_value = max(scored_actions.values())
        max_boards = [b for b, v in scored_actions.items() if v == max_value]
        return Ternary(np.random.choice(max_boards)), max_value
    else:
        min_value = min(scored_actions.values())
        min_boards = [b for b, v in scored_actions.items() if v == min_value]
        return Ternary(np.random.choice(min_boards)), min_value


if __name__ == "__main__":
    play_again = True
    while play_again:
        _board = Ternary("0" * 9)
        _winner = -1
        _turn = 1

        while _winner < 0:
            _player = _turn % 2 + 1
            if _player == 2:
                _board, _ = minimax(_board)
            else:
                print(plot(_board))
                _action = int(input("Human turn (0-8): "))
                while _action not in np.where(np.array(list(_board.number)) == "0")[0]:
                    _action = int(input(f"Action {_action} is already used, try new (0-9): "))

                _action_board = list(_board.number)
                _action_board[_action] = str(_player)

                _board = Ternary("".join(_action_board))

            _winner = whois_winner(_board)
            _turn += 1

        print(f"\nWinner: {_winner}\n")
        print(plot(_board))

        play_again = input("Play again [y/n]: ") == "y"
