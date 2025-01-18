'''
An abstract player class.
Subclasses should implement the `find_move()` method, which returns a `chess.Move` object after examining the current board state
'''

from abc import ABC, abstractmethod
import chess


class GenericPlayer(ABC):
    def __init__(self, color: bool, game):
        self.color = color
        self.game = game
        self.board = game.board
    
    
    @property
    def opponent(self):
        return not self.color
    
    
    @property
    def my_time(self):
        '''
        The time left on the Player's own clock in seconds.
        Use `self.game.initial_time` to get original amount of time given to both players
        '''
        
        return self.game.white_time if self.color == chess.WHITE else self.game.black_time
    
    
    @property
    def opponent_time(self):
        '''
        The time left on the opposing Player's clock in seconds.
        Use `self.game.initial_time` to get original amount of time given to both players
        '''
        
        return self.game.black_time if self.color == chess.WHITE else self.game.white_time
    
    
    @abstractmethod
    async def find_move(self) -> chess.Move:
        pass