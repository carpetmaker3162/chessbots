'''
A class representing a chess game.

- Stores the current board state.
- Queries Player classes for their next move
- Keeps track of both players' time, supporting increment
- Can be exported as a PGN file to be viewed on a website like https://lichess.org
'''

import asyncio
from board import Board
import chess
import chess.pgn
from genericplayer import GenericPlayer
from engine import Engine
import time
from utils import pretty_print
from hashlib import sha1


class Game:
    def __init__(self, white_player: GenericPlayer, black_player: GenericPlayer, initial_time=50000, increment=0, verbose=True, export=True):
        self.verbose = verbose
        self.export = export
        self.board = Board()
        self.white = white_player(chess.WHITE, self)
        self.black = black_player(chess.BLACK, self)
        self.initial_time = initial_time
        self.white_time = initial_time
        self.black_time = initial_time
        self.increment = increment
        self._turns_made = 0
    
    
    @property
    def move_number(self):
        return self._turns_made // 2 + 1
    
    
    def clock_display(self, fmt='[{:02d}:{:05.2f} - {:02d}:{:05.2f}]'):
        '''Return a string display of the current clock.'''
        white_time_min = int(self.white_time // 60)
        white_time_sec = self.white_time % 60
        black_time_min = int(self.black_time // 60)
        black_time_sec = self.black_time % 60
        return fmt.format(white_time_min, white_time_sec, black_time_min, black_time_sec)
    
    
    async def get_move_from(self, player: GenericPlayer):
        '''
        Get a move from a player then subtract from their clock accordingly.
        Raises TimeoutError if the player runs out of time.
        '''
        begin_time = time.time()
        timeout = self.white_time if player.color == chess.WHITE else self.black_time
        move = await asyncio.wait_for(player.find_move(), timeout=timeout)
        end_time = time.time()
        
        if player.color == chess.WHITE:
            self.white_time -= end_time - begin_time
            self.white_time += self.increment
        else:
            self.black_time -= end_time - begin_time
            self.black_time += self.increment
        
        return move
    
    
    def export_pgn(self):
        '''
        Export this game's PGN
        Easily visualize a game more clearly using websites like https://lichess.org
        '''
        game_pgn = chess.pgn.Game()
        node = game_pgn.add_variation(self.board.move_stack[0])
        for move in self.board.move_stack[1:]:
            node = node.add_variation(move)
        
        # Only used for identification purposes
        sha1_hash = sha1()
        sha1_hash.update(str(game_pgn).encode('utf-8'))
        game_pgn.headers['Event'] = 'Chessbots Match ' + sha1_hash.hexdigest()[:4]
        with open('game_pgn.txt', 'w') as f:
            f.write(str(game_pgn))
            
    
    def loop(self):
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
        
        if type(self.white) == Engine:
            event_loop.run_until_complete(self.white.initialize_engine())
        if type(self.black) == Engine:
            event_loop.run_until_complete(self.black.initialize_engine())
        
        try:
            while not self.board.is_game_over():
                if self.board.turn == chess.WHITE:
                    player = self.white
                    player_name = 'WHITE'
                else:
                    player = self.black
                    player_name = 'BLACK'
                
                try:
                    move = event_loop.run_until_complete(self.get_move_from(player))
                    self.board.push(move)
                except chess.IllegalMoveError:
                    print(f'{player_name} played illegal move.')
                    return
                
                self._turns_made += 1
                
                if self.verbose:
                    print('\n\n\n')
                    pretty_print(self.board)
        
        finally:
            if type(self.white) == Engine:
                event_loop.run_until_complete(self.white.close())
            if type(self.black) == Engine:
                event_loop.run_until_complete(self.black.close())
            event_loop.close()
        
        if self.export:
            self.export_pgn()
