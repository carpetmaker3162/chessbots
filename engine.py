'''
An Engine object that behaves like a Player object, which invokes an external chess engine (ex. Stockfish)
'''

import chess
import chess.engine
from genericplayer import GenericPlayer

engine_path = 'stockfish/stockfish-macos-m1-apple-silicon'


class Engine(GenericPlayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = None
        self.time_limit = 0.01  # small time limit for benchmarking purposes
    
    
    async def initialize_engine(self):
        if self.engine is None:
            transport, self.engine = await chess.engine.popen_uci(engine_path)
    
    
    async def find_move(self) -> chess.Move:
        await self.initialize_engine()
        result = await self.engine.play(self.board, chess.engine.Limit(time=self.time_limit))
        return result.move
    
    
    async def close(self):
        if self.engine:
            await self.engine.quit()
            self.engine = None