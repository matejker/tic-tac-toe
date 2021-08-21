import numpy as np
from typing import Tuple

from tic_tac_toe.game import whois_winner
from tic_tac_toe.utils.plot import plot, plot_values
from tic_tac_toe.utils.permutations import get_all_symmetries_for_board
from tic_tac_toe.utils.ternary import Ternary

VALUE_X = {}
VALUE_O = {}
DEFAULT_VALUE = 0.5
EPSILON = 0.2
ALPHA = 0.9


def get_value(board: Ternary, player: int) -> Tuple[Ternary, float]:
    v = VALUE_X if player == 2 else VALUE_O

    if v.get(board.number) is None:
        symmetries = get_all_symmetries_for_board(board)

        for s in symmetries:
            if v.get(s.number) is not None:
                return s, v.get(s.number)

    return board, v.get(board.number, DEFAULT_VALUE)


def explore_action(board: Ternary, player: int) -> Tuple[int, Ternary]:
    actions = np.where(np.array(list(board.number)) == "0")[0]
    action_chose = np.random.choice(actions, 1)[0]

    action_board = list(board.number)
    action_board[action_chose] = str(player)

    action_hash, action_value = get_value(Ternary("".join(action_board)), player)

    return action_chose, action_hash


def exploit_action(board: Ternary, player: int) -> Tuple[int, Ternary]:
    actions = np.where(np.array(list(board.number)) == "0")[0]
    best_action_value = -99
    best_action_hash = Ternary("0" * 9)
    best_action = 0

    for a in actions:
        action_board = list(board.number)
        action_board[a] = str(player)
        action_hash, action_value = get_value(Ternary("".join(action_board)), player)

        if best_action_value < action_value:
            best_action_value = action_value
            best_action = a

    return best_action, best_action_hash


def train(num_rounds=100):
    for r in range(num_rounds):
        board = Ternary("0" * 9)
        turn = 1
        winner = -1
        game = ""
        history = []

        # Play game
        while winner < 0:
            player = turn % 2 + 1

            # Explore move
            if np.random.rand() < EPSILON:
                action, board_hash = explore_action(board, player)
            # Exploit move
            else:
                action, board_hash = exploit_action(board, player)

            history.append(board_hash)
            game += str(action)

            action_board = list(board.number)
            action_board[action] = str(player)

            board = Ternary("".join(action_board))
            winner = whois_winner(board)
            turn += 1

        if winner == 2:
            reward_x = 1
            reward_o = 0
        elif winner == 1:
            reward_x = 0
            reward_o = 1
        else:
            reward_x = 0
            reward_o = 0

        # Assign values player X
        for h in history[::-2]:
            v = VALUE_X.get(h.number, DEFAULT_VALUE)
            VALUE_X[h.number] = v + ALPHA * (reward_x - v)
            reward_x = v

        # Assign values player X
        for h in history[::-1][1::2]:
            v = VALUE_X.get(h.number, DEFAULT_VALUE)
            VALUE_X[h.number] = v + ALPHA * (reward_o - v)
            reward_o = v

        # Logging
        if r % 10000 == 0:
            print(f"\nGame: {game}, winner: {winner}, round: {r}\n")
            print(plot(game))


if __name__ == "__main__":
    print("Training...")
    train(60000)
    print("Training finished!")
    print("-------------------------")
    print("Human vs RL")

    play_again = True
    while play_again:
        _board = Ternary("0" * 9)
        _winner = -1
        _turn = 1
        _action_values = {}

        while _winner < 0:
            _player = _turn % 2 + 1
            if _player == 2:
                _action, _ = exploit_action(_board, _player)

                for _a in np.where(np.array(list(_board.number)) == "0")[0]:
                    __action_board = list(_board.number)
                    __action_board[_a] = str(_player)
                    _, _action_value = get_value(Ternary("".join(__action_board)), _player)
                    _action_values[_a] = _action_value

                print(plot_values(_board, _action_values))
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
