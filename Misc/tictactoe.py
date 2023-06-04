from random import randint
from os import system

ROWS = 3
COLS = 3
EMPTY = "-"
PLAYER = "X" if randint(0, 1) == 0 else "O"
COMPUTER = "O" if PLAYER == "X" else "X"
DECODE_MOVES = [{0: "Top", 1: "Center", 2: "Bottom"},
                {0: "Left", 1: "Center", 2: "Right"}]


def eval_rows(board):
    for row in range(ROWS):
        if board[row][0] == board[row][1] == board[row][2]:
            if board[row][0] == PLAYER:
                return -10
            elif board[row][0] == COMPUTER:
                return 10

    return 0


def eval_cols(board):
    for col in range(COLS):
        if board[0][col] == board[1][col] == board[2][col]:
            if board[0][col] == PLAYER:
                return -10
            elif board[0][col] == COMPUTER:
                return 10

    return 0


def eval_diags(board):
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == PLAYER:
            return -10
        elif board[0][0] == COMPUTER:
            return 10

    if board[0][2] == board[1][1] == board[2][0]:
        if board[0][2] == PLAYER:
            return -10
        elif board[0][2] == COMPUTER:
            return 10

    return 0


def print_board(board):
    print(" Y -- 0 1 2\nX\n|")
    for i, row in enumerate(board):
        print(i, "   ", *row, sep=" ")


def evaluate(board):
    row_val = eval_rows(board)
    col_val = eval_cols(board)
    diag_val = eval_diags(board)
    if row_val != 0:
        return row_val
    if col_val != 0:
        return col_val
    if diag_val != 0:
        return diag_val
    return 0


def is_full(board):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == EMPTY:
                return False

    return True


def minimax(board, is_max):
    score = evaluate(board)
    if score != 0:
        return score
    if is_full(board):
        return 0
    if is_max:
        best = -1000
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] == EMPTY:
                    board[row][col] = COMPUTER
                    best = max(best, minimax(board, not is_max))
                    board[row][col] = EMPTY

        return best

    best = 1000
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == EMPTY:
                board[row][col] = PLAYER
                best = min(best, minimax(board, not is_max))
                board[row][col] = EMPTY

    return best


def get_best_move(board):
    best_move = -1, -1
    best_val = -1000

    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == EMPTY:
                board[row][col] = COMPUTER
                move_val = minimax(board, False)
                board[row][col] = EMPTY
                if move_val > best_val:
                    best_move = row, col
                    best_val = move_val

    return best_move


def clear_screen():
    system("cls")


def print_margins():
    print("=" * 100)


def main():
    board = [[EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY]]
    computer_chance = randint(0, 1) == 0
    clear_screen()
    while True:
        clear_screen()
        print_margins()
        print_board(board)
        print_margins()
        board_score = evaluate(board)
        if board_score < 0:
            print("Player Wins!")
            break
        elif board_score > 0:
            print("Computer Wins!")
            break
        elif is_full(board):
            print("Game ends in a Draw!")
            break

        if computer_chance:
            best_move = get_best_move(board)
            try:
                board[best_move[0]][best_move[1]] = COMPUTER
            except KeyError:
                print("Game ends in a Draw!")
                break

        else:
            while True:
                print(f"Your mark is {PLAYER}")
                print(f"Enter coordinates of mark as X Y: ", end="")
                x, y = tuple(int(ele) for ele in input().split())
                if not (0 <= x < ROWS and 0 <= y < COLS) or board[x][y] != EMPTY:
                    clear_screen()
                    print_margins()
                    print_board(board)
                    print_margins()
                    continue

                board[x][y] = PLAYER
                break

        computer_chance = not computer_chance
        


if __name__ == "__main__":
    main()
