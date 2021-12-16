import chess
import numpy as numpy

from project.chess_utilities.utility import Utility
PAWN_TABLE = numpy.array([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [0, 0, 0, 0, 0, 0, 0, 0]
])

KNIGHT_TABLE = numpy.array([
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 15, 20, 20, 15, 0, -30],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
])

BISHOP_TABLE = numpy.array([
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]
])

ROOK_TABLE = numpy.array([
    [0, 0, 0, 5, 5, 0, 0, 0],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0]
])

QUEEN_TABLE = numpy.array([
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10, 0, 5, 0, 0, 0, 0, -10],
    [-10, 5, 5, 5, 5, 5, 0, -10],
    [0, 0, 5, 5, 5, 5, 0, -5],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [-10, 0, 5, 5, 5, 5, 0, -10],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20]
])

listoftable = {'Q': QUEEN_TABLE, "R": ROOK_TABLE, 'B': BISHOP_TABLE,
               'N': KNIGHT_TABLE,
               'P': PAWN_TABLE}

class ExampleUtility(Utility):

    def __init__(self) -> None:
        pass
#get a score for the position the pieces take on the scoreboard
    def get_piece_position_score(self, board: chess.Board):
        white = 0
        black = 0
        for x in range(64):
            piece = board.piece_at(x)
            if piece is not None :
                table = listoftable.get(str(piece))
                if table is not None:
                    table2 = table.flatten()
                    if piece.color:
                            white += table2[x]
                    else:
                        black += table2[7 - x]
        return white - black

#Calculate the weighted amount of white pieces minus the amount of black pieces
    def amount_of_pieces_score(self, board):
        n_white = 0
        n_white += len(board.pieces(piece_type=chess.PAWN, color=chess.WHITE))
        n_white += len(board.pieces(piece_type=chess.BISHOP, color=chess.WHITE)) * 3
        n_white += len(board.pieces(piece_type=chess.KNIGHT, color=chess.WHITE)) * 3
        n_white += len(board.pieces(piece_type=chess.ROOK, color=chess.WHITE)) * 5
        n_white += len(board.pieces(piece_type=chess.QUEEN, color=chess.WHITE)) * 9

        n_black = 0
        n_black += len(board.pieces(piece_type=chess.PAWN, color=chess.BLACK))
        n_black += len(board.pieces(piece_type=chess.BISHOP, color=chess.BLACK)) * 3
        n_black += len(board.pieces(piece_type=chess.KNIGHT, color=chess.BLACK)) * 3
        n_black += len(board.pieces(piece_type=chess.ROOK, color=chess.BLACK)) * 5
        n_black += len(board.pieces(piece_type=chess.QUEEN, color=chess.BLACK)) * 9
        scoreAmountOfPieces = n_white - n_black
        return scoreAmountOfPieces

    # Calculate the amount of white pieces minus the amount of black pieces
    def board_value(self, board: chess.Board):
        # if winning move, take it
        if board.is_checkmate():
            return 999
        score_board = self.get_piece_position_score(board)
        print("score_board = " + str(score_board))
        score_amount_of_pieces = self.amount_of_pieces_score(board)
        print("score_amount_of_pieces = " + str(score_amount_of_pieces))
        total_score = score_amount_of_pieces + score_board/10
        print("total_score = " + str(total_score))
        return total_score
