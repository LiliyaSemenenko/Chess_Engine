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


    # MAKE A SET INSTEAD
    # initialize pieces
    BlackWhitePieces = [set(),set()]

    for i in range(8): # rows
        for j in range(8): # columns
            if boardState[i,j,0] != 0:
                BlackWhitePieces[boardState[i,j,1]].add((i,j))


    return boardState, positionKings, BlackWhitePieces


# array slicing
# print(boardState[:,:,0]) # 2D chess ids
# print(boardState[:,:,1]) # 2D colors (0: black, 1:white)

# =============================================================================
# Functions: OLD_allLegal, allLegal, DrawStalemateMate
# =============================================================================

def OLD_allLegal(boardState, color, positionKings, BlackWhitePieces):

    listMoves = []

    listCol = BlackWhitePieces[color]
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

                            if checkLegal(move, boardState, color, positionKings, BlackWhitePieces):
                                # !!!! fix this
                                listMoves.append(np.copy(move))

                    else:
                        move[4] = 0
                        if checkLegal(move, boardState, color, positionKings, BlackWhitePieces):
                            listMoves.append(np.copy(move))

    return listMoves


def allLegal(boardState, color, positionKings, BlackWhitePieces):

    finalList = []
    listCol = BlackWhitePieces[color]

    for piece in copy.copy(listCol):

        legalMoves = generateLegal(
            piece, boardState, color, positionKings, BlackWhitePieces)

        finalList.extend(legalMoves)

    return finalList


def DrawStalemateMate(boardState, color, positionKings, BlackWhitePieces, legalMoves=None):

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
            boardState, color, positionKings, BlackWhitePieces)
        # end = time.time()

    listCol = BlackWhitePieces[color]
    listOpp = BlackWhitePieces[1-color]

    # check if only kings are left
    # check if only knights or bishops left
    if (len(listCol) == 1 or (len(listCol) == 2 and ((4 in listCol) or (5 in listCol)))):
        if (len(listOpp) == 1 or (len(listOpp) == 2 and ((4 in listOpp) or (5 in listOpp)))):
            return 2

    myKcheck = king_in_check(
        boardState, color, positionKings, BlackWhitePieces)

    if legalMoves == []:

        # Stalemate check
        if not myKcheck:
            return 3

        # Mate check
        else:
            return 1

    if myKcheck:
        return 4

    OppKcheck = king_in_check(
        boardState, 1-color, positionKings, BlackWhitePieces)
    if OppKcheck:
        return 5

    return 0


# =====================================================================
# Decision functions: move ordering, minimax, alphabeta pruning
# =====================================================================

def orderMoves(boardState, positionKings, BlackWhitePieces, legalMoves,color):

    evalList = []
    for move in legalMoves:
        
        kingsExp = np.copy(positionKings)
        
        # expected board with last user input
        cpc, dpc = movePiece(move, boardState, kingsExp, BlackWhitePieces)
        evalList.append(sortingEval(boardState))
        undoMove(move, cpc, dpc, boardState, BlackWhitePieces)

    if color == 1: # white
        sortedMoves = [legalMoves[i] for i in np.argsort(evalList)[::-1]]
        return sortedMoves
    
    else: # black
        sortedMoves = [legalMoves[i] for i in np.argsort(evalList)]
        return sortedMoves



def minimax(boardState, color, positionKings, depth, BlackWhitePieces):

    legalMoves = allLegal(boardState, color, positionKings, BlackWhitePieces)

    if depth == 0 or legalMoves == []:
        return Eval(boardState, color, positionKings, BlackWhitePieces, legalMoves), None

    if color == 1:  # white's move

        max_evalScore = -np.Inf
        max_move = None

        for move in legalMoves:
            piecesExp = copy.deepcopy(BlackWhitePieces)
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
            piecesExp = copy.deepcopy(BlackWhitePieces)
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


def negaAB(boardState, color, positionKings, depth, α, β, BlackWhitePieces,evalPoints):

    legalMoves = allLegal(boardState, color, positionKings, BlackWhitePieces)

    if depth == 0 or legalMoves == []:
        return signCol[color]*Eval(boardState, color, positionKings, BlackWhitePieces, legalMoves), None

    legalMoves = orderMoves(boardState, positionKings,BlackWhitePieces, legalMoves,color)

    max_evalScore = -np.Inf
    max_move = None

    for move in legalMoves:
        #piecesExp = copy.deepcopy(BlackWhitePieces)
        kingsExp = np.copy(positionKings)

        # expected board with last user input
        cpc, dpc, evalPoints = movePiece_EVAL(move, boardState, kingsExp, BlackWhitePieces,evalPoints)
       
        eval_of_move = -negaAB(
            boardState, 1-color, kingsExp, depth-1, -β, -α, BlackWhitePieces,evalPoints)[0]
        
        evalPoints = undoMove_EVAL(move, cpc, dpc, boardState, BlackWhitePieces,evalPoints)

        if eval_of_move >= max_evalScore:
            max_evalScore = eval_of_move
            max_move = move

        # if max eval_Sc > a, then update alpha w/ max eval_Sc
        # if the reverse, a stays the same
        α = max(α, max_evalScore)
        
        if α >= β:
            break

    return max_evalScore, max_move

# =====================================================================
# Evaluation functions: sortingEval, Eval
# =====================================================================

def sortingEval(boardState):

    # calculates total evaluation score
    sumPoints = 0

    Npieces_BL = 0
    Npieces_WH = 0

    for i in range_8:
        for j in range_8:
            b = boardState[i, j, :]
            c = b[1]

            if b[0] != 0:
                if c == 0:
                    Npieces_BL += 1
                if c == 1:
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

            # add points when pushing pawns
            if i in range(2, 6) and j in range(2, 6) and b[0] != 0:
                #c = b[1]
                centerPoints = (1e-4)*signCol[c]
                sumPoints += centerPoints

            # piece, color
            sumPoints += pieceEval[(b[0], b[1])]

    return sumPoints  # output evaluation score


# TIME EVERYTHING in main loop
def Eval(boardState, color, positionKings, BlackWhitePieces,legalMoves=None):

    # 0 = play
    # 1 = mate
    # 2 = draw by insufficient material
    # 3 = stalemate
    # 4 = player in check
    # 5 = opponent in check

    # checks for game status
    status = DrawStalemateMate(boardState, color, positionKings, BlackWhitePieces, legalMoves)

    if status == 1:
        # black or white gets mated
        sumPoints = (1 - 2*color)*np.Inf  # white or black wins
        return sumPoints

    if status == 2 or status == 3:
        sumPoints = 0
        return sumPoints

    # calculates total evaluation score
    sumPoints = 0

    # player's king in check
    if status == 4:
        checkPoints = -(1e-1)*signCol[color]
        sumPoints += checkPoints

    # opponent's king in check
    if status == 5:
        OppCheckPoints = (1e-1)*signCol[color]
        sumPoints += OppCheckPoints

    # total number of bl/wh pieces
    Npieces_BL = len(BlackWhitePieces[0])
    Npieces_WH = len(BlackWhitePieces[1])


    for i in range_8:
        for j in range_8:
            b = boardState[i, j, :]
            c = b[1]

            # add points for moving pawn towards promotion
            if b[0] == 6 and i < 7:
                if c == 0 and Npieces_BL < 12:  # black
                    BLprom = -(1e-4)*(i-1)
                    sumPoints += BLprom

                if c == 1 and Npieces_WH < 12:  # white
                    WHprom = (1e-4)*(6-i)
                    sumPoints += WHprom

            # add points for controlling center with pieces
            if i in range(2, 6) and j in range(2, 6) and b[0] != 0:

                centerPoints = (1e-3)*signCol[c]
                sumPoints += centerPoints

            # piece, color
            sumPoints += pieceEval[(b[0], b[1])]

    return sumPoints  # output evaluation score

# TIME EVERYTHING in main loop
def finalEval(boardState, color, positionKings, BlackWhitePieces,evalPoints,legalMoves=None):

    # 0 = play
    # 1 = mate
    # 2 = draw by insufficient material
    # 3 = stalemate
    # 4 = player in check
    # 5 = opponent in check

    # checks for game status
    status = DrawStalemateMate(boardState, color, positionKings, BlackWhitePieces, legalMoves)

    if status == 1:
        # black or white gets mated
        evalPoints = (1 - 2*color)*np.Inf  # white or black wins
        return evalPoints

    if status == 2 or status == 3:
        evalPoints = 0
        return evalPoints

    # player's king in check
    if status == 4:
        checkPoints = -(1e-1)*signCol[color]
        evalPoints += checkPoints

    # opponent's king in check
    if status == 5:
        OppCheckPoints = (1e-1)*signCol[color]
        evalPoints += OppCheckPoints


    return evalPoints  # output evaluation score
