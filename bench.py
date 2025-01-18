'''
Play many chess games with 2 Player or Engine objects, outputting overall statistics at the end
Can be used to evaluate a bot user's performance against other bot users
'''

from game import Game
from tqdm import tqdm
import chess
from engine import Engine
from player1 import Player as Player1
from player2 import Player as Player2
import json

terminations = {
    chess.Termination.STALEMATE: 'stalemate',
    chess.Termination.SEVENTYFIVE_MOVES: '75_moves',
    chess.Termination.FIVEFOLD_REPETITION: 'repetition',
    chess.Termination.INSUFFICIENT_MATERIAL: 'material'
}


def benchmark(iterations, verbose=False):
    results = {
        'black_win_time': 0,
        'white_win_time': 0,
        'black_win_checkmate': 0,
        'white_win_checkmate': 0,
        'repetition': 0,
        'material': 0,
        'stalemate': 0,
        '75_moves': 0,
    }
    
    score_w = 0
    score_b = 0
    
    if verbose:
        iterations = range(iterations)
    else:
        iterations = tqdm(range(iterations))
    
    for i in iterations:
        game = Game(white_player=Player1, black_player=Player2, verbose=False, export=False)
        try:
            game.loop()
        except TimeoutError:  # One player timed out
            termination = 'TIMEOUT'
            if game.turn is chess.WHITE:
                results['black_win_time'] += 1
                score_b += 1
                verdict = 'BLACK wins'
            else:
                results['white_win_time'] += 1
                score_w += 1
                verdict = 'WHITE wins'
        else:  # Any other normal outcome
            outcome = game.board.outcome()
            if outcome.winner is chess.BLACK:
                results['black_win_checkmate'] += 1
                score_b += 1
            elif outcome.winner is chess.WHITE:
                results['white_win_checkmate'] += 1
                score_w += 1
            else:
                results[terminations[outcome.termination]] += 1
                score_b += 0.5
                score_w += 0.5
            
            termination = str(outcome.termination)
        
            if outcome.winner is chess.WHITE:
                verdict = 'WHITE wins'
            elif outcome.winner is chess.BLACK:
                verdict = 'BLACK wins'
            else:
                verdict = 'DRAW'
        finally:
            if verbose:
                print(f'Game {(str(i) + ':').ljust(5)} {termination.ljust(34)} {verdict.ljust(12)} {game.clock_display()} {game.move_number}')
    
    return results, (score_w, score_b)


if __name__ == '__main__':
    results, scores = benchmark(100, verbose=True)
    score_w, score_b = scores
    print(json.dumps(results, indent=4))
    print(f'WHITE {score_w} - {score_b} BLACK')