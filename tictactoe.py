# write your code here
import random


class TicTacToe:
    TOP_AND_BOTTOM = '---------'
    board = [' '] * 9
    move = ['X', 'O']
    move_count = 0
    levels = ('user', 'easy', 'medium', 'hard')
    players = ['hard', 'hard']

    space_guide = {'11': 6, '12': 3, '13': 0, '21': 7, '22': 4, '23': 1, '31': 8, '32': 5, '33': 2}

    def __init__(self, player1='hard', player2='hard', start_pos=None):
        self.players = [player1, player2]
        if not start_pos:
            self.board = [' '] * 9
        else:
            self.board = [pos for pos in start_pos]
            self.move_count = self.board.count('X') + self.board.count('O')

    def print_board(self):
        print(TicTacToe.TOP_AND_BOTTOM)
        print(f'| {self.board[0]} {self.board[1]} {self.board[2]} |')
        print(f'| {self.board[3]} {self.board[4]} {self.board[5]} |')
        print(f'| {self.board[6]} {self.board[7]} {self.board[8]} |')
        print(TicTacToe.TOP_AND_BOTTOM)

    def game_state(self):
        winners = set()
        if all(space == 'X' for space in self.board[0:3]) or all(space == 'O' for space in self.board[0:3]):  # horizontal check
            winners.add(self.board[0])
        if all(space == 'X' for space in self.board[3:6]) or all(space == 'O' for space in self.board[3:6]):
            winners.add(self.board[3])
        if all(space == 'X' for space in self.board[6:9]) or all(space == 'O' for space in self.board[6:9]):
            winners.add(self.board[6])
        if all(space == 'X' for space in self.board[0:9:3]) or all(space == 'O' for space in self.board[0:9:3]):  # vertical check
            winners.add(self.board[0])
        if all(space == 'X' for space in self.board[1:9:3]) or all(space == 'O' for space in self.board[1:9:3]):
            winners.add(self.board[1])
        if all(space == 'X' for space in self.board[2:9:3]) or all(space == 'O' for space in self.board[2:9:3]):
            winners.add(self.board[2])
        if all(space == 'X' for space in self.board[0:9:4]) or all(space == 'O' for space in self.board[0:9:4]):  # diagonal check
            winners.add(self.board[0])
        if all(space == 'X' for space in self.board[2:7:2]) or all(space == 'O' for space in self.board[2:7:2]):
            winners.add(self.board[2])
        if len(winners) == 1:
            return f'{winners.pop()} wins'
        if len(winners) > 1 or self.board.count('X') - self.board.count('O') not in (0, 1):
            return 'Impossible'
        if ' ' in self.board:
            return 'Game not finished'
        return 'Draw'

    def clr_board(self):
        self.board = [' '] * 9

    def comp_move(self, level):
        empty = [space for space, player in enumerate(self.board) if player == ' ']
        winnable = self.next_move_wins()
        if len(empty) == 1 or level == 'easy' or (level == 'medium' and winnable == -1):
            self.make_move(random.choice(empty))
            return
        if winnable != -1:
            self.make_move(winnable)
            return
        self.make_move(self.minmax())

    def make_move(self, x, y=None):
        if y:
            space = ''.join((x, y))
            if self.board[TicTacToe.space_guide[space]] == ' ':
                self.board[TicTacToe.space_guide[space]] = TicTacToe.move[self.move_count % 2]
                self.move_count += 1
                return True
        else:
            self.board[x] = TicTacToe.move[self.move_count % 2]
            self.move_count += 1
            return True
        return False

    def next_move_wins(self):
        empty = [space for space, player in enumerate(self.board) if player == ' ']
        for space in empty:
            sample_game = TicTacToe(start_pos=str(''.join(self.board)))
            sample_game.make_move(space)
            if 'wins' in sample_game.game_state():
                return space
        return -1

    def minmax(self):
        if self.next_move_wins() != -1:
            return 10
        empty = {space: 0 for space, player in enumerate(self.board) if player == ' '}
        if len(empty) == 1:
            return 0
        if len(empty) == 9:
            return 4
        best_move = [-999999, -1]
        for space in empty:
            minmax_game = TicTacToe(start_pos=''.join(self.board))
            minmax_game.make_move(space)
            empty[space] = -1 * minmax_game.minmax()
            if empty[space] > best_move[0]:
                best_move = [empty[space], space]
        return best_move[1]


def new_game():
    start_game = input('Input command: ').split()
    while not start_game or not (
            start_game[0] == 'start' and all(level in TicTacToe.levels for level in start_game[1:]) and len(start_game) == 3):
        try:
            if start_game[0] == 'exit':
                break
        except IndexError:
            pass
        print('Bad parameters')
        start_game = input('Input command: ').split()
    return start_game


command = new_game()
game = ''
while command[0] != 'exit':
    if len(command) == 3 and command[0] == 'start' and all(level in TicTacToe.levels for level in command[1:]):
        game = TicTacToe(player1=command[1], player2=command[2])
        game.print_board()
        if 'user' not in game.players:
            while game.game_state() == 'Game not finished':
                print(f'Making move level "{game.players[game.move_count % 2]}"')
                game.comp_move(game.players[game.move_count % 2])
                game.print_board()
            print(game.game_state())

            command = new_game()

            continue
        elif command[1] != 'user':
            pass
        else:
            command = input('Enter the coordinates: ').split()
            continue
    if game.players[game.move_count % 2] == 'user':
        try:
            for coord in command:
                _ = int(coord)
        except ValueError:
            if command[0] == 'exit':
                break
            print('You should enter numbers!')
            command = input('Enter the coordinates: ').split()
            continue
        if not all(coord in ('1', '2', '3') for coord in command):
            print('Coordinates should be from 1 to 3!')
        elif game.make_move(command[0], command[1]):
            game.print_board()
            continue
        else:
            print('This cell is occupied! Choose another one!')
            command = input('Enter the coordinates: ').split()
            continue
    elif game.game_state() == 'Game not finished':
        print(f'Making move level "{game.players[game.move_count % 2]}"')
        game.comp_move(game.players[game.move_count % 2])
        game.print_board()
    if game.game_state() != 'Game not finished':
        print(game.game_state())
        game = ''

        command = new_game()

    else:
        command = input('Enter the coordinates: ').split()
