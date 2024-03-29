import numpy as np
import copy

# =============================================================================
# Parameters
# =============================================================================

# import matplotlib.pyplot as plt
# a = [1,1,1,2,2,2,2,3,3,3,3,3,5,6,6,6,7,7,7,7,7,8,10,22,25,25,33,21,30,12,17,14,23,24,23,24,43,22,15,34,43,22,38,41,35,25,1,1,1,2,2,2,2,3,3,3,3,3,5,6,6,6,7,7,7,7,7,8,10,22,25,25,33,21,30,12,17,14,23,24,23,24,43,22,15,34,43,22,38,41,35,25]
# numbins = max(a) - min(a) + 1

# plt.figure(figsize = (6,6))
# plt.hist(a, density = False, rwidth = 0.7, bins = numbins)



# creating the bar plot
# counts, edges = np.histogram(a)  # density=False would make counts
# plt.plot(edges[:-1],counts)
# print(counts)

# , align='mid'
range_8 = range(8)
MATE_EVALSCORE = 1e4

# =============================================================================
# Piece-Square tables
# =============================================================================

################################ PAWNS #################################

### WHITE pawns ###

W_pawnTable = np.array([[ 0,  0,  0,  0,  0,  0,  0,  0],
                        [50, 50, 50, 50, 50, 50, 50, 50],
                        [10, 10, 20, 30, 30, 20, 10, 10],
                        [ 5,  5, 10, 25, 25, 10,  5,  5],
                        [ 0,  0,  0, 20, 20,  0,  0,  0],
                        [ 5, -5,-10,  0,  0,-10, -5,  5],
                        [ 5, 10, 10,-20,-20, 10, 10,  5],
                        [ 0,  0,  0,  0,  0,  0,  0,  0]],dtype=int)

### BLACK pawns ###

B_pawnTable = np.flip(W_pawnTable, axis=0) 

################################ KNIGHTS #################################

### WHITE knights ###

W_knightTable = np.array([[-50,-40,-30,-30,-30,-30,-40,-50],
                            [-40,-20,  0,  0,  0,  0,-20,-40],
                            [-30,  0, 10, 15, 15, 10,  0,-30],
                            [-30,  5, 15, 20, 20, 15,  5,-30],
                            [-30,  0, 15, 20, 20, 15,  0,-30],
                            [-30,  5, 10, 15, 15, 10,  5,-30],
                            [-40,-20,  0,  5,  5,  0,-20,-40],
                            [-50,-40,-30,-30,-30,-30,-40,-50,]],dtype=int)

### BLACK knights ###

B_knightTable = np.flip(W_knightTable, axis=0) 

################################ BISHOPS #################################

### WHITE bishops ###

W_bishopTable = np.array([[-20,-10,-10,-10,-10,-10,-10,-20],
                            [-10,  0,  0,  0,  0,  0,  0,-10],
                            [-10,  0,  5, 10, 10,  5,  0,-10],
                            [-10,  5,  5, 10, 10,  5,  5,-10],
                            [-10,  0, 10, 10, 10, 10,  0,-10],
                            [-10, 10, 10, 10, 10, 10, 10,-10],
                            [-10,  5,  0,  0,  0,  0,  5,-10],
                            [-20,-10,-10,-10,-10,-10,-10,-20,]],dtype=int)

### BLACK bishops ###

B_bishopTable = np.flip(W_bishopTable, axis=0)

################################ ROOKS #################################

### WHITE rooks ###

W_rookTable = np.array([[  0,  0,  0,  0,  0,  0,  0,  0],
                             [ 5, 10, 10, 10, 10, 10, 10,  5],
                             [-5,  0,  0,  0,  0,  0,  0, -5],
                             [-5,  0,  0,  0,  0,  0,  0, -5],
                             [-5,  0,  0,  0,  0,  0,  0, -5],
                             [-5,  0,  0,  0,  0,  0,  0, -5],
                             [-5,  0,  0,  0,  0,  0,  0, -5],
                             [ 0,  0,  0,  5,  5,  0,  0,  0]],dtype=int)

### BLACK rooks ###

B_rookTable = np.flip(W_rookTable, axis=0)

################################ QUEEN #################################

### WHITE queen ###

W_queenTable = np.array([[-20,-10,-10, -5, -5,-10,-10,-20],
                            [-10,  0,  0,  0,  0,  0,  0,-10],
                            [-10,  0,  5,  5,  5,  5,  0,-10],
                            [ -5,  0,  5,  5,  5,  5,  0, -5],
                            [  0,  0,  5,  5,  5,  5,  0, -5],
                            [-10,  5,  5,  5,  5,  5,  0,-10],
                            [-10,  0,  5,  0,  0,  0,  0,-10],
                            [-20,-10,-10, -5, -5,-10,-10,-20]],dtype=int)

### BLACK queen ###

B_queenTable = np.flip(W_queenTable, axis=0)

################################ KING #################################

### WHITE king - MIDDLE game ### 

W_kingTable_mid = np.array([[-30,-40,-40,-50,-50,-40,-40,-30],
                                [-30,-40,-40,-50,-50,-40,-40,-30],
                                [-30,-40,-40,-50,-50,-40,-40,-30],
                                [-30,-40,-40,-50,-50,-40,-40,-30],
                                [-20,-30,-30,-40,-40,-30,-30,-20],
                                [-10,-20,-20,-20,-20,-20,-20,-10],
                                [ 20, 20,  0,  0,  0,  0, 20, 20],
                                [ 20, 30, 10,  0,  0, 10, 30, 20]],dtype=int)

### BLACK king - MIDDLE game ### 

B_kingTable_mid = np.flip(W_kingTable_mid, axis=0)

#-------------------------------------------------

### WHITE king - END game ### 

W_kingTable_end = np.array([[-50,-40,-30,-20,-20,-30,-40,-50],
                            [-30,-20,-10,  0,  0,-10,-20,-30],
                            [-30,-10, 20, 30, 30, 20,-10,-30],
                            [-30,-10, 30, 40, 40, 30,-10,-30],
                            [-30,-10, 30, 40, 40, 30,-10,-30],
                            [-30,-10, 20, 30, 30, 20,-10,-30],
                            [-30,-30,  0,  0,  0,  0,-30,-30],
                            [-50,-30,-30,-30,-30,-30,-30,-50]],dtype=int)

### BLACK king - END game ### 

B_kingTable_end = np.flip(W_kingTable_end, axis=0)

# =============================================================================
# Dictionaries
# =============================================================================

# instead of 2*col - 1
signCol = {
    0: -1,
    1: 1,
    }


# translating column letters to numbers
columnNum = {
    "a": 0,
    "b": 1,
    "c": 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7,
}

# translating numbers to column letters
numColumn = {
    0: "a",
    1: "b",
    2: "c",
    3: 'd',
    4: 'e',
    5: 'f',
    6: 'g',
    7: 'h',
}

# promotion piece number
promotion = {
    "q": 2,
    "r": 3,
    "b": 4,
    'n': 5,
}

# promotion piece number
numPromotion = {
    2: "q",
    3: "r",
    4: "b",
    5: 'n',
}

# Piece evaluation
pieceEval = {
    # black
    (0, 0): 0,   # empty
    (1, 0): 0,   # King
    (2, 0): -900,  # Queen
    (3, 0): -500,  # Rook
    (4, 0): -300,  # Bishop
    (5, 0): -300,  # Knight
    (6, 0): -100,  # Pawn
    # white
    (0, 1): 0,
    (1, 1): 0,
    (2, 1): 900,
    (3, 1): 500,
    (4, 1): 300,  # Bishop
    (5, 1): 300,  # Knight
    (6, 1): 100,
    }

gameStatus ={
    0: "play",
    1: "CHECKMATE",
    2: "DRAW by insufficient material",
    3: "STALEMATE",
    }

#------------------------------------------------------------------------------
# Piece-square table access dictionaries

mid_pieceTable ={
    
    # black

    (1, 0): B_kingTable_mid,# King MID
    (2, 0): B_queenTable,   # Queen
    (3, 0): B_rookTable,    # Rook
    (4, 0): B_bishopTable,  # Bishop
    (5, 0): B_knightTable,  # Knight
    (6, 0): B_pawnTable,    # Pawn
    #--------------------------------
    # white
    
    (1, 1): W_kingTable_mid,# King MID
    (2, 1): W_queenTable,   # Queen
    (3, 1): W_rookTable,    # Rook
    (4, 1): W_bishopTable,  # Bishop
    (5, 1): W_knightTable,  # Knight
    (6, 1): W_pawnTable,    # Pawn
    }

end_pieceTable = copy.deepcopy(mid_pieceTable)
end_pieceTable[(1,0)] = B_kingTable_end
end_pieceTable[(1,1)] = W_kingTable_end

pieceTable ={
    "m": mid_pieceTable,
    "e": end_pieceTable,
    }

#------------------------------------------------------------------------------