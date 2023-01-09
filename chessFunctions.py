import numpy as np
import random
import time
import copy

# importing functions
from global_parameters import *
from legal_checks import *
from ui import *

# print(dir(legal_checks))
# =============================================================================
# Piece initialization function
# =============================================================================

def initialization():

    # 3D board
    boardState = np.zeros((8, 8, 2), dtype=int)

    # Set up 3D matrix

    # A[r,c,0] = piece id
    # A[r,c,1] = piece color

    for i in [0, 7]:  # pieces with 3+ value

        # black(0) & white(7) pieces ids
        boardState[i, 4, 0] = 1  # king
        boardState[i, 3, 0] = 2  # queen
        boardState[i, 0, 0] = 3  # rook L
        boardState[i, 7, 0] = 3  # rook R
        boardState[i, 2, 0] = 4  # bishop L
        boardState[i, 5, 0] = 4  # bishop R
        boardState[i, 1, 0] = 5  # knight L
        boardState[i, 6, 0] = 5  # knight R

    for j in range_8:  # columns: range(n) is 0:n-1

        # black pawns
        boardState[1, j, 0] = 6  # id
        boardState[1, j, 1] = 0  # color

        # white pawns
        boardState[6, j, 0] = 6  # id
        boardState[6, j, 1] = 1  # color

        # color of black 3+ value pieces
        boardState[0, j, 1] = 0  # black

        # color of white 3+ value pieces
        boardState[7, j, 1] = 1  # white


    # initialize king's position
    positionKing_W = [7,4] # e1
    positionKing_B = [0,4] # e8
    # both kings in array -> black: bothKings[0], white: bothKings[1]
    positionKings = [positionKing_B, positionKing_W] 


    # initialize pieces
    BWpieces = [set(),set()]

    for i in range(8): # rows
        for j in range(8): # columns
            if boardState[i,j,0] != 0:
                BWpieces[boardState[i,j,1]].add((i,j))

    
    # castling status and pieces
    castlingStatus = {
        # black (r,c)
        (0): False, # black castled
        (0,4): 0, # "e8K"  King
        (0,7): 0, # "h8R"  short - right
        (0,0): 0, # "a8R"  long - left

        # white
        (1): False, # white castled
        (7,4): 0, # "e1K"  King
        (7,7): 0, # "h1R"  short - right
        (7,0): 0, # "a1R"  long - left
        }
    
    evalPoints = 0
    
    
    return boardState, positionKings, BWpieces, castlingStatus, evalPoints


# array slicing
# print(boardState[:,:,0]) # 2D chess ids
# print(boardState[:,:,1]) # 2D colors (0: black, 1:white)

# =============================================================================
# Functions: OLD_allLegal, allLegal, DrawStalemateMate
# =============================================================================

#OAL##########################################################################################

def OLD_allLegal(boardState, color, positionKings, BWpieces,castlingStatus):

    
    
    listMoves = []

    listCol = BWpieces[color]
    oppColor = 1-color

    move = np.zeros(5, dtype=int)
    for piece in copy.copy(listCol):
        i, j = piece  # i = 0, j = 1
        move[0:2] = piece

        for k in range_8:  # destination rows
            for l in range_8:  # columns
                if (boardState[k, l, 1] == oppColor) or boardState[k, l, 0] == 0:
                    # locate the pieces of same color as the engine's turn
                    move[2:4] = [k, l]

                    # promotion pawns
                    if boardState[i, j, 0] == 6 and ((i == 1 and k == 0) or (i == 6 and k == 7)):
                        for prom in [2, 3, 4, 5]:
                            move[4] = prom

                            if checkLegal(move, boardState, color, positionKings, BWpieces,castlingStatus):
                                # !!!! fix this
                                listMoves.append(np.copy(move))

                    else:
                        move[4] = 0
                        if checkLegal(move, boardState, color, positionKings, BWpieces,castlingStatus):
                            listMoves.append(np.copy(move))

    return listMoves

#AL##########################################################################################

def allLegal(boardState, color, positionKings, BWpieces,castlingStatus):

    finalList = []
    listCol = BWpieces[color]

    for piece in copy.copy(listCol):

        legalMoves = generateLegal(
            piece, boardState, color, positionKings, BWpieces,castlingStatus)

        finalList.extend(legalMoves)

    return finalList

#DSM##########################################################################################

def DrawStalemateMate(boardState,color,positionKings,BWpieces,castlingStatus,legalMoves=None):

    # 0 = play
    # 1 = mate
    # 2 = draw by insufficient material
    # 3 = stalemate
    # 4 = in check
    # 5 = opponent in check

    # passes legal moves if calculated previously
    if legalMoves == None:
        # start = time.time()
        legalMoves = allLegal(
            boardState, color, positionKings, BWpieces,castlingStatus)
        # end = time.time()

    listCol = BWpieces[color]
    listOpp = BWpieces[1-color]

    # DRAW by INSUFFICIENT MATERIAL
    # check if only kings are left
    # check if only knights or bishops left
    if (len(listCol) == 1 or (len(listCol) == 2 and ((4 in listCol) or (5 in listCol)))):
        if (len(listOpp) == 1 or (len(listOpp) == 2 and ((4 in listOpp) or (5 in listOpp)))):
            return 2

    myKcheck = sqr_under_attack(
        boardState, color, positionKings[color], BWpieces,castlingStatus)

    if legalMoves == []:

        # Stalemate check
        if not myKcheck:
            return 3

        # Mate check
        else:
            return 1

    if myKcheck:
        return 4

    OppKcheck = sqr_under_attack(
        boardState, 1-color, positionKings[1-color], BWpieces,castlingStatus)
    if OppKcheck:
        return 5

    return 0


# =====================================================================
# Decision functions: move ordering, minimax, alphabeta pruning
# =====================================================================

#OM##########################################################################################

def orderMoves(boardState, positionKings, BWpieces, legalMoves,color,castlingStatus):

    evalList = []
    for move in legalMoves:
        
        kingsExp = np.copy(positionKings)
        
        # expected board with last user input
        cpc, dpc = movePiece(move, boardState, kingsExp, BWpieces,castlingStatus)
        evalList.append(sortingEval(boardState))
        undoMove(move, cpc, dpc, boardState, BWpieces,castlingStatus)

    if color == 1: # white
        sortedMoves = [legalMoves[i] for i in np.argsort(evalList)[::-1]]
        return sortedMoves
    
    else: # black
        sortedMoves = [legalMoves[i] for i in np.argsort(evalList)]
        return sortedMoves

#MM##########################################################################################

def minimax(boardState, color, positionKings, depth, BWpieces):

    legalMoves = allLegal(boardState, color, positionKings, BWpieces)

    if depth == 0 or legalMoves == []:
        return Eval(boardState, color, positionKings, BWpieces, legalMoves), None

    if color == 1:  # white's move

        max_evalScore = -np.Inf
        max_move = None

        for move in legalMoves:
            piecesExp = copy.deepcopy(BWpieces)
            kingsExp = np.copy(positionKings)
            # expected board with last user input
            boardExp = movePiece(move, np.copy(
                boardState), kingsExp, piecesExp,evalPoints)
            eval_of_move = minimax(
                boardExp, 1-color, kingsExp, depth-1, piecesExp)[0]

            if eval_of_move >= max_evalScore:
                max_evalScore = eval_of_move
                max_move = move

        return max_evalScore, max_move

    if color == 0:  # black's move

        min_evalScore = np.Inf
        min_move = None

        for move in legalMoves:
            piecesExp = copy.deepcopy(BWpieces)
            kingsExp = np.copy(positionKings)
            # expected board with last user input
            boardExp = movePiece(move, np.copy(
                boardState), kingsExp, piecesExp,evalPoints)
            eval_of_move = minimax(
                boardExp, 1-color, kingsExp, depth-1, piecesExp)[0]

            if eval_of_move <= min_evalScore:
                min_evalScore = eval_of_move
                min_move = move

        return min_evalScore, min_move

# def negaAB(boardState, color, positionKings, depth, α, β, BWpieces):

#     legalMoves = allLegal(boardState, color, positionKings, BWpieces)

#     if depth == 0 or legalMoves == []:
#         return signCol[color]*Eval(boardState, color, positionKings, BWpieces, legalMoves), None

#     legalMoves = orderMoves(boardState, positionKings,BWpieces, legalMoves,color)

#     max_evalScore = -np.Inf
#     max_move = None

#     for move in legalMoves:
#         #piecesExp = copy.deepcopy(BWpieces)
#         kingsExp = np.copy(positionKings)

#         # expected board with last user input
#         cpc, dpc = movePiece(move, boardState, kingsExp, BWpieces)

#         eval_of_move = -negaAB(
#             boardState, 1-color, kingsExp, depth-1, -β, -α, BWpieces)[0]
        
#         undoMove(move, cpc, dpc, boardState, BWpieces)

#         if eval_of_move >= max_evalScore:
#             max_evalScore = eval_of_move
#             max_move = move

#         # if max eval_Sc > a, then update alpha w/ max eval_Sc
#         # if the reverse, a stays the same
#         α = max(α, max_evalScore)
        
#         if α >= β:
#             break

#     return max_evalScore, max_move

#MSN##########################################################################################

def moveSequence_negaAB(boardState_,color,positionKings_,depth,BWpieces_,evalPoints,castlingStatus_):
    
    sequence = []
    boardState = np.copy(boardState_)
    positionKings = copy.deepcopy(positionKings_)
    BWpieces = copy.deepcopy(BWpieces_)
    castlingStatus = copy.deepcopy(castlingStatus_)
    
    α,β, = -np.Inf,np.Inf 
    
    for i in reversed(range(1,depth)):
        color = 1 - color
        move = negaAB(boardState,color,positionKings,i,α,β,BWpieces,evalPoints,castlingStatus)[1]
        sequence.append(move)
        movePiece_EVAL(move,boardState,positionKings,BWpieces,evalPoints,castlingStatus)
        
    return sequence

#NAB#########################################################################################


def negaAB(boardState, color, positionKings, depth, α, β, BWpieces, evalPoints,castlingStatus):

    legalMoves = allLegal(boardState, color, positionKings, BWpieces,castlingStatus)

    if depth == 0 or legalMoves == []:
        return signCol[color]*Eval(boardState, color, positionKings, BWpieces,castlingStatus, legalMoves), None

    legalMoves = orderMoves(boardState, positionKings,BWpieces, legalMoves,color,castlingStatus)

    max_evalScore = -np.Inf
    max_move = None

    for move in legalMoves:
        #piecesExp = copy.deepcopy(BWpieces)
        kingsExp = np.copy(positionKings)
        
        # expected board with last user input
        cpc, dpc, evalPoints = movePiece_EVAL(move, boardState, kingsExp, BWpieces,evalPoints,castlingStatus)

        eval_of_move = -negaAB(
            boardState, 1-color, kingsExp, depth-1, -β, -α, BWpieces, evalPoints,castlingStatus)[0]
        
        evalPoints = undoMove_EVAL(move, cpc, dpc, boardState, BWpieces,evalPoints,castlingStatus)

        if eval_of_move >= max_evalScore:
            max_evalScore = eval_of_move
            max_move = move

        # if max eval_Sc > a, then update alpha w/ max eval_Sc
        # if the reverse, a stays the same
        α = max(α, max_evalScore)
        
        if α >= β:
            break

    return max_evalScore, max_move

#AB##########################################################################################

def alphabeta(boardState, color, positionKings, depth, α, β, BWpieces,castlingStatus):

    legalMoves = allLegal(boardState, color, positionKings, BWpieces,castlingStatus)

    if depth == 0 or legalMoves == []:
        return Eval(boardState, color, positionKings, BWpieces,castlingStatus, legalMoves), None

    legalMoves = orderMoves(boardState, positionKings,
                            BWpieces, legalMoves,color,castlingStatus)

    if color == 1:  # white's move

        max_evalScore = -np.Inf
        max_move = None

        for move in legalMoves:
            #piecesExp = copy.deepcopy(BWpieces)
            kingsExp = np.copy(positionKings)
            
            # expected board with last user input
            cpc, dpc = movePiece(move, boardState, kingsExp, BWpieces,castlingStatus)
            eval_of_move = alphabeta(
                boardState, 1-color, kingsExp, depth-1, α, β, BWpieces,castlingStatus)[0]
            undoMove(move, cpc, dpc, boardState, BWpieces,castlingStatus)

            if eval_of_move >= max_evalScore:
                max_evalScore = eval_of_move
                max_move = move

            if max_evalScore > β:
                break

            # if max eval_Sc > a, then update alpha w/ max eval_Sc
            # if the reverse, a stays the same
            α = max(α, max_evalScore)

        return max_evalScore, max_move

    if color == 0:  # black's move

        min_evalScore = np.Inf
        min_move = None

        for move in legalMoves:
            #piecesExp = copy.deepcopy(BWpieces)
            kingsExp = np.copy(positionKings)
            
            # expected board with last user input
            cpc, dpc = movePiece(move, boardState, kingsExp, BWpieces,castlingStatus)
            eval_of_move = alphabeta(
                boardState, 1-color, kingsExp, depth-1, α, β, BWpieces,castlingStatus)[0]
            undoMove(move, cpc, dpc, boardState, BWpieces,castlingStatus)

            if eval_of_move <= min_evalScore:
                min_evalScore = eval_of_move
                min_move = move

            if min_evalScore < α:
                break

            β = min(β, min_evalScore)

        return min_evalScore, min_move
# =====================================================================
# Evaluation functions: sortingEval, Eval
# =====================================================================

#SE##########################################################################################

def sortingEval(boardState):

    # calculates total evaluation score
    sumPoints = 0

    # total number of bl/wh pieces
    Npieces_BL = 0
    Npieces_WH = 0
    
    for i in range_8:
        for j in range_8:
            b = boardState[i, j, :]
            p = b[0]
            c = b[1]
            if c == 0 and p != 0:
                Npieces_BL += 1
                
            if c == 1 and p != 0:
                Npieces_WH += 1
                    

    for i in range_8:
        for j in range_8:
            b = boardState[i, j, :]
            c = b[1]

            # add points for moving pawn towards promotion
            if b[0] == 6 and i < 7:
                if c == 0 and Npieces_BL < 12:  # black
                    BLprom = -(1e-5)*(i-1)
                    sumPoints += BLprom

                if c == 1 and Npieces_WH < 12:  # white
                    WHprom = (1e-5)*(6-i)
                    sumPoints += WHprom

            # add points when pawns in center
            if i in range(2, 6) and j in range(2, 6) and b[0] != 0:
                centerPoints = (1e-4)*signCol[c]
                sumPoints += centerPoints

            # piece, color
            sumPoints += pieceEval[(b[0],c)]

    return sumPoints  # output evaluation score

#E##########################################################################################

# TIME EVERYTHING in main loop
def Eval(boardState, color, positionKings, BWpieces,castlingStatus,legalMoves=None):

    # 0 = play
    # 1 = mate
    # 2 = draw by insufficient material
    # 3 = stalemate
    # 4 = player in check
    # 5 = opponent in check

    # checks for game status
    status = DrawStalemateMate(boardState, color, positionKings,BWpieces,castlingStatus,legalMoves)

    if status == 1:
        # black or white gets mated
        return (1 - 2*color)*np.Inf  # white or black wins

    if status == 2 or status == 3:
        return 0

    # calculates total evaluation score
    sumPoints = 0

    # player's king in check
    if status == 4:
        sumPoints += -(1e-1)*signCol[color]

    # opponent's king in check
    if status == 5:
        sumPoints += (1e-1)*signCol[color]

    # add points for castling
    if castlingStatus[(color)]:
        sumPoints += (5e-1)*signCol[color]


    # total number of bl/wh pieces
    Npieces_BL = len(BWpieces[0])
    Npieces_WH = len(BWpieces[1])


    for i in range_8:
        for j in range_8:
            b = boardState[i, j, :]
            c = b[1]

            # add points for moving pawn towards promotion
            if b[0] == 6 and i < 7:
                if c == 0 and Npieces_BL < 12:  # black
                    sumPoints += -(1e-4)*(i-1)

                if c == 1 and Npieces_WH < 12:  # white
                    sumPoints += (1e-4)*(6-i)

            # add points for controlling center with pieces
            if i in range(2, 6) and j in range(2, 6) and b[0] != 0:
                sumPoints += (1e-3)*signCol[c]

            # piece, color
            sumPoints += pieceEval[(b[0], b[1])]

    return sumPoints  # output evaluation score

#FE##########################################################################################

# TIME EVERYTHING in main loop
def finalEval(boardState, color, positionKings, BWpieces,evalPoints,castlingStatus,legalMoves=None):

    # 0 = play
    # 1 = mate
    # 2 = draw by insufficient material
    # 3 = stalemate
    # 4 = player in check
    # 5 = opponent in check

    # checks for game status
    status = DrawStalemateMate(boardState, color, positionKings, BWpieces,castlingStatus,legalMoves)

    if status == 1:
        # black or white gets mated
        return (1 - 2*color)*np.Inf  # white or black wins

    if status == 2 or status == 3:
        return 0

    # player's king in check
    if status == 4:
        evalPoints += -(1e-1)*signCol[color]

    # opponent's king in check
    if status == 5:
        evalPoints += (1e-1)*signCol[color]


    return evalPoints  # output evaluation score
