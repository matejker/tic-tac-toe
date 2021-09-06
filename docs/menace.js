const replicasPerStage = [8, 4, 2, 1];
const rewards = {won: 3, draw: 1, lost: -1}
let menaceMemory = {0: {}, 1: {}}

let menaceCells = [0, 0, 0, 0, 0, 0, 0, 0, 0];
let turnMenace = 0;
let menaceHistory = [];

let totalBeadsAdded = [0];
let xAxis = [0];

const numberDiff = (a, b) => {
    let diff = 0;
    for (i in a) {
        if (a[i] != b[i]) {
            diff++;
        }
    }
    return diff;
}

const getPossibleSymmetryAction = (board_classes, board, stage) => {
    if (stage == 7) {
        return availActions(board);
    }

    let actions = [];

    for (b in boardClasses[stage + 1]) {
        newBoard = boardClasses[stage + 1][b];
        let diff = numberDiff(newBoard, board);
        if (diff.length == 1) {
            actions.push(diff[0]);
        }
    }
    return actions;
};

const initiateMenaceMemory = () => {
    const [boardClasses, _] = getAllBoards();
    for (stage in boardClasses.slice(0, -2)) {
        let _turn = (stage / 2) >> 0;
        for (b in boardClasses[stage]){
            let board = boardClasses[stage][b];
            let actions = (stage > 0) ? availActions(board) : [0, 1, 2];
            menaceMemory[stage % 2][board.join('')] = [];

            for (a in actions) {
                let action = actions[a];
                let defaultValues = new Array(replicasPerStage[_turn]).fill(action);
                menaceMemory[stage % 2][board.join('')].push(...defaultValues);
            }
        }
    }
};

function makeTurnMenace(board, gameId) {
    let actions = availActions(board);
    if (actions.length === 1) {
        const action = actions[0];
        document.querySelector('#cell_' + gameId + '_' + action).innerHTML = 'X';
        menaceCells[action] = 2;
        turnMenace += 1;

        whoWon(menaceCells, gameId);
        return
    }

    let symmetryClass = "";
    let symmetryElement = symmetryPermutations[0];

    if (board.join('') in menaceMemory[0]) {
        symmetryClass = board.join('');
    } else {
        const symmetries = getAllSymmetriesForBoard(board);
        for (s in symmetries) {
            let symmetry = symmetries[s];
            if (symmetry in menaceMemory[0]) {
                symmetryClass = symmetry;
                symmetryElement = symmetryPermutations[s];
            }
        }
    }

    if (!symmetryClass.length) {
        console.log('Any symmetry class found for ' + board.join('') + ' in MENACE\'s memory');
        return
    }
    const memoryActions = menaceMemory[0][symmetryClass];
    if (!memoryActions.length) {
        console.log();
        return
    }

    let actionChosen = choose(memoryActions);

    let actionOnOriginalBoard = symmetryElement[actionChosen];
    document.querySelector('#cell_' + gameId + '_' + actionOnOriginalBoard).innerHTML = 'X';
    menaceCells[actionOnOriginalBoard] = 2;
    turnMenace += 1;

    whoWon(menaceCells, gameId);

    return [actionChosen, symmetryClass];

};

const menaceLearn = (history, winner) => {
    if (history.length == 5) {
        history = history.slice(0, -1);
    }
    if (winner < 0) {
        return
    }

    xAxis.push(Number(xAxis.slice(-1)) + 1);

    if (winner == 1) {
        for (h in history) {
            let [action, symmetryClass] = history[h];
            for (let r = rewards.lost; r < 0; r++) {
                let i = menaceMemory[0][symmetryClass].indexOf(action);
                menaceMemory[0][symmetryClass].splice(i, 1);
            }
        }
        totalBeadsAdded.push(Number(totalBeadsAdded.slice(-1)) + rewards.lost);
        cumulativeRewardMenace.update();
        return
    }

    result = (winner == 2) ? rewards.won : rewards.draw;
    for (h in history) {
        let [action, symmetryClass] = history[h];
        const rewardValues = new Array(result).fill(action);
        menaceMemory[0][symmetryClass].push(...rewardValues);
    }
    totalBeadsAdded.push(Number(totalBeadsAdded.slice(-1)) + result);
    cumulativeRewardMenace.update();
    return

};

function cellClickMenace(gameId, e) {
    const d = document.querySelector('#' + e.target.id);
    if (!d.innerHTML && hadGameEnded(menaceCells.join('')) < 0) {
      let cellId = e.target.id.split("_")[2];
      d.innerHTML = (turnMenace % 2) ? 'O' : 'X';
      menaceCells[cellId] = (turnMenace % 2) ? 1 : 2;
      turnMenace += 1;
      let winner = hadGameEnded(menaceCells.join(''));

      whoWon(menaceCells, gameId);

      if (winner < 0) {
        let history = makeTurnMenace(menaceCells, gameId);
        menaceHistory.push(history);
      }
    }
    winner = hadGameEnded(menaceCells.join(''));
    if (winner > -1) {
        menaceLearn(menaceHistory, winner);
    }
}

function resetGameMenace(gameId) {
    let game = document.querySelector('#tic-tac-toe-' + gameId);
    game.innerHTML = "";

    menaceCells = [0, 0, 0, 0, 0, 0, 0, 0, 0];
    turnMenace = 0;
    let span = document.querySelector('#who-won-' + gameId);
    span.innerHTML = '';
    menaceHistory = [];

    let totalBeadsAdded = [0];
    let xAxis = [0];

    createGameMenace(gameId);
    console.log(menaceMemory[0]["000000000"]);
}

function createGameMenace(gameId) {
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
            cell.addEventListener('click', (e) => cellClickMenace(gameId, e));
            row.appendChild(cell);
        }
        game.appendChild(row);
    }
    menaceHistory = [];
    brains();

    let history = makeTurnMenace(menaceCells, gameId);
    menaceHistory.push(history);
}

const drawBrain = (symmetryClass) => {
    const brain = document.querySelector('#brain-' + symmetryClass);
    const values = menaceMemory[0][symmetryClass];

    for (let i = 0; i < n; i++) {
        let row = document.createElement('tr');
        if (i === 1) {
            row.setAttribute('class', 'middle');
        }

        for (let j = 0; j < n; j++) {
            let cell = document.createElement('td');
            if (j === 1) {
                cell.setAttribute('class', 'middle');
            }
            if (symmetryClass[idMapping[i][j]] == 0) {
                cell.innerHTML = values.filter(v => v == idMapping[i][j]).length;
            } else {
                cell.innerHTML = '<span class="red">' + ((symmetryClass[idMapping[i][j]] == '2') ? 'X' : 'O') + '</span>';
            }
            row.appendChild(cell);
        }
        brain.appendChild(row);
    }
}

const brains = () => {
    const brain = document.querySelector('#brains');
    brain.innerHTML = "";
    const [allBoards, _] = getAllBoards();
    for (b in allBoards.slice(0, -2)) {
        if (b % 2) {
            continue
        }
        for (s in allBoards[b]) {
            const symmetryClass = allBoards[b][s].join('');
            let table = document.createElement('table');
            table.setAttribute('class', 'brain');
            table.setAttribute('id', 'brain-' + symmetryClass);
            brain.appendChild(table);
            drawBrain(symmetryClass);
        }
    }
}

