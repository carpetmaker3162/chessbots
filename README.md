# ChessBots  

An interface which allows people to implement their own chess bot  
This can be used for a programming club activity  

## Notes  

- This uses the [python-chess](https://python-chess.readthedocs.io/en/latest/) library  
- `player1.py` and `player2.py` are identical dummy implementations of `GenericPlayer` (`genericplayer.py`) which showcase various methods such as detecting checkmates/draws, etc  
- To use the `Engine` class (`engine.py`), a chess engine must be installed. I used Stockfish for my testing purposes. Simply create a `stockfish/` directory containing the Stockfish executable into the same directory as these files.  
- Scripts: `bench.py`, `main.py`, `play_vs_bot.py`