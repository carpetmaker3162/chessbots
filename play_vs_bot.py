'''
Use this class to play against a bot user (either a Player or Engine object)
'''

import chess
from genericplayer import GenericPlayer
from utils import pretty_print
from player1 import Player as Player1
from player2 import Player as Player2
from game import Game


class Human(GenericPlayer):
    '''
    A GenericPlayer class that prompts the user for the next move via stdin, instead of coming up with a move by itself
    Mainly intended for use within a script allowing a human player to play against a bot
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pretty_print(self.board)
    
    
    async def find_move(self) -> chess.Move:
        player = ('BLACK' if self.color is chess.BLACK
                else 'WHITE')
        
        while True:
            try:
                move = self.board.parse_san(input(f'Input move as {player}: '))
                return move
            except chess.InvalidMoveError:
                print('Invalid Algebraic Notation.')
            except chess.IllegalMoveError:
                print('Illegal move.')
            except chess.AmbiguousMoveError:
                print('The move is ambiguous. Try again.')


if __name__ == '__main__':
    game = Game(white_player=Player1, black_player=Human)
    try:
        game.loop()
    except TimeoutError:
        player = ('BLACK' if game.turn is chess.BLACK
                else 'WHITE')
        print(f'{player} loses by timeout on move {game.move_number}')
    else:
        print()
        outcome = game.board.outcome()
        winner = ('BLACK (lowercase)' if outcome.winner is chess.BLACK
                else 'WHITE (uppercase)' if outcome.winner is chess.WHITE
                else None)
        
        if outcome.termination == chess.Termination.CHECKMATE:
            print(f'{winner} wins by checkmate after {game.move_number} moves')

        else:
            print(f'Draw by {str(outcome.termination).removeprefix('Termination.')} after {game.move_number} moves')
