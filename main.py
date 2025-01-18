'''
Play a single chess game with 2 bots
'''

from game import Game
from player1 import Player as Player1
from player2 import Player as Player2
from engine import Engine
import chess


if __name__ == '__main__':
    game = Game(white_player=Player1, black_player=Player2)
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
