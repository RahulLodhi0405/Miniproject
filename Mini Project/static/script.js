let board = ["", "", "", "", "", "", "", "", ""];
let currentPlayer = "X";
let gameOver = false;

function updateBoard() {
    const cells = document.querySelectorAll('#game-board div');
    cells.forEach((cell, index) => {
        cell.textContent = board[index];
    });
}

function makeMove(cellIndex) {
    if (board[cellIndex] !== "" || gameOver) return;

    board[cellIndex] = currentPlayer;
    updateBoard();

    if (checkWinner(currentPlayer)) {
        document.getElementById('status').innerText = `${currentPlayer} wins!`;
        gameOver = true;
        return;
    }

    if (checkDraw()) {
        document.getElementById('status').innerText = "It's a draw!";
        gameOver = true;
        return;
    }

    currentPlayer = currentPlayer === "X" ? "O" : "X";
    document.getElementById('status').innerText = `${currentPlayer}'s turn`;

    if (currentPlayer === "O" && !gameOver) {
        aiMove();
    }
}

function aiMove() {
    const difficulty = document.getElementById("difficulty").value;
    fetch('/move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            board: board,
            difficulty: difficulty
        })
    })
    .then(response => response.json())
    .then(data => {
        const move = data.move;
        if (move !== null) {
            board[move] = "O";
            updateBoard();

            if (checkWinner("O")) {
                document.getElementById('status').innerText = "O wins!";
                gameOver = true;
                return;
            }

            if (checkDraw()) {
                document.getElementById('status').innerText = "It's a draw!";
                gameOver = true;
                return;
            }

            currentPlayer = "X";
            document.getElementById('status').innerText = "X's turn";
        }
    });
}

function checkWinner(player) {
    const winConditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], // rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], // columns
        [0, 4, 8], [2, 4, 6]  // diagonals
    ];
    for (let condition of winConditions) {
        if (board[condition[0]] === player && board[condition[1]] === player && board[condition[2]] === player) {
            return true;
        }
    }
    return false;
}

function checkDraw() {
    return board.every(cell => cell !== "");
}

function resetGame() {
    board = ["", "", "", "", "", "", "", "", ""];
    currentPlayer = "X";
    gameOver = false;
    document.getElementById('status').innerText = "X's turn";
    updateBoard();
}
