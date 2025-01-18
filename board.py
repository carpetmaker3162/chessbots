'''
chess.Board with some add-ons
'''

import chess
from typing import *


class Board(chess.Board):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    
    def get_position_after(self, moves: List[chess.Move]):
        '''
        Return a new Board object representing the state of the board after a certain sequence of moves
        Raises chess.IllegalMoveError if one of the moves are ilegal
        Will always return the move stack to its original state
        '''
        
        illegal_move = False
        for i in range(len(moves)):
            move = moves[i]
            if not self.is_legal(move):
                illegal_move = True
                break
            self.push(move)
        
        board_after_moves = self.copy()
        
        for _ in range(i + 1 - illegal_move):
            self.pop()
        
        if illegal_move:
            raise chess.IllegalMoveError
        else:
            return board_after_moves
    
    
    def is_check_after(self, move: chess.Move):
        if not self.is_legal(move):
            raise chess.IllegalMoveError
        
        return self.gives_check(move)
    
    
    def is_checkmate_after(self, move: chess.Move):
        if not self.is_legal(move):
            raise chess.IllegalMoveError
        
        self.push(move)
        ans = self.is_checkmate()
        self.pop()
        return ans
    
    
    def is_stalemate_after(self, move: chess.Move):
        if not self.is_legal(move):
            raise chess.IllegalMoveError
        
        self.push(move)
        ans = self.is_stalemate()
        self.pop()
        return ans
    
    
    def is_fivefold_repetition_after(self, move: chess.Move):
        if not self.is_legal(move):
            raise chess.IllegalMoveError
        
        self.push(move)
        ans = self.is_fivefold_repetition()
        self.pop()
        return ans
    
    
    def is_draw_after(self, move: chess.Move):
        if not self.is_legal(move):
            raise chess.IllegalMoveError
        
        return self.is_stalemate_after(move) or self.is_fivefold_repetition_after(move)