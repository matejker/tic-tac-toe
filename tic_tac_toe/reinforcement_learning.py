import numpy as np
from typing import Tuple, Dict
from copy import deepcopy

from tic_tac_toe.game import whois_winner
from tic_tac_toe.utils.ternary import Ternary
from tic_tac_toe.utils.plot import plot, plot_values

np.set_printoptions(suppress=True)

VALUE_X: Dict = {}
VALUE_O: Dict = {}
DEFAULT_VALUE = 0.5
EPSILON = 0.05
ALPHA = 0.5


def get_value(board: Ternary, player: int) -> Tuple[Ternary, float]:
    """A value function for each state and player
    Initial values:
    • Winning end-state has value 1
    • Lost / draw end-states are worth 0
    • Otherwise DEFAULT_VALUE (0.5)
    """
    v = VALUE_X if player == 2 else VALUE_O

    if (w := whois_winner(board)) >= 0:
        v[board.number] = (w == player) * 1
        return board, v[board.number]

    return board, v.get(board.number, DEFAULT_VALUE)


def explore_action(board: Ternary, player: int) -> Tuple[int, Ternary]:
    """Choose action at random from the set of available actions"""
    actions = np.where(np.array(list(board.number)) == "0")[0]
    action_chosen = np.random.choice(actions, 1)[0]

    action_board = list(board.number)
    action_board[action_chosen] = str(player)

    return action_chosen, Ternary("".join(action_board))


def exploit_action(board: Ternary, player: int) -> Tuple[int, Ternary, Dict]:
    """Choose action with the highest value from player's value function"""
    actions = np.where(np.array(list(board.number)) == "0")[0]
    best_action_value = -99.0
    best_action_hash = Ternary("0" * 9)
    best_action = 0
    action_values: Dict = {}

    for a in actions:
        action_board = list(board.number)
        action_board[a] = str(player)
        action_hash, action_value = get_value(Ternary("".join(action_board)), player)
        action_values[a] = action_value

        if best_action_value < action_value:
            best_action_value = action_value
            best_action_hash = deepcopy(action_hash)
            best_action = a

    return best_action, best_action_hash, action_values


def train(num_rounds=10000):
    """To train players and fill their value functions with winning probabilities"""
    for r in range(1, num_rounds + 1):
        board = Ternary("0" * 9)
        turn = 1
        winner = -1
        game = ""
        history_x = []
        history_o = []

        # Play game
        while winner < 0:
            player = turn % 2 + 1

            # Explore move
            if np.random.uniform(0, 1) < EPSILON:
                action, board_hash = explore_action(board, player)
            # Exploit move
            else:
                action, board_hash, _ = exploit_action(board, player)

            if player == 2:
                history_x.append(board_hash)
            else:
                history_o.append(board_hash)

            game += str(action)

            action_board = list(board.number)
            action_board[action] = str(player)

            board = Ternary("".join(action_board))
            winner = whois_winner(board)
            turn += 1

        reward_x = (winner == 2) * 1.0
        reward_o = (winner == 1) * 1.0

        """
        Player's value functions are updated based on:
          V(S_t) = V(S_t) + \alpha * (V(S_{t+1}) - V(S_t))
        where S_t is state at time t, \alpha is the learning rate parameter and V(S_t)
        is the probability of winning from that state.
        """

        # Assign values player X
        for h in history_x[::-1]:
            _, v = get_value(h, 2)
            VALUE_X[h.number] = v + ALPHA * (reward_x - v)
            reward_x = deepcopy(VALUE_X[h.number])

        # Assign values player O
        for h in history_o[::-1]:
            _, v = get_value(h, 1)
            VALUE_O[h.number] = v + ALPHA * (reward_o - v)
            reward_o = deepcopy(VALUE_O[h.number])

        # Logging
        if r % 10000 == 0:
            print(f"\nGame: {game}, winner: {winner}, round: {r}\n")
            print(plot(game))


if __name__ == "__main__":
    print("Training...")
    train()
    print("Training finished!")
    print("-------------------------")
    print("Human vs RL")

    play_again = True
    while play_again:
        _board = Ternary("0" * 9)
        _winner = -1
        _turn = 1

        while _winner < 0:
            _player = _turn % 2 + 1
            if _player == 2:
                _action, _, _action_values = exploit_action(_board, _player)

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
