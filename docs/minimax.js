const n = 3;
let turn = 0;

const idMapping = [
    [1, 2, 3],
    [8, 0, 4],
    [7, 6, 5]
];

let cells = [0, 0, 0, 0, 0, 0, 0, 0, 0];

const whoWon = (gameId) => {
    const whoWonMapping = ['It\'s draw!', 'Player O won!', 'Player X won!'];
    const winner = hadGameEnded(cells.join(''));

    if (winner > -1) {
        let span = document.querySelector('#who-won-' + gameId);
        span.innerHTML = whoWonMapping[winner];
}
}


const winningWays = (board) => [
    String(board[1]) + String(board[0]) + String(board[5]),  // diagonal \
    String(board[3]) + String(board[0]) + String(board[7]),  // diagonal /
    String(board[1]) + String(board[2]) + String(board[3]),  // top row
    String(board[8]) + String(board[0]) + String(board[4]),  // middle row
    String(board[7]) + String(board[6]) + String(board[5]),  // bottom row
    String(board[1]) + String(board[8]) + String(board[7]),  // left column
    String(board[2]) + String(board[0]) + String(board[6]),  // middle column
    String(board[3]) + String(board[4]) + String(board[5]),  // right column
]

function createGame(gameId) {
    let game = document.querySelector('#tic-tac-toe-' + gameId);
    for (let i = 0; i < n; i++) {
        let row = document.createElement('tr');
        if (i === 1) {
          row.setAttribute('class', 'middle');
        }

        for (let j = 0; j < n; j++) {
            let cell = document.createElement('td');
            cell.setAttribute('id', 'cell_' + gameId + '_' + idMapping[i][j]);
            if (j === 1) {
              cell.setAttribute('class', 'middle');
            }
            cell.addEventListener('click', (e) => cellClick(gameId, e));
            row.appendChild(cell);
        }
    game.appendChild(row);
    }
}

function makeTurn(board, gameId) {
    const [_, action] = minimax(board, 0);
    if (action === -1) {
        return false;
    }
    document.querySelector('#cell_' + gameId + '_' + action).innerHTML = 'X';
    cells[action] = 2;
    turn += 1;

    whoWon(gameId);
}

function cellClick(gameId, e) {
    const d = document.querySelector('#' + e.target.id);
    if (!d.innerHTML && hadGameEnded(cells.join('')) < 0) {
      let cellId = e.target.id.split("_")[2];
      d.innerHTML = (turn % 2) ? 'O' : 'X';
      cells[cellId] = (turn % 2) ? 1 : 2;
      turn += 1;
      makeTurn(cells, gameId);
    }

    whoWon(gameId);
}

function hadGameEnded(board) {
    const actions = availActions(board);

    if (actions.length === 0) {
        return 0;
    }

    const ww = winningWays(board);
    for (w in ww) {
        if (ww[w] === "222") {
            return 2;
        } else if (ww[w] === "111") {
            return 1;
        }
    }

    return -1;
}

function resetGame(gameId) {
    let game = document.querySelector('#tic-tac-toe-' + gameId);
    game.innerHTML = "";
    createGame(gameId);

    cells = [0, 0, 0, 0, 0, 0, 0, 0, 0];
    turn = 0;
    let span = document.querySelector('#who-won-' + gameId);
    span.innerHTML = '';

    makeTurn(cells, gameId);
}

window.onload=()=>{
    createGame(1);
    makeTurn(cells, 1);
}

const getScore = (board, depth) => {
    let winner = hadGameEnded(board);

    if (winner == 2) {
      return [10 - depth, true];
    } else if (winner < 1) {
      return [0, winner == 0];
    } else {
      return [depth - 10, true];
    }
}

const choose = (choices) => {
    const index = Math.floor(Math.random() * choices.length);
    return choices[index];
}

const availActions = (board) => {
    let actions = [];
    for (let i = 0; i < n * n; i++) {
        if (board[i] == 0) {
            actions.push(i);
        }
    }
    return actions;
}

const getAllIndexes = (arr, val) => {
    let indexes = [], i = -1;
    while ((i = arr.indexOf(val, i + 1)) != -1){
        indexes.push(i);
    }
    return indexes;
}

const minimax = (board, depth) => {
    let [score, ended] = getScore(board, depth);
    if (score != 0 || ended) {
        return [score, -1];
}

    const actions = availActions(board);
    let scores = [];
    let activePlayer = (actions.length % 2) + 1;

    depth++;

    for (a in actions) {
        let newBoard = [...board];
        let action = actions[a];
        newBoard[action] = activePlayer;
        let [score, _] = minimax(newBoard, depth);
        scores.push(score);
    }

    if (activePlayer == 2) {
        let maxValue = Math.max(...scores);
        let randomAction = choose(getAllIndexes(scores, maxValue));
        let actionChosen = actions[randomAction];
        let newBoard = [...board];
        newBoard[actionChosen] = activePlayer;

        return [maxValue, actionChosen];
    } else {
        let minValue = Math.min(...scores);
        let randomAction = choose(getAllIndexes(scores, minValue));
        let actionChosen = actions[randomAction];
        let newBoard = [...board];
        newBoard[actionChosen] = activePlayer;

        return [minValue, actionChosen];
    }
}