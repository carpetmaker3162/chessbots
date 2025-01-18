from board import Board
import chess

pieces_w = 'PRNBQK'
pieces_b = 'prnbqk'

piece_value = {
    chess.KING: float('inf'),  # should be unnecessary
    chess.QUEEN: 9,
    chess.ROOK: 5,
    chess.BISHOP: 3,
    chess.KNIGHT: 3,
    chess.PAWN: 1,
}

def value(piece: chess.Piece | None):
    return 0 if piece is None else piece_value[piece.piece_type]


def pretty_print(board: Board, **kwargs):
    str_board = str(board)
    for piece_b in pieces_b:
        str_board = str_board.replace(piece_b, '\033[97m\033[100m' + piece_b.upper() + '\033[0m')
    print(str_board, **kwargs)
    return str_board