import chess
import numpy as numpy

from project.chess_utilities.utility import Utility
PAWN_TABLE = numpy.array([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [-5, -30, -40, -70, -50, -40, -30, -5],
    [5, -5, -10, 10, 30, -10, -5, 5],
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

    def get_score_of_piece(self, value):
        if value.upper() == 'N':
            return 5
        elif value.upper() == 'Q':
            return 9
        elif value.upper() == 'P':
            return 1
        elif value.upper() == 'R':
            return 3
        elif value.upper() == 'B':
            return 3
        elif value.upper() == 'K':
            return 50

    def get_pieces_squares_covered_combined(self, board: chess.Board):
        whitesquarescovered = 0
        blacksquarescovered = 0
        whiteattacks = 0
        blackattacks = 0
        whitedefend = 0
        blackdefend = 0
        whiteposition = 0
        blackposition = 0

        for x in range(64):
            piece = board.piece_at(x)
            if piece is not None:
                table = listoftable.get(str(piece).upper())
                # position score
                if table is not None:
                    tableflattend = table.flatten()
                    if piece.color:
                        whiteposition += tableflattend[x]
                    elif not piece.color:
                        blackposition += tableflattend[63 - x]
                # amount of squares covered by piece
                squarescovered = len(board.attacks(x))
                # amount of attacked/defended squares
                # gets location and pieces of all attackable places
                squaresattack = (board.attacks(x))
                for square in squaresattack:
                    pieceinsquareattack = board.piece_at(square)
                    if pieceinsquareattack is not None:
                        if piece.color:
                            if not pieceinsquareattack.color:
                                piecetype = pieceinsquareattack
                                multiplier = self.get_score_of_piece(str(piecetype))
                                whiteattacks += 1 * multiplier
                            else:
                                whitedefend += 1
                        else:
                            if pieceinsquareattack.color:
                                piecetype = pieceinsquareattack
                                multiplier = self.get_score_of_piece(str(piecetype))
                                blackattacks += 1 * multiplier
                            else:
                                blackdefend += 1
                # for squares covered
                if piece.color:
                    # gets amount of covered places
                    whitesquarescovered += squarescovered
                else:
                    # gets amount of covered places
                    blacksquarescovered += squarescovered

        squarescoveredscore = whitesquarescovered - blacksquarescovered
        positionscore = whiteposition - blackposition
        defendscore = whitedefend - blackdefend
        attackscore = whiteattacks - blackattacks
        """        
        print("squarescoveredscore= " + str(squarescoveredscore))
        print("positionscore= " + str(positionscore))
        print("defendscore= " + str(defendscore))
        print("attackscore= " + str(attackscore))
        totalscore = attackscore + defendscore + positionscore / 50 + squarescoveredscore / 3
        print("totaalscore= " + str(totalscore))
        """
        #totalscore = attackscore / 30 + defendscore / 20 + positionscore / 60 + squarescoveredscore / 3  # heeft 1 win gefixed
        totalscore = attackscore / 35 + defendscore / 20 + positionscore / 65 + squarescoveredscore / 3


        return totalscore


    def get_squares_covered(self, board: chess.Board):
        white = 0
        black = 0
        for x in range(64):
            piece = board.piece_at(x)
            squares = len(board.attacks(x))

            if piece is not None:
                    if piece.color:
                            #gets amount of covered places
                            squares = len(board.attacks(x))
                            white += squares
                    else:
                        # gets amount of covered places
                        squares = len(board.attacks(x))
                        black += squares
        return white - black

#checks how many pieces can be attacked
    def get_piece_attacks(self, board: chess.Board):
        white = 0
        black = 0
        for x in range(64):
            piece = board.piece_at(x)
            if piece is not None:
                    if piece.color:
                            #gets location of all attackable places
                            squares = (board.attacks(x))
                            #checks if enemy is at attackable squares
                            for square in squares:
                                pieceinsquare = board.piece_at(square)
                                if pieceinsquare is not None:
                                    if not pieceinsquare.color:
                                        piecetype = pieceinsquare
                                        multiplier = self.get_score_of_piece(str(piecetype))
                                        white += 1 * multiplier
                    else:
                        # gets location of all attackable places
                        squares = (board.attacks(x))
                        # checks if enemy is at attackable squares
                        for square in squares:
                            pieceinsquare = board.piece_at(square)
                            if pieceinsquare is not None:
                                if pieceinsquare.color:
                                    piecetype = pieceinsquare
                                    multiplier = self.get_score_of_piece(str(piecetype))
                                    black += 1  * multiplier
        return white - black

# checks how many pieces are protected
    def get_piece_defend(self, board: chess.Board):
        white = 0
        black = 0
        for x in range(64):
            piece = board.piece_at(x)
            # gets location of all attackable places
            squares = (board.attacks(x))
            if piece is not None:
                if piece.color:
                    # checks white is at attackable squares
                    for square in squares:
                        pieceinsquare = board.piece_at(square)
                        if pieceinsquare is not None:
                            if pieceinsquare.color:
                                white += 1
                else:
                    # checks if enemy is at attackable squares
                    for square in squares:
                        pieceinsquare = board.piece_at(square)
                        if pieceinsquare is not None:
                            if not pieceinsquare.color:
                                black += 1
        return white - black
#get a score for the position the pieces take on the scoreboard
    def get_piece_position_score(self, board: chess.Board):
        white = 0
        black = 0
        for x in range(64):
            piece = board.piece_at(x)
            if piece is not None:
                table = listoftable.get(str(piece).upper())
                if table is not None:
                    table2 = table.flatten()
                    if piece.color == True:
                        white += table2[x]
                    elif piece.color == False:
                        black += table2[63 - x]
        return white - black

#Calculate the weighted amount of white pieces minus the amount of black pieces
    def amount_of_pieces_score(self, board):
        n_white = 0
        n_white += len(board.pieces(piece_type=chess.PAWN, color=chess.WHITE))
        n_white += len(board.pieces(piece_type=chess.BISHOP, color=chess.WHITE)) * 3
        n_white += len(board.pieces(piece_type=chess.KNIGHT, color=chess.WHITE)) * 3
        n_white += len(board.pieces(piece_type=chess.ROOK, color=chess.WHITE)) * 5
        n_white += len(board.pieces(piece_type=chess.QUEEN, color=chess.WHITE)) * 9
        n_white += len(board.pieces(piece_type=chess.KING, color=chess.WHITE)) * 100


        n_black = 0
        n_black += len(board.pieces(piece_type=chess.PAWN, color=chess.BLACK))
        n_black += len(board.pieces(piece_type=chess.BISHOP, color=chess.BLACK)) * 3
        n_black += len(board.pieces(piece_type=chess.KNIGHT, color=chess.BLACK)) * 3
        n_black += len(board.pieces(piece_type=chess.ROOK, color=chess.BLACK)) * 5
        n_black += len(board.pieces(piece_type=chess.QUEEN, color=chess.BLACK)) * 9
        n_black += len(board.pieces(piece_type=chess.KING, color=chess.BLACK)) * 100
        scoreAmountOfPieces = n_white - n_black
        return scoreAmountOfPieces

    def board_value(self, board: chess.Board):
        # if winning move, take it
        if board.is_checkmate():
            return 9999999
        else:
            score_amount_of_pieces = self.amount_of_pieces_score(board)
            score_attacks_defends_covered_combined = self.get_pieces_squares_covered_combined(board)
            total_score = score_amount_of_pieces * 25 + score_attacks_defends_covered_combined
        return total_score
