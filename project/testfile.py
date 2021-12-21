import numpy
import chess
import chess.svg
import random

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


def get_score_of_piece(value):
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
        return 10

def get_piece_defend(board: chess.Board):
    white = 0
    black = 0
    for x in range(64):
        piece = board.piece_at(x)
        if piece is not None:
            # gets location of all attackable places
            squares = (board.attacks(x))
            if piece.color:
                # checks white is at attackable squares
                for square in squares:
                    pieceinsquare = board.piece_at(square)
                    if pieceinsquare is not None:
                        if pieceinsquare.color:
#                           piecetype = pieceinsquare
#                           multiplier = get_score_of_piece(str(piecetype))
                            white += 1
            else:
                # checks if enemy is at attackable squares
                for square in squares:
                    pieceinsquare = board.piece_at(square)
                    if pieceinsquare is not None:
                        if not pieceinsquare.color:
#                         piecetype = pieceinsquare
#                         multiplier = get_score_of_piece(str(piecetype))
                         black += 1
    print("white: " + str(white))
    print("black: " + str(black))
    return white - black


def get_piece_attacks(board):
    white = 0
    black = 0
    for f in range(1):
        x = 45
        piece = board.piece_at(x)
        print(piece)
        if piece is not None:
            if piece.color:
                # gets location of all attackable places
                squares = (board.attacks(x))
                # checks if enemy is at attackable squares
                for square in squares:
                    pieceinsquare = board.piece_at(square)
                    if pieceinsquare is not None:
                        if not pieceinsquare.color:
                            piecetype = pieceinsquare
                            multiplier = get_score_of_piece(str(piecetype))
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
                            multiplier = get_score_of_piece(str(piecetype))
                            black += 1 * multiplier
    return white - black


def get_piece_position_score(board: chess.Board):
    white = 0
    black = 0
    for x in range(64):
        piece = board.piece_at(x)
        if piece is not None:
            table = listoftable.get(str(piece).upper())
            if table is not None:
                table2 = table.flatten()
                table2 = numpy.flip(table2)
                if piece.color == True:
                    white += table2[x]
                elif  piece.color == False:
                    black += table2[63 - x]
    return white - black


#board = chess.Board("r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq -  4")
board = chess.Board("rnb1k2r/ppp2ppp/5n2/3q4/1b1P4/2N5/PP3PPP/R1BQKBNR w KQkq - 3 7")
print(board)
direction = board.attacks(35)
print(direction)
#board = chess.Board()
#moves = list(board.legal_moves)
#for i in range(35):
 #   moves = list(board.legal_moves)
  #  choice = random.randint(0, 3)
  #  board.push(moves[choice])

    #print("score" + str(i) + ": " + str(get_piece_position_score(board)))



#print("score1: " + str(get_piece_position_score(board)))
#board.push(moves[2])
#score = get_piece_position_score(board)
"""print(board)
squares = board.king(False)
print(get_piece_attacks(board))"""
""""print("score2: " + str(get_piece_position_score(board)))
squares = board.attacks(chess.E4)
print(board.attackers(chess.WHITE, chess.E8))
piece = board.piece_at(53)"""
