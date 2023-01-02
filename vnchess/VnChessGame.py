from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .VnChessLogic import Board
import numpy as np

# Index action space to 5 * 5 = 25 size array.

class VnChessGame(Game):
    square_content = {
        -1: "X",
         0: "-",
         1: "O"
    }




    @staticmethod
    def getSquarePiece(piece):
        return VnChessGame.square_content[piece]
    
    def __init__(self, n=5):
        self.n = n
    
    def getInitBoard(self):
        b = Board(self.n)
        return np.array(b.pieces)
    
    def getBoardSize(self):
        #Returns shape (a, b) tuple
        return (self.n, self.n)
    
    def getActionSize(self):
        # Return number of maximum actions can get from board
        return 112

    def getNextState(self, board, player, action):
        # if player takes action, on board, return next (board, player)
        # Action must be a valid move
        # Action is array (flatten)
        b = Board(self.n)
        b.pieces = np.copy(board)
        b.execute_move(action, player)
        return (b.pieces, -player)

    def getValidMoves(self, board, player):
        # Return fixed size vector
        pass

    def getGameEnded(self, board, player):
        '''
        Return result of game played.
        0 indicated not end
        1 if player 1 won,
        -1 if player 1 lost
        player = 1
        '''
        board_results = np.sum(board)
        return -1 if board_results == -1 else 1 if board_results == 1 else 0
    
    def getCanonicalForm(self, board, player):
        '''
        Return state of player view
        '''
        return player * board
    
    def getSymmetries(self, board, pi):
        pass
    
    def stringRepresentation(self, board):
        return board.tostring()

    def stringRepresentationReadable(self, board):
        board_s = "".join(self.square_content[square] for row in board for square in row)
        return board_s
    
    def getScore(self, board, player):
        '''
        init of q value
        '''
        b = Board(self.n)
        b.pieces = np.copy(board)
        return b.countDiff(player)
    
    @staticmethod
    def display(board):
        n = board.shape[0]
        print("   ", end = "")
        for y in range(n):
            print(y, end = " ")
        print("")
        print("---"*5)
        for y in range(n):
            print(y, "|", end="")
            for x in range(n):
                piece = board[y][x] #get the piece to print
                print(VnChessGame.square_content[piece], end=" ")
            print("|")
        print("---"*5)