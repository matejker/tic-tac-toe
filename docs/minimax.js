let turn = 0;
let cells = [0, 0, 0, 0, 0, 0, 0, 0, 0];

function makeTurn(board, gameId) {
    const [_, action] = minimax(board, 0);
    if (action === -1) {
        return false;
    }
    document.querySelector('#cell_' + gameId + '_' + action).innerHTML = 'X';
    cells[action] = 2;
    turn += 1;

    whoWon(cells, gameId);
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

    whoWon(cells, gameId);
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
