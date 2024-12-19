from flask import Flask, render_template, request, jsonify
import random
import math

app = Flask(__name__)

# Initialize a game board
def init_board():
    return [""] * 9  # 3x3 board initialized to empty strings

# Check if a player has won
def check_winner(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]  # diagonals
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

# Check if the game is a draw
def check_draw(board):
    return "" not in board

# Minimax algorithm with Alpha-Beta Pruning
def minimax(board, depth, alpha, beta, is_maximizing, player):
    opponent = "O" if player == "X" else "X"
    
    if check_winner(board, player):
        return 10 - depth
    if check_winner(board, opponent):
        return depth - 10
    if check_draw(board):
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for i in range(9):
            if board[i] == "":
                board[i] = player
                eval = minimax(board, depth + 1, alpha, beta, False, player)
                board[i] = ""
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if board[i] == "":
                board[i] = opponent
                eval = minimax(board, depth + 1, alpha, beta, True, player)
                board[i] = ""
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

def find_best_move(board, player):
    best_move = None
    best_value = -math.inf

    for i in range(9):
        if board[i] == "":
            board[i] = player
            move_value = minimax(board, 0, -math.inf, math.inf, False, player)
            board[i] = ""
            if move_value > best_value:
                best_value = move_value
                best_move = i
    return best_move

# Get random move for easy difficulty
def random_move(board):
    empty_cells = [i for i, cell in enumerate(board) if cell == ""]
    return random.choice(empty_cells) if empty_cells else None

# Block winning move for medium difficulty
def medium_move(board):
    for i in range(9):
        if board[i] == "":
            board[i] = "X"
            if check_winner(board, "X"):
                return i
            board[i] = "O"
            if check_winner(board, "O"):
                return i
            board[i] = ""
    return random_move(board)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    board = data['board']
    difficulty = data['difficulty']

    move = None
    
    if difficulty == 'easy':
        move = random_move(board)
    elif difficulty == 'medium':
        move = medium_move(board)
    elif difficulty == 'hard':
        move = find_best_move(board, "O")

    return jsonify({'move': move})

@app.route('/reset_game', methods=['POST'])
def reset_game():
    return jsonify({'message': 'Game Reset'})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)

