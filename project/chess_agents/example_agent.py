from project.chess_agents.agent import Agent
import chess
from project.chess_utilities.utility import Utility
import time
import random

"""An example search agent with two implemented methods to determine the next move"""
class ExampleAgent(Agent):

    # Initialize your agent with whatever parameters you want
    def __init__(self, utility: Utility, time_limit_move: float) -> None:
        super().__init__(utility, time_limit_move)
        self.name = "Example search agent"
        self.author = "J. Duym & A. Troch"


    def minimax(self,board, depth, maximizingPlayer):
        if depth == 0 | board.is_checkmate():
            return self.utility.board_value(board)

        if maximizingPlayer == True:
            maxEval = -9999
            for move in list(board.legal_moves):
                board.push(move)
                eval = self.minimax(board, depth-1, False)
                board.pop()
                maxEval = max(eval, maxEval)
            return maxEval

        elif maximizingPlayer == False:
            minEval = 9999
            for move in list(board.legal_moves):
                board.push(move)
                eval = self.minimax(board, depth - 1, True)
                board.pop()
                minEval = min(eval, minEval)
            return minEval

    def minimaxprune(self, board, depth, maximizingPlayer, alpha, beta):
        if depth == 0 | board.is_checkmate():
            return self.utility.board_value(board)

        if maximizingPlayer:
            maxEval = -9999
            for move in list(board.legal_moves):
                board.push(move)
                eval = self.minimaxprune(board, depth - 1, False, alpha, beta)
                board.pop()
                maxEval = max(eval, maxEval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval

        else:
            minEval = +9999
            for move in list(board.legal_moves):
                board.push(move)
                eval = self.minimaxprune(board, depth - 1, True, alpha, beta)
                board.pop()
                minEval = min(eval, minEval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval


    def calculate_move(self, board: chess.Board):
        start_time = time.time()

        # If the agent is playing as black, the utility values are flipped (negative-positive)
        if board.turn == chess.WHITE:
            flip_value = 1
            maximazingplayer = True
        else:
            flip_value = -1
            maximazingplayer = False


        best_move = random.sample(list(board.legal_moves), 1)[0]
        best_utility = -9999
        # Loop trough all legal moves
        valuelist = []
        for move in list(board.legal_moves):

            # Check if the maximum calculation time for this move has been reached
         #   if time.time() - start_time > self.time_limit_move:
          #      print("time limit reached")
           #     break
            # Play the move
            board.push(move)
            # Determine the value of the board after this move
            value = self.minimaxprune(board, 2, False, -9999, 9999)
            valuelist.append(round(value, 2))
            # If this is better than all other previous moves, store this move and its utility
            if value > best_utility:
                best_move = move
                best_utility = value
            # Revert the board to its original state
            board.pop()
        print(valuelist)
        print("best utility: " + str(best_utility))
        return best_move
"""

#This agent does not perform any searching, it sinmply iterates trough all the moves possible and picks the one with the highest utility
    def calculate_move(self, board: chess.Board):
        
        start_time = time.time()
        
        # If the agent is playing as black, the utility values are flipped (negative-positive)
        flip_value = 1 if board.turn == chess.WHITE else -1
        
        best_move = random.sample(list(board.legal_moves), 1)[0]
        best_utility = 0
        # Loop trough all legal moves
        for move in list(board.legal_moves):
            # Check if the maximum calculation time for this move has been reached
            if time.time() - start_time > self.time_limit_move:
                break
            # Play the move
            board.push(move)
            # Determine the value of the board after this move
            score,score_board,score_piece_attacks,score_amount_of_pieces = self.utility.board_value(board)
            print("score: " + str(score))
            print("score_board: " + str(score_board))
            print("score_piece_attacks: " + str(score_piece_attacks))
            print("score_amount_of_pieces: " + str(score_amount_of_pieces))
           # value = flip_value * self.utility.board_value(board)
            value = flip_value * score
            # If this is better than all other previous moves, store this move and its utility
            if value > best_utility:
                best_move = move
                best_utility = value
            # Revert the board to its original state
            board.pop()
        return best_move
"""