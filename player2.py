'''
An example/template implementation of the Player class.
'''

import chess
from genericplayer import GenericPlayer
import random


class Player(GenericPlayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    
    async def find_move(self) -> chess.Move:
        '''Example find_move method implementation
        Must return a chess.Move object.
        
        The example implementation will:
        - avoid draw moves if possible
        - always checkmate if a checkmate exists
        - if no checkmate exists, always check if a check exists
        '''
        
        legal_moves = set(self.board.legal_moves)
        draw_moves = set()
        
        for move in legal_moves:
            if self.board.is_draw_after(move):
                draw_moves.add(move)
                continue

            if self.board.is_checkmate_after(move):
                return move
        
        for move in legal_moves:
            if self.board.is_check_after(move):
                return move
        
        # Note that it is possible to have the only legal moves be moves that draw the game.
        preferred_moves = legal_moves - draw_moves
        if not preferred_moves:
            return random.choice(list(legal_moves))
        else:
            return random.choice(list(preferred_moves))