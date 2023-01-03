import numpy as np
import random
import time
import copy

# =============================================================================
# Piece initialization function
# =============================================================================
range_8 = range(8)


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

    return boardState


# array slicing
# print(boardState[:,:,0]) # 2D chess ids
# print(boardState[:,:,1]) # 2D colors (0: black, 1:white)

# =============================================================================
# Printing the board state function
# =============================================================================

def printboard(boardState):

    # dictionary of (chess piece, color): "unicode"

    piece_color = {
        # 0 = black
        (0, 0): "\u2610",  # empty
        (1, 0): "\u265A",  # King
        (2, 0): "\u265B",  # Queen
        (3, 0): "\u265C",  # Rook
        (4, 0): "\u265D",  # Bishop
        (5, 0): "\u265E",  # Knight
        (6, 0): "\u265F",  # Pawn
        # 1 = white
        (0, 1): "\u2610",
        (1, 1): "\u2654",
        (2, 1): "\u2655",
        (3, 1): "\u2656",
        (4, 1): "\u2657",  # Bishop
        (5, 1): "\u2658",  # Knight
        (6, 1): "\u2659",
    }

    for i in range_8:  # rows
        oneRow = str(8-i) + " "
        for j in range_8:  # columns
            p = (boardState[i, j, 0], boardState[i, j, 1])
            oneRow += piece_color[p] + " "
        print(oneRow)

    print("  a  b  c  d  e  f  g  h")


# =============================================================================
# Dictionaries
# =============================================================================

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
    (0, 0): 0,  # empty
    (1, 0): 0,  # King
    (2, 0): -9,  # Queen
    (3, 0): -5,  # Rook
    (4, 0): -3,  # Bishop
    (5, 0): -3,  # Knight
    (6, 0): -1,  # Pawn
    # white
    (0, 1): 0,
    (1, 1): 0,
    (2, 1): 9,
    (3, 1): 5,
    (4, 1): 3,  # Bishop
    (5, 1): 3,  # Knight
    (6, 1): 1,
}

# =============================================================================
# Functions: move piece (1),check if legal (2), king in check (3)
# =============================================================================


def stringTOmove(userString):

    userMove = np.array([8-int(userString[1]), columnNum[userString[0]],
                        8-int(userString[3]), columnNum[userString[2]], 0])
    if len(userString) == 5:
        userMove[4] = promotion[userString[4]]

    return userMove


def moveTOstring(userMove):

    userString = numColumn[userMove[1]] + str(8-userMove[0]) + numColumn[userMove[3]] + str(8-userMove[2])

    if userMove[4] != 0:
        userString = userString + numPromotion[userMove[4]]

    return userString


def validInput(userMove):

    allR = [str(i) for i in range(1, 9)]  # "1" - "8"
    if userMove == "r":
        return True

    elif len(userMove) == 4 or len(userMove) == 5:
        letterC = userMove[0]
        rowC = userMove[1]

        letterD = userMove[2]
        rowD = userMove[3]

        current = (letterC in columnNum.keys()) and (rowC in allR)
        destination = (letterD in columnNum.keys()) and (rowD in allR)

        if len(userMove) == 4:
            if current and destination:
                return True

        elif len(userMove) == 5:

            letterP = userMove[4]
            promotionL = (letterP in promotion.keys())

            if current and destination and promotionL:
                return True

    else:
        return False


def movePiece(userMove, boardState, positionKings, BlackWhitePieces): #evalPoints

    # current square, destination square, promotion
    i, j, k, l, prom = userMove  # r,c,r,c,prom

    # current becoming destination square
    p, c = boardState[i, j, :]
    cpc = np.copy(boardState[i, j, :])  # currentpiece & color


    # update the king
    if p == 1:
        # positionKings[c] = userMove[2:4]
        positionKings[c] = [k, l]  # matrix format


    # update bl/wh pieces set
    # remove black/white piece from the list if on a current square
    BlackWhitePieces[c].remove((i, j))

    # adds black/white piece to the list if on a destination square
    BlackWhitePieces[c].add((k, l))
    

    dp = boardState[k, l, 0]  # dpc[0] # destination piece
    dpc = np.copy(boardState[k, l, :])  # destination piece & color
    dc = boardState[k, l, 1]
    
    if dp != 0:
        BlackWhitePieces[1-c].remove((k, l))
        
        # # evaluation
        # if c != dc:
        #     evalPoints -= pieceEval[(dp,dc)]
    
    
    # promotion
    if prom != 0:
        p = prom

    boardState[k, l, 0] = p
    boardState[k, l, 1] = c

    # current square
    # ex. a2     (0,6,0) = 6
    boardState[i, j, 0] = 0

    return cpc, dpc  # current[piece,color], destination[piece,color]


def undoMove(userMove, cpc, dpc, boardState, BlackWhitePieces):

    # current square, destination square, promotion
    i, j, k, l, prom = userMove  # r,c,r,c,prom

    boardState[i, j, :] = cpc  # current piece & color
    c = cpc[1]

    boardState[k, l, :] = dpc  # destination piece & color
    dp = dpc[0]  # destination piece

    # remove black/white piece from the list if on a current square
    BlackWhitePieces[c].remove((k, l))

    # adds black/white piece to the list if on a destination square
    BlackWhitePieces[c].add((i, j))

    if dp != 0:
        BlackWhitePieces[1-c].add((k, l))


# check if userMove is legal
def positionLegal(userMove, boardState, color):

    # # pass 'r' through function
    # if userMove == "r":
    #     return True

    # current square, destination square, promotion
    ch, cv, dh, dv, prom = userMove  # r,c,r,c,prom

    # current square
    # ex. a2     (6,0,0) = 6
    p = boardState[ch, cv, 0]  # 6
    c = boardState[ch, cv, 1]  # 1

    # destination square
    # ex. a3    (5,0,1)
    dp = boardState[dh, dv, 0]
    dc = boardState[dh, dv, 1]  # 1

    # horizontal and vertical differences
    # ex. a2a3
    h = dv - cv  # 1-1 = 0
    v = ch - dh  # 3-2 = 1

    absH = abs(h)
    absV = abs(v)

    ###### general checks (applies to both sides) ######

    # 1. only pieces can move, not squares
    # Empty squares: (0,0),  (0,1)
    if p == 0:
        return False

    # 2. only move your own piece
    if color != c:
        return False

    # 3. If there's my piece on a destination, it's illegal
    if c == dc and dp != 0:
        return False

    ###### knight check ######
    if p == 5:
        # goodKnight = (absH == 1 or absH == 2) and (absH+absV == 3)
        if (absH+absV != 3) or not(absH == 1 or absH == 2):
            return False

    ###### bishop check ######
    def bishopLegal():
        goodBishop = absH == absV
        if not goodBishop:
            return False
        i = 1
        sign_v = np.sign(v)
        sign_h = np.sign(h)
        while i < absH:
            if boardState[ch-sign_v*i, cv+sign_h*i, 0] != 0:
                return False
            i += 1

    # check legal bishop
    if p == 4:
        if bishopLegal() == False:
            return False

    ###### rook check ######
    def rookLegal():
        # allows only go horiz or vert
        if h == 0:  # moves vertically
            a, b = np.sort([ch, dh])
            if np.any(boardState[a+1:b, cv, 0]):
                return False

        elif v == 0:  # moves horizontally
            a, b = np.sort([cv, dv])
            if np.any(boardState[ch, a+1:b, 0]):
                return False
        else:
            return False

    # check legal rook
    if p == 3:
        if rookLegal() == False:
            return False

    ###### queen check ######
    if p == 2:
        if (h == 0 or v == 0):
            if (rookLegal() == False):
                return False

        elif (absH == absV):
            if (bishopLegal() == False):
                return False
        else:
            return False

    ###### king check ######
    if p == 1:
        if absH > 1 or absV > 1:
            return False

    # pawn check ###### DO EN PASSANT !!!
    if p == 6:
        v_dir = (2*color - 1)*v  # (2*1 - 1)*1 = 1

        # doesn't allow go 2 or more sqyares horizontally
        # ex. a2a3
        if absH > 1:  # skip since h=0
            return False

        # 1 square forward
        if v_dir == 1:  # true
            if absH == 1:  # false
                if dc == color or dp == 0:
                    return False
            # doesn't allow pawn to capture a piece in front
            if h == 0 and dp != 0:  # false
                return False

        # 2 squares forward
        if v_dir == 2:  # false
            if absH == 0:

                # check if standing on initial square
                # if not ((ch==1 and color==0) or (ch==6 and color==1)):
                if (ch != 1 or color != 0) and (ch != 6 or color != 1):
                    return False

                # doesn't allow to jump over a piece
                White2 = (ch == 6 and boardState[5, cv, 0] != 0)
                # Black2 = (ch == 1 and boardState[2,cv,0] != 0)
                if (White2 or (ch == 1 and boardState[2, cv, 0] != 0)) or dp != 0:
                    return False
            else:
                return False
        # check that pawn doesn't go beyond 2 squares vertically
        if (v_dir != 1) and (v_dir != 2):  # false
            return False

        # promotion: black, white
        if dh == 7 or dh == 0:
            if prom == 0:
                return False

    return True


def king_in_check(boardState, color, positionKings, BlackWhitePieces):

    # opposite color from king
    opp_color = 1 - color

    listOpp = BlackWhitePieces[1-color]

    kingCol = positionKings[color]
    kh = kingCol[0]  # 0:7 matrix format

    move = np.zeros(5, dtype=int)
    move[2:4] = kingCol
    # attack piece in list of opposite color
    for ap in listOpp:
        ah = ap[0]  # row matrix format
        av = ap[1]  # attack verical
        move[0:2] = ap

        if boardState[ah, av, 0] == 6 and ((ah == 1 and kh == 0) or (ah == 6 and kh == 7)):
            for prom in [2, 3, 4, 5]:
                move[4] = prom  # d7e8q format

                if positionLegal(move, boardState, opp_color):  # if condition true
                    return True
        else:
            move[4] = 0
            # tells if king of the same color as userMove is in check
            if positionLegal(move, boardState, opp_color):  # if condition true
                return True

    return False  # by default


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

# both positionally legal moves & returns false for king_in_check


def generateLegal(piece, boardState, color, positionKings, BlackWhitePieces):

    # current square
    ch, cv = piece
    p = boardState[ch, cv, 0]  # 6

    listMoves = []

    oppCol = 1-color

    ###### pawn moves ######
    if p == 6:

        v_dir = -1*(2*color - 1)  # black: -1*(2*0 - 1) = 1
                                    # white: -1*(2*1 - 1) = -1
        
        ch1 = ch + v_dir
        

        # 1 sqr forward is empty
        if boardState[ch1, cv, 0] == 0:

            # promotion
            if (ch == 1 and color == 1) or (ch == 6 and color == 0):
                for prom in [2, 3, 4, 5]:
                    listMoves.append([ch, cv, ch1, cv, prom])

            # 1 sqr forward
            else:
                listMoves.append([ch, cv, ch1, cv, 0])

            # 2 sqrs forward
            if (ch == 1 and color == 0) or (ch == 6 and color == 1):
                ch2 = ch + 2*(v_dir)
                
                if boardState[ch2, cv, 0] == 0:
                    listMoves.append([ch, cv, ch2, cv, 0])

        # 1 sqr forward & right
        if cv < 7:
            if boardState[ch1, cv+1, 0] != 0 and boardState[ch1, cv+1, 1] == oppCol:
    
                # promotion
                if (ch == 1 and color == 1) or (ch == 6 and color == 0):
                    for prom in [2, 3, 4, 5]:
                        listMoves.append([ch, cv, ch1, cv+1, prom])
    
                # eating a piece
                else:
                    listMoves.append([ch, cv, ch1, cv+1, 0])

        # 1 sqr forward & left
        if cv > 0:
            if boardState[ch1, cv-1, 0] != 0 and boardState[ch1, cv-1, 1] == oppCol:
                listMoves.append([ch, cv, ch1, cv-1, 0])
    
                # promotion
                if ch == 1 or ch == 6:
                    for prom in [2, 3, 4, 5]:
                        listMoves.append([ch, cv, ch1, cv-1, prom])
    
                # eating a piece
                else:
                    listMoves.append([ch, cv, ch1, cv-1, 0])

    ###### knight moves ######
    if p == 5:

        knightCase = {(ch+2, cv+1), (ch+2, cv-1), (ch-2, cv+1), (ch-2, cv-1),
                         (ch+1, cv+2), (ch+1, cv-2), (ch-1, cv+2), (ch-1, cv-2)}

        for case in knightCase:
            k, l = case
            if k >= 0 and k <= 7 and l >= 0 and l <= 7:
                if boardState[k, l, 0] == 0 or boardState[k, l, 1] == oppCol:
                    listMoves.append([ch, cv, k, l, 0])

    ###### king moves ######
    if p == 1:

        kingCase = {(ch+1, cv), (ch+1, cv+1), (ch+1, cv-1),  # up, up & right, up & left
                       # down, down & right, down & left
                       (ch-1, cv), (ch-1, cv+1), (ch-1, cv-1),
                       (ch, cv+1),  # right
                       (ch, cv-1)}  # left

        for case in kingCase:
            k, l = case
            if k >= 0 and k <= 7 and l >= 0 and l <= 7:
                if boardState[k, l, 0] == 0 or boardState[k, l, 1] == oppCol:
                    listMoves.append([ch, cv, k, l, 0])

    ###### rook moves ###### & ###### queen moves ######
    if p == 3 or p == 2:

        lenH = 7 - ch
        lenV = 7 - cv

        # moving right
        for sqr in range(1, lenV+1):
            right = cv+sqr

            if boardState[ch, right, 0] == 0:
                listMoves.append([ch,cv,ch,right, 0])

            elif boardState[ch, right, 1] == color:
                break

            elif boardState[ch, right, 1] == oppCol:
                listMoves.append([ch,cv,ch,right, 0])
                break

        # moving left
        for sqr in range(1, cv+1):
            left = cv-sqr

            if boardState[ch, left, 0] == 0:
                listMoves.append([ch,cv,ch, left, 0])

            elif boardState[ch, left, 1] == color:
                break

            elif boardState[ch, left, 1] == oppCol:
                listMoves.append([ch,cv,ch, left, 0])
                break

        # moving up
        for sqr in range(1, ch+1):
            up = ch-sqr

            if boardState[up, cv, 0] == 0:
                listMoves.append([ch,cv,up, cv, 0])

            elif boardState[up, cv, 1] == color:
                break

            elif boardState[up, cv, 1] == oppCol:
                listMoves.append([ch,cv,up, cv, 0])
                break

        # moving down
        for sqr in range(1, lenH+1):
            down = ch+sqr

            if boardState[down, cv, 0] == 0:
                listMoves.append([ch,cv,down, cv, 0])

            elif boardState[down, cv, 1] == color:
                break

            elif boardState[down, cv, 1] == oppCol:
                listMoves.append([ch,cv,down, cv, 0])
                break

    ###### bishop check ###### & ###### queen moves ######
    if p == 4 or p == 2:

        # distance
        lenH = 7 - cv  # right
        lenV = 7 - ch  # down

        # right & up
        for sqr in range(1, min(lenH, ch)+1):
            right = cv+sqr
            up = ch-sqr

            if boardState[up, right, 0] == 0:
                listMoves.append([ch, cv, up, right, 0])

            elif boardState[up, right, 1] == color:
                break

            elif boardState[up, right, 1] == oppCol:
                listMoves.append([ch,cv,up, right, 0])
                break

        # left & up
        for sqr in range(1,min(ch,cv)+1):
            left = cv-sqr
            up = ch-sqr

            if boardState[up, left, 0] == 0:
                listMoves.append([ch,cv,up, left,0])

            elif boardState[up, left, 1] == color:
                break

            elif boardState[up, left, 1] == oppCol:
                listMoves.append([ch,cv,up, left, 0])
                break

        # right & down
        for sqr in range(1,min(lenV,lenH)+1):
            down = ch+sqr
            right = cv+sqr

            if boardState[down, right, 0] == 0:
                listMoves.append([ch,cv,down, right,0])

            elif boardState[down, right, 1] == color:
                break

            elif boardState[down, right, 1] == oppCol:
                listMoves.append([ch,cv,down, right, 0])
                break

        # left & down
        for sqr in range(1,min(lenV,cv)+1):
            down = ch+sqr
            left = cv-sqr

            if boardState[down, left, 0] == 0:
                listMoves.append([ch,cv,down, left, 0])

            elif boardState[down, left, 1] == color:
                break

            elif boardState[down, left, 1] == oppCol:
                listMoves.append([ch,cv,down, left, 0])
                break

    # king in check
    legalMoves = []
    kingsExp = np.copy(positionKings)

    for move in listMoves:
        cpc, dpc = movePiece(move, boardState, kingsExp, BlackWhitePieces)

        # is king IN check?
        kingINcheck = king_in_check(
            boardState, color, kingsExp, BlackWhitePieces)

        undoMove(move, cpc, dpc, boardState, BlackWhitePieces)

        if not kingINcheck:
            legalMoves.append(move)

    return legalMoves


# checks for both position and square IN check
def checkLegal(userMove, boardState, color, positionKings, BlackWhitePieces):

    ###### king IN check ######

    # is position of intended userMove legal ?
    positionL = positionLegal(userMove, boardState, color)

    if positionL:
        #print("userMove: ", moveTOstring(userMove))
        kingsExp = np.copy(positionKings)
        # piecesExp = copy.deepcopy(BlackWhitePieces)
        # expected board with last user input
        cpc, dpc = movePiece(userMove, boardState, kingsExp, BlackWhitePieces)
       # print("after move: ")
        # printboard(boardState)

        # is king IN check?
        kingINcheck = king_in_check(
            boardState, color, kingsExp, BlackWhitePieces)

        undoMove(userMove, cpc, dpc, boardState, BlackWhitePieces)
        #print("after undoMove: ")
       # printboard(boardState)

        if not kingINcheck:
            return True

    # returns True if: positionL = True and squareCheck = False
    return False


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

def orderMoves(boardState, positionKings, BlackWhitePieces, legalMoves):

    evalList = []
    for move in legalMoves:
        #piecesExp = copy.deepcopy(BlackWhitePieces)
        kingsExp = np.copy(positionKings)
        # expected board with last user input
        cpc, dpc = movePiece(move, boardState, kingsExp, BlackWhitePieces)
        evalList.append(sortingEval(boardState))
        undoMove(move, cpc, dpc, boardState, BlackWhitePieces)

    sortedMoves = [legalMoves[i] for i in np.argsort(evalList)[::-1]]

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
                boardState), kingsExp, piecesExp)
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
                boardState), kingsExp, piecesExp)
            eval_of_move = minimax(
                boardExp, 1-color, kingsExp, depth-1, piecesExp)[0]

            if eval_of_move <= min_evalScore:
                min_evalScore = eval_of_move
                min_move = move

        return min_evalScore, min_move


def alphabeta(boardState, color, positionKings, depth, α, β, BlackWhitePieces):

    legalMoves = allLegal(boardState, color, positionKings, BlackWhitePieces)

    if depth == 0 or legalMoves == []:
        return Eval(boardState, color, positionKings, BlackWhitePieces, legalMoves), None

    legalMoves = orderMoves(boardState, positionKings,
                            BlackWhitePieces, legalMoves)

    if color == 1:  # white's move

        max_evalScore = -np.Inf
        max_move = None

        for move in legalMoves:
            #piecesExp = copy.deepcopy(BlackWhitePieces)
            kingsExp = np.copy(positionKings)

            # expected board with last user input
            cpc, dpc = movePiece(move, boardState, kingsExp, BlackWhitePieces)
            eval_of_move = alphabeta(
                boardState, 1-color, kingsExp, depth-1, α, β, BlackWhitePieces)[0]
            undoMove(move, cpc, dpc, boardState, BlackWhitePieces)

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
            #piecesExp = copy.deepcopy(BlackWhitePieces)
            kingsExp = np.copy(positionKings)

            # expected board with last user input
            cpc, dpc = movePiece(move, boardState, kingsExp, BlackWhitePieces)
            eval_of_move = alphabeta(
                boardState, 1-color, kingsExp, depth-1, α, β, BlackWhitePieces)[0]
            undoMove(move, cpc, dpc, boardState, BlackWhitePieces)

            if eval_of_move <= min_evalScore:
                min_evalScore = eval_of_move
                min_move = move

            if min_evalScore < α:
                break

            β = min(β, min_evalScore)

        return min_evalScore, min_move

# ===============================================================


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
                centerPoints = (1e-4)*(2*c-1)
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
        checkPoints = -(1e-5)*(2*color-1)
        sumPoints += checkPoints

    # opponent's king in check
    if status == 5:
        OppCheckPoints = (1e-5)*(2*color-1)
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
                    BLprom = -(1e-5)*(i-1)
                    sumPoints += BLprom

                if c == 1 and Npieces_WH < 12:  # white
                    WHprom = (1e-5)*(6-i)
                    sumPoints += WHprom

            # add points when pushing pawns
            if i in range(2, 6) and j in range(2, 6) and b[0] != 0:
                #c = b[1]
                centerPoints = (1e-4)*(2*c-1)
                sumPoints += centerPoints

            # piece, color
            sumPoints += pieceEval[(b[0], b[1])]

    return sumPoints  # output evaluation score
