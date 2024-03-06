import tkinter as tk

def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_board_full(board):
    return all(board[i][j] != ' ' for i in range(3) for j in range(3))

def get_empty_cells(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']

def evaluate_board(board):
    for player in ['X', 'O']:
        for i in range(3):
            if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
                return 1 if player == 'X' else -1
        if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
            return 1 if player == 'X' else -1
    return 0

def minimax(board, depth, maximizing_player):
    if check_winner(board, 'O'):
        return -1
    elif check_winner(board, 'X'):
        return 1
    elif is_board_full(board):
        return 0

    empty_cells = get_empty_cells(board)

    if maximizing_player:
        max_eval = float('-inf')
        for cell in empty_cells:
            board[cell[0]][cell[1]] = 'X'
            eval = minimax(board, depth + 1, False)
            eval += evaluate_board(board)
            board[cell[0]][cell[1]] = ' '
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for cell in empty_cells:
            board[cell[0]][cell[1]] = 'O'
            eval = minimax(board, depth + 1, True)
            eval += evaluate_board(board)
            board[cell[0]][cell[1]] = ' '
            min_eval = min(min_eval, eval)
        return min_eval

def get_best_move(board):
    empty_cells = get_empty_cells(board)
    best_move = None
    best_eval = float('-inf')

    for cell in empty_cells:
        board[cell[0]][cell[1]] = 'X'
        eval = minimax(board, 0, False)
        eval += evaluate_board(board)
        board[cell[0]][cell[1]] = ' '

        if eval > best_eval:
            best_eval = eval
            best_move = cell

    return best_move

class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic-Tac-Toe")
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.master, text='', font=('Helvetica', 20), width=5, height=2,
                                              command=lambda row=i, col=j: self.on_button_click(row, col), bg='#E0E0E0')
                self.buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

        self.message_label = tk.Label(self.master, text='', font=('Helvetica', 16), fg='white', bg='black')
        self.message_label.grid(row=3, columnspan=3, pady=10)

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        self.game_over = False
        self.restart_game()

    def on_button_click(self, row, col):
        if not self.game_over and self.board[row][col] == ' ':
            self.board[row][col] = 'O'
            self.buttons[row][col].config(text='O', state='disabled', disabledforeground='#004080')
            if check_winner(self.board, 'O'):
                self.display_message("You win!", '#008000')
            elif is_board_full(self.board):
                self.display_message("It's a tie!", '#808080')
            else:
                self.ai_move()

    def ai_move(self):
        if not self.game_over:
            ai_row, ai_col = get_best_move(self.board)
            self.board[ai_row][ai_col] = 'X'
            self.buttons[ai_row][ai_col].config(text='X', state='disabled', disabledforeground='#FF0000')

            if check_winner(self.board, 'X'):
                self.display_message("AI wins!", '#FF0000')
            elif is_board_full(self.board):
                self.display_message("It's a tie!", '#808080')

    def display_message(self, message, color):
        self.message_label.config(text=message, fg=color)
        self.game_over = True
        self.master.after(2000, self.restart_game)

    def restart_game(self):
        self.message_label.config(text='', fg='white')
        self.game_over = False
        for i in range(3):
            for j in range(3):
                self.board[i][j] = ' '
                self.buttons[i][j].config(text='', state='normal', bg='#E0E0E0')

    def on_close(self):
        self.master.destroy()

def main():
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
