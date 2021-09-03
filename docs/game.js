const n = 3;
const idMapping = [
    [1, 2, 3],
    [8, 0, 4],
    [7, 6, 5]
];

const symmetryPermutations = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8],  // identity
    [0, 7, 8, 1, 2, 3, 4, 5, 6],  // r - 90° rotation about 0
    [0, 5, 6, 7, 8, 1, 2, 3, 4],  // r - 180° rotation about 0
    [0, 3, 4, 5, 6, 7, 8, 1, 2],  // r - 270° rotation about 0
    [0, 7, 6, 5, 4, 3, 2, 1, 8],  // t_x - reflection about the x axis
    [0, 3, 2, 1, 8, 7, 6, 5, 4],  // t_y - reflection about the y axis
    [0, 1, 8, 7, 6, 5, 4, 3, 2],  // t_AC - reflection about the AC axis
    [0, 5, 4, 3, 2, 1, 8, 7, 6]  // t_BD - reflection about the BD axis
];

const whoWon = (board, gameId) => {
    const whoWonMapping = ['It\'s draw!', 'Player O won!', 'Player X won!'];
    const winner = hadGameEnded(board.join(''));

    if (winner > -1) {
        let span = document.querySelector('#who-won-' + gameId);
        span.innerHTML = whoWonMapping[winner];
    }
};

const winningWays = (board) => [
    String(board[1]) + String(board[0]) + String(board[5]),  // diagonal \
    String(board[3]) + String(board[0]) + String(board[7]),  // diagonal /
    String(board[1]) + String(board[2]) + String(board[3]),  // top row
    String(board[8]) + String(board[0]) + String(board[4]),  // middle row
    String(board[7]) + String(board[6]) + String(board[5]),  // bottom row
    String(board[1]) + String(board[8]) + String(board[7]),  // left column
    String(board[2]) + String(board[0]) + String(board[6]),  // middle column
    String(board[3]) + String(board[4]) + String(board[5]),  // right column
];

function hadGameEnded(board) {
    const actions = availActions(board);

    const ww = winningWays(board);
    for (w in ww) {
        if (ww[w] === "222") {
            return 2;
        } else if (ww[w] === "111") {
            return 1;
        }
    }

    if (actions.length === 0) {
        return 0;
    }

    return -1;
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
};

const getScore = (board, depth) => {
    let winner = hadGameEnded(board);

    if (winner == 2) {
      return [10 - depth, true];
    } else if (winner < 1) {
      return [0, winner == 0];
    } else {
      return [depth - 10, true];
    }
};

const getAllSymmetriesForBoard = (board) => {
    let symmetryList = [];

    for (s in symmetryPermutations) {
        let permutation = symmetryPermutations[s];
        symmetryList.push(permutation.map((i) => board[i]).join(''));
    }
    return symmetryList;
};

const getAllBoards = () => {
    let possibleBoards = [
        new Set(), new Set(), new Set(),
        new Set(), new Set(), new Set(),
        new Set(), new Set(), new Set(), new Set()
    ];
    let boardClasses = [[], [], [], [], [], [], [], [], [], []];
    possibleBoards[0].add([0, 0, 0, 0, 0, 0, 0, 0, 0]);
    boardClasses[0].push([0, 0, 0, 0, 0, 0, 0, 0, 0]);

    for (let r = 1; r < 10; r++) {
        let activePlayer = r % 2 + 1;
        for (s in boardClasses[r - 1]) {
            let board = boardClasses[r - 1][s];
            let possibleActions = availActions(board);
            for (a in possibleActions) {
                let actionChosen = possibleActions[a];
                let newBoard = [...board];
                newBoard[actionChosen] = activePlayer;
                const strBoard = newBoard.join('');

                if (hadGameEnded(newBoard) >= 0) {
                    continue;
                }

                if (possibleBoards[r].has(strBoard)) {
                    continue
                }

                boardSymmetries = getAllSymmetriesForBoard(newBoard);
                boardSymmetries.forEach(possibleBoards[r].add, possibleBoards[r]);
                boardClasses[r].push(newBoard);
            }
        }
    }
    return [boardClasses, boardSymmetries];
}
