'''
Board class:
Board data:
    1=X, -1=O, 0=empty, or something:)))
    first dim is column, 2nd is row:
        pieces[1][3] is the square in column 2,
        at the opposite end of the board in row 4.
Squares are stored and manipulated as (x,y) tuples.
x is the column index, y is the row index.
'''

from .VnChessUtils import get_all_actions, get_traps, get_actions_of_chessman, blind_move, get_avail_half_actions, get_at, get_surrounded_chesses, surround

class Board():
    def __init__(self, n=5):
        '''
        Set up initial board configuration.
        params: n: size of board
        '''
        self.n = n
        # Create the empty board array.
        self.pieces = [[1, 1, 1, 1, 1],
                        [1, 0, 0, 0, 1],
                        [1, 0, 0, 0, -1],
                        [-1, 0, 0, 0, -1],
                        [-1, -1, -1, -1, -1]]
        self.moves = []
    
    #Add [][] indexer syntax to the Board.
    def __getitem__(self, index):
        return self.pieces[index]
    
    def countDiff(self, type):
        '''
        Couts the # piees of the given type chessman
        (1 for X, -1 for O, 0 for empty spaces) or something ;))
        '''
        count = 0
        for i in range(self.n):
            for j in range(self.n):
                if self[i][j] == type:
                    count += 1
                elif self[i][j] == -type:
                    count -= 1
        return count
    
    def get_last_move(self):
        return None if len(self.moves) == 0 else self.moves[-1]

    def get_legal_moves(self, type):
        '''
        Returns all the legal moves for the given chess types.
        (1 for X, -1 for O)
        '''
        last_move = self.get_last_move()
        if last_move is not None:
            last_start, _ = last_move
            traps_move = get_traps(self.pieces, type, last_start)
            if len(traps_move) != 0:
                return traps_move

        all_actions = []
        for i in range(self.n):
            for j in range(self.n):
                if self[i][j] == type:
                    actions = get_actions_of_chessman(self.pieces,(i,j))
                    all_actions += [((i,j), blind_move((i,j),action)) for action in actions]
        
        return all_actions
    
    def has_legal_moves(self, type):
        for i in range(self.n):
            for j in range(self.n):
                if self[i][j] == type:
                    newmoves = self.get_moves_for_square((i,j))
                    if len(newmoves) > 0:
                        return True
        return False
    
    def get_moves_for_square(self, square):
        '''
        Returns all legal moves start at index square
        '''
        (x,y) = square
        type = self[x][y]

        #skip empty source squares.
        if type == 0:
            return None
        
        #search all possible directions:
        return get_actions_of_chessman(self.pieces,square)
    
    def execute_move(self, move, type):
        '''
        Perform given move on the board
        '''
        start, end = move
        i, j = start
        if self[i][j] != type:
            raise Exception("Start position is not valid")
        
        # i, j = start
        self[i][j] = 0

        i, j = end
        self[i][j] = type
        
        # Cap nhat ganh, vay
        for action in get_avail_half_actions(end):
            pos1, pos2 = blind_move(end, action), blind_move(end, action.get_opposite())

            type1, type2 = get_at(self.pieces, pos1), get_at(self.pieces, pos2)

            if type1 == type2 == -type:
                i1, j1 = pos1
                i2, j2 = pos2
                self[i1][j1] = type
                self[i2][j2] = type
        surround_teams = get_surrounded_chesses(self.pieces, type)
        self.pieces = surround(self.pieces, surround_teams, type)
    
    @staticmethod
    def _increment_move(move, direction, n):
        '''
        Geneator expression for incrementing moves
        '''
        move = list(map(sum, zip(move, direction)))

        while all(map(lambda x: 0 <= x < n, move)):
            yield move
            move=list(map(sum,zip(move,direction)))