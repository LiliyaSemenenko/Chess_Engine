import numpy as np
import random
import time
import copy

# importing functions
from global_parameters import *

# =============================================================================
# Functions: movePiece, undoMove, positionLegal, sqr_under_attack, generateLegal 
# =============================================================================

#MP##########################################################################################

def movePiece(userMove, boardState, positionKings,BWpieces,castlingStatus):

    # current square, destination square, promotion
    i, j, k, l, prom = userMove  # r,c,r,c,prom

    # current becoming destination square
    p, c = boardState[i, j, :]
    cpc = np.copy(boardState[i, j, :])  # current piece & color

    dp = boardState[k, l, 0]  # dpc[0] # destination piece
    dpc = np.copy(boardState[k, l, :])  # destination piece & color
    dc = boardState[k, l, 1]
        
    #------------------------
    ### update the king
    if p == 1:
        positionKings[c] = [k, l]  # matrix format

    #------------------------
    ### update bl/wh pieces set
    
    # remove black/white piece from the list if on a current square
    BWpieces[c].remove((i, j))

    # adds black/white piece to the list if on a destination square
    BWpieces[c].add((k, l))
    
    if dp != 0:
        BWpieces[1-c].remove((k, l))
    
    #------------------------
    ### promotion
    if prom != 0:
        p = prom
    #------------------------
    ### castling
    
    # king
    if p == 1: #and not castlingStatus[(c,c)]
        
        if c == 0: # black
            row = 0
        if c == 1: # white
            row = 7
        
        # black or white king
        castlingStatus[(row,4)] += 1   
        
        #---------------------------
        ### moving rook 
        
        # short - right
        if i == row and j == 4 and k == row and l == 6: # king move: e1g1 or e8g8

                # rook move to destination: e8e6
                boardState[row, 5, 0] = 3
                boardState[row, 5, 1] = c

                # current square
                boardState[row, 7, 0] = 0
                #-----------------------------
                # remove black/white piece from the list if on a current square
                BWpieces[c].remove((row, 7))

                # adds black/white piece to the list if on a destination square
                BWpieces[c].add((row, 5))
                #-----------------------------
                
                # rook moves 
                castlingStatus[(row,7)] += 1
                
                # updating castling status for color
                castlingStatus[(c)] = True
                
        # long - left
        if i == row and j == 4 and k == row and l == 2: # king move: e1c1 or e8c8
                
                # rook move to destination: 
                boardState[row, 3, 0] = 3
                boardState[row, 3, 1] = c

                # current square
                boardState[row, 0, 0] = 0
                #-----------------------------
                
                # remove black/white piece from the list if on a current square
                BWpieces[c].remove((row, 0))

                # adds black/white piece to the list if on a destination square
                BWpieces[c].add((row, 3))
                #-----------------------------
                
                # rook moves or being taken
                castlingStatus[(row,0)] += 1
    
                # updating castling status for color
                castlingStatus[(c)] = True

        
    # rook moves 
    if p == 3: #and not castlingStatus[(c,c)]
        # black
        if c == 0:
            
            ### short - right
            if i == 0 and j == 7: # h8R
                castlingStatus[(i,j)] += 1
                
            ### long - left
            if i == 0 and j == 0: # a8R
                castlingStatus[(i,j)] += 1

        # white
        if c == 1:
            
            # short - right
            if (i == 7 and j == 7): # h1R
                castlingStatus[(i,j)] += 1
                
            # long - left
            if (i == 7 and j == 0): # a1R
                castlingStatus[(i,j)] += 1
    
            
    # rook being taken
    if dp == 3: # and not castlingStatus[(dc,dc)] 
        
        # black
        if dc == 0:
            
            ### short - right
            # if rook was taken
            if (k == 0 and l == 7): # h8R
                castlingStatus[(k,l)] += 1
                
            ### long - left
            # if rook was taken
            if (k == 0 and l == 0): # a8R
                castlingStatus[(k,l)] += 1
            
            
        # white
        if dc == 1:
            
            # short - right
            if (k == 7 and l == 7): # h1R
                castlingStatus[(k,l)] += 1
                
            # long - left
            if (k == 7 and l == 0): # a1R
                castlingStatus[(k,l)] += 1
              
    
    #------------------------
    ### boardstate updates
    
    boardState[k, l, 0] = p
    boardState[k, l, 1] = c

    # current square
    # ex. a2     (0,6,0) = 6
    boardState[i, j, 0] = 0


    return cpc, dpc  # current[piece,color], destination[piece,color]

#MPE##########################################################################################

def movePiece_EVAL(userMove, boardState, positionKings,BWpieces,evalPoints,castlingStatus):

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
    BWpieces[c].remove((i, j))

    # adds black/white piece to the list if on a destination square
    BWpieces[c].add((k, l))
    

    dp = boardState[k, l, 0]  # dpc[0] # destination piece
    dpc = np.copy(boardState[k, l, :])  # destination piece & color
    dc = boardState[k, l, 1]
    
    if dp != 0:
        BWpieces[1-c].remove((k, l))
        
        
    if dp != 0:
        # evaluation for eating a piece
        if c != dc:
            evalPoints -= pieceEval[(dp,dc)]
    
    
    
    evalPoints += (centerMatrix[k,l] - centerMatrix[i,j])*signCol[c]
    
    # deducts points from opponent for NOT controlling center after being eaten
    if dp != 0:
        evalPoints -= (centerMatrix[k,l])*signCol[1-c]
            
    
    # # add points for controlling center with pieces
    # if (k > 1 and k < 6) and (l > 1 and l < 6):
        
    #     # gives points for controlling center
    #     centerPoints = (1e-4)*signCol[c] # Bl: 2*0-1 = -1, Wh: 2*1-1 = 1
    #     evalPoints += centerPoints

    #     # deducts points for NOT controlling center after being eaten
    #     if dp != 0:
    #         centerPoints = (1e-4)*signCol[1-c] # Bl:  = -1, Wh: 2*1-1 = 1
    #         evalPoints -= centerPoints

    # promotion
    if prom != 0:
        p = prom

    #------------------------
    ### castling
    
    # king
    if p == 1: #and not castlingStatus[(c,c)]
        
        if c == 0: # black
            row = 0
        if c == 1: # white
            row = 7
        
        # black or white king
        castlingStatus[(row,4)] += 1   
        
        #---------------------------
        ### moving rook 
        
        # short - right
        if i == row and j == 4 and k == row and l == 6: # king move: e1g1 or e8g8

                # rook move to destination: e8e6
                boardState[row, 5, 0] = 3
                boardState[row, 5, 1] = c

                # current square
                boardState[row, 7, 0] = 0
                #-----------------------------
                # remove black/white piece from the list if on a current square
                BWpieces[c].remove((row, 7))

                # adds black/white piece to the list if on a destination square
                BWpieces[c].add((row, 5))
                #-----------------------------
                
                # rook moves 
                castlingStatus[(row,7)] += 1
                
                # updating castling status for color
                castlingStatus[(c)] = True
                
        # long - left
        if i == row and j == 4 and k == row and l == 2: # king move: e1c1 or e8c8
                
                # rook move to destination: 
                boardState[row, 3, 0] = 3
                boardState[row, 3, 1] = c

                # current square
                boardState[row, 0, 0] = 0
                #-----------------------------
                # remove black/white piece from the list if on a current square
                BWpieces[c].remove((row, 0))

                # adds black/white piece to the list if on a destination square
                BWpieces[c].add((row, 3))
                #-----------------------------
                
                # rook moves or being taken
                castlingStatus[(row,0)] += 1
    
                # updating castling status for color
                castlingStatus[(c)] = True

        
    # rook moves 
    if p == 3: #and not castlingStatus[(c,c)]
        # black
        if c == 0:
            
            ### short - right
            if i == 0 and j == 7: # h8R
                castlingStatus[(i,j)] += 1
                
            ### long - left
            if i == 0 and j == 0: # a8R
                castlingStatus[(i,j)] += 1

        # white
        if c == 1:
            
            # short - right
            if (i == 7 and j == 7): # h1R
                castlingStatus[(i,j)] += 1
                
            # long - left
            if (i == 7 and j == 0): # a1R
                castlingStatus[(i,j)] += 1
    
            
    # rook being taken
    if dp == 3: # and not castlingStatus[(dc,dc)] 
        
        # black
        if dc == 0:
            
            ### short - right
            # if rook was taken
            if (k == 0 and l == 7): # h8R
                castlingStatus[(k,l)] += 1
                
            ### long - left
            # if rook was taken
            if (k == 0 and l == 0): # a8R
                castlingStatus[(k,l)] += 1
            
            
        # white
        if dc == 1:
            
            # short - right
            if (k == 7 and l == 7): # h1R
                castlingStatus[(k,l)] += 1
                
            # long - left
            if (k == 7 and l == 0): # a1R
                castlingStatus[(k,l)] += 1
            
    #------------------------
    # boardstate update
    boardState[k, l, 0] = p
    boardState[k, l, 1] = c

    # current square
    # ex. a2     (0,6,0) = 6
    boardState[i, j, 0] = 0

    return cpc, dpc, evalPoints  # current[piece,color], destination[piece,color]

#UM##########################################################################################

def undoMove(userMove, cpc, dpc, boardState, BWpieces,castlingStatus):

    # current square, destination square, promotion
    i, j, k, l, prom = userMove  # r,c,r,c,prom
       
    #--------------------------     
    # putting pieces back where they used to be
    boardState[i, j, :] = cpc  # current piece & color
    p = cpc[0]
    c = cpc[1]

    boardState[k, l, :] = dpc  # destination piece & color
    dp = dpc[0]  # destination piece
    dc = dpc[1]
    
    #---------------------------
    # remove black/white piece from the list if on a current square
    BWpieces[c].remove((k, l))

    # adds black/white piece to the list if on a destination square
    BWpieces[c].add((i, j))

    if dp != 0:
        BWpieces[1-c].add((k, l))

    #---------------------------
    ### castling
    
    # king
    if p == 1:
        
        if c == 0: # black
            row = 0
        if c == 1: # white
            row = 7
        
        # if not castlingStatus[(c,c)]:
        castlingStatus[(row,4)] -= 1
        
        #---------------------------
        ### moving rook 
        
        # short - right
        if i == row and j == 4 and k == row and l == 6: # king move: e1g1 or e8g8

                # rook move to destination: e8e6
                boardState[row, 5, 0] = 0

                # current square
                boardState[row, 7, 0] = 3
                boardState[row, 7, 1] = c
                #---------------------------
                # remove black/white piece from the list if on a current square
                BWpieces[c].remove((row, 5))

                # adds black/white piece to the list if on a destination square
                BWpieces[c].add((row, 7))
                #-----------------------------
                
                # rook moves or being taken
                castlingStatus[(row,7)] -= 1
                    
                # updating castling status for color
                castlingStatus[(c)] = False
                    
        # long - left
        if i == row and j == 4 and k == row and l == 2: # king move: e1c1 or e8c8
                
                # rook move to destination: 
                boardState[row, 3, 0] = 0

                # current square
                boardState[row, 0, 0] = 3
                boardState[row, 0, 1] = c
                #---------------------------
                # remove black/white piece from the list if on a current square
                BWpieces[c].remove((row, 3))

                # adds black/white piece to the list if on a destination square
                BWpieces[c].add((row, 0))
                #-----------------------------
                
                # rook moves or being taken
                castlingStatus[(row,0)] -= 1
                
                # updating castling status for color
                castlingStatus[(c)] = False
    
    
    # rook moves or being taken
    if p == 3: #and castlingStatus[(c,c)]
        
        # black
        if c == 0:
            
            # short - right
            if i == 0 and j == 7: # h8R
                castlingStatus[(i,j)] -= 1
                
            # long - left
            if (i == 0 and j == 0): # a8R
                castlingStatus[(i,j)] -= 1
            
            
        # white
        if c == 1:
            
            # short - right
            if (i == 7 and j == 7): # h1R
                castlingStatus[(i,j)] -= 1
                
            # long - left
            if (i == 7 and j == 0): # a1R
                castlingStatus[(i,j)] -= 1
                
    
    if dp == 3: #and castlingStatus[(dc,dc)]
        
        # black
        if dc == 0:
            
            # short - right
            if k == 0 and l == 7: # h8R
                castlingStatus[(k,l)] -= 1
             
            # long - left
            if (k == 0 and l == 0): # a8R
                castlingStatus[(k,l)] -= 1
                
        # white
        if dc == 1:    
            
            # short - right
            if (k == 7 and l == 7): # h1R
                castlingStatus[(k,l)] -= 1
             
            # long - left
            if (k == 7 and l == 0): # a1R
                castlingStatus[(k,l)] -= 1
            
            
   
 
#UME##########################################################################################

def undoMove_EVAL(userMove, cpc, dpc, boardState, BWpieces,evalPoints,castlingStatus):

    # current square, destination square, promotion
    i, j, k, l, prom = userMove  # r,c,r,c,prom
            
    
    boardState[i, j, :] = cpc  # current piece & color
    p = cpc[0]
    c = cpc[1]

    boardState[k, l, :] = dpc  # destination piece & color
    dp = dpc[0]  # destination piece
    dc = dpc[1]
    
    #----------------------------------------
    ### undo evaluation
    if dp != 0:
        if c != dc:
            evalPoints += pieceEval[(dp,dc)]
    
    evalPoints -= (centerMatrix[k,l] - centerMatrix[i,j])*signCol[c]
    
    # deducts points for NOT controlling center after being eaten
    if dp != 0:
        evalPoints += (centerMatrix[k,l])*signCol[1-c]
            
    #----------------------------------------
    ### undo BWPieces
    
    # remove black/white piece from the list if on a current square
    BWpieces[c].remove((k, l))

    # adds black/white piece to the list if on a destination square
    BWpieces[c].add((i, j))

    if dp != 0:
        BWpieces[1-c].add((k, l))
        
    #---------------------------
    ### castling START
    
    # king
    if p == 1:
        
        if c == 0: # black
            row = 0
        if c == 1: # white
            row = 7
        
        # if not castlingStatus[(c,c)]:
        castlingStatus[(row,4)] -= 1
        
        #---------------------------
        ### moving rook 
        
        # short - right
        if i == row and j == 4 and k == row and l == 6: # king move: e1g1 or e8g8

                # rook move to destination: e8e6
                boardState[row, 5, 0] = 0

                # current square
                boardState[row, 7, 0] = 3
                boardState[row, 7, 1] = c
                #---------------------------
                # remove black/white piece from the list if on a current square
                BWpieces[c].remove((row, 5))

                # adds black/white piece to the list if on a destination square
                BWpieces[c].add((row, 7))
                #-----------------------------
                
                # rook moves or being taken
                castlingStatus[(row,7)] -= 1
                    
                # updating castling status for color
                castlingStatus[(c)] = False
                    
        # long - left
        if i == row and j == 4 and k == row and l == 2: # king move: e1c1 or e8c8
                
                # rook move to destination: 
                boardState[row, 3, 0] = 0

                # current square
                boardState[row, 0, 0] = 3
                boardState[row, 0, 1] = c
                #---------------------------
                # remove black/white piece from the list if on a current square
                BWpieces[c].remove((row, 3))

                # adds black/white piece to the list if on a destination square
                BWpieces[c].add((row, 0))
                #-----------------------------
                
                # rook moves or being taken
                castlingStatus[(row,0)] -= 1
                
                # updating castling status for color
                castlingStatus[(c)] = False
    
    
    # rook moves or being taken
    if p == 3: #and castlingStatus[(c,c)]
        
        # black
        if c == 0:
            
            # short - right
            if i == 0 and j == 7: # h8R
                castlingStatus[(i,j)] -= 1
                
            # long - left
            if (i == 0 and j == 0): # a8R
                castlingStatus[(i,j)] -= 1
            
            
        # white
        if c == 1:
            
            # short - right
            if (i == 7 and j == 7): # h1R
                castlingStatus[(i,j)] -= 1
                
            # long - left
            if (i == 7 and j == 0): # a1R
                castlingStatus[(i,j)] -= 1
                
    
    if dp == 3: #and castlingStatus[(dc,dc)]
        
        # black
        if dc == 0:
            
            # short - right
            if k == 0 and l == 7: # h8R
                castlingStatus[(k,l)] -= 1
             
            # long - left
            if (k == 0 and l == 0): # a8R
                castlingStatus[(k,l)] -= 1
                
        # white
        if dc == 1:    
            
            # short - right
            if (k == 7 and l == 7): # h1R
                castlingStatus[(k,l)] -= 1
             
            # long - left
            if (k == 7 and l == 0): # a1R
                castlingStatus[(k,l)] -= 1
    #---------------------------
    ### castling END

        
    return evalPoints
        

#SUA##########################################################################################

# former name: king_in_check
def sqr_under_attack(boardState, color, square, BWpieces,castlingStatus):

    # opposite color from king
    opp_color = 1 - color

    listOpp = BWpieces[1-color]

    kh = square[0]  # 0:7 matrix format

    move = np.zeros(5, dtype=int)
    move[2:4] = square
    
    # attack piece in list of opposite color
    for ap in listOpp:
        ah = ap[0]  # row matrix format
        av = ap[1]  # attack verical
        move[0:2] = ap

        if boardState[ah, av, 0] == 6 and ((ah == 1 and kh == 0) or (ah == 6 and kh == 7)):
            for prom in [2, 3, 4, 5]:
                move[4] = prom  # d7e8q format

                if positionLegal(move, boardState, opp_color,BWpieces,castlingStatus):  # if condition true
                    return True
        else:
            move[4] = 0
            # tells if king of the same color as userMove is in check
            if positionLegal(move, boardState, opp_color,BWpieces,castlingStatus):  # if condition true
                return True

    return False  # by default

#CL#########################################################################################

# checks for both position and square IN check
def checkLegal(userMove, boardState, color, positionKings, BWpieces, castlingStatus,debug=False):

    ###### king IN check ######

    # is position of intended userMove legal ?
    positionL = positionLegal(userMove, boardState, color,BWpieces, castlingStatus)
    if debug:
        print("BWpieces aftr posLeg: ",BWpieces) 
    
    if positionL:
        if debug:
            print("PosLeg was True")
        kingsExp = np.copy(positionKings)
        

        # expected board with last user input
        cpc, dpc = movePiece(userMove,boardState,kingsExp,BWpieces,castlingStatus)
        if debug:
            print("MP passed")
        # is king IN check?
        kingINcheck = sqr_under_attack(
            boardState, color, kingsExp[color], BWpieces,castlingStatus)
        if debug:
            print("K in Ch passed")
        undoMove(userMove, cpc, dpc, boardState, BWpieces,castlingStatus)
        if debug:
            print("UM passed")
        if not kingINcheck:
            if debug:
                print("CL returned True")
            return True

    # returns True if: positionL = True and squareCheck = False
    return False

#PL##########################################################################################

# check if userMove is legal
def positionLegal(userMove, boardState, color,BWpieces,castlingStatus):


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
        
        # (black & bl king moved = F) or (white & wh king moved = F)
        if (color == 0 and castlingStatus[(0,4)] == 0) or (color == 1 and castlingStatus[(7,4)] == 0):

            # short, long castling for white & black
            if cv == 4 and dp == 0 and ch == dh:
                
                # short - right castling
                if (color == 0 and castlingStatus[(0,7)] == 0) or (color == 1 and castlingStatus[(7,7)] == 0):       

                    # dv = g and 1f = empty
                    if dv == 6 and boardState[ch,5,0] == 0:
                        bishopSquare = [[0,5],[7,5]]

                        if not sqr_under_attack(boardState,color,bishopSquare[color],BWpieces,castlingStatus):
                            knightSquare = [[0,6],[7,6]]
 
                            if not sqr_under_attack(boardState,color,knightSquare[color],BWpieces,castlingStatus):

                                return True
                            
                # long - left castling
                if (color == 0 and castlingStatus[(0,0)] == 0) or (color == 1 and castlingStatus[(7,0)] == 0):

                    if dv == 2 and boardState[ch,3,0] == 0:
                        bishopSquare = [[0,2],[7,2]]

                        if not sqr_under_attack(boardState,color,bishopSquare[color],BWpieces,castlingStatus):
                            queenSquare = [[0,3],[7,3]]

                            if not sqr_under_attack(boardState,color,queenSquare[color],BWpieces,castlingStatus):

                                return True 
                            
            
        if absH > 1 or absV > 1:
            return False

    # pawn check ###### DO EN PASSANT !!!
    if p == 6:
        v_dir = signCol[color]*v  # (2*1 - 1)*1 = 1

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

#GL##########################################################################################

# both positionally legal moves & returns false for sqr_under_attack
def generateLegal(piece, boardState, color, positionKings, BWpieces,castlingStatus):

    # current square
    ch, cv = piece
    p = boardState[ch, cv, 0]  # 6

    listMoves = []

    oppCol = 1-color

    ###### pawn moves ######
    if p == 6:

        v_dir = -signCol[color]      # black: -1*(2*0 - 1) = 1
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
                if (ch == 1 and color == 1) or (ch == 6 and color == 0):
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
            if k >= 0 and k <= 7 and l >= 0 and l <= 7: # board boundries check
                if boardState[k, l, 0] == 0 or boardState[k, l, 1] == oppCol:
                    listMoves.append([ch, cv, k, l, 0])
        
        if cv == 4 and (ch == 7 or ch == 0):
            
            # long-left, short-right
            CastlMove = {(ch,cv,ch,cv-2,0),(ch,cv,ch,cv+2,0)}
            
            for move in CastlMove:
                if positionLegal(move, boardState,color,BWpieces,castlingStatus):
                    listMoves.append(move)
                    
            
      
    # # current square
    # ch, cv = piece
    # p = boardState[ch, cv, 0]  # 6

    # listMoves = []

    # oppCol = 1-color
                    
                    
    #========================================================================================
    ###### king check ######
    
    
    # positionLegal(userMove, boardState, color,BWpieces,castlingStatus)
    
    
    # if p == 1:
        
    #     # (black & bl king moved = F) or (white & wh king moved = F)
    #     if (color == 0 and castlingStatus[(0,4)] == 0) or (color == 1 and castlingStatus[(7,4)] == 0):

    #         # short
    #         if cv == 4 and dp == 0 and ch == dh:
                
    #             # short - right castling
    #             if (color == 0 and castlingStatus[(0,7)] == 0) or (color == 1 and castlingStatus[(7,7)] == 0):       

    #                 # dv = g and 1f = empty
    #                 if dv == 6 and boardState[ch,5,0] == 0:
    #                     bishopSquare = [[0,5],[7,5]]

    #                     if not sqr_under_attack(boardState,color,bishopSquare[color],BWpieces,castlingStatus):
    #                         knightSquare = [[0,6],[7,6]]
 
    #                         if not sqr_under_attack(boardState,color,knightSquare[color],BWpieces,castlingStatus):

    #                             return True
                            
    #             # long - left castling
    #             if (color == 0 and castlingStatus[(0,0)] == 0) or (color == 1 and castlingStatus[(7,0)] == 0):

    #                 if dv == 2 and boardState[ch,3,0] == 0:
    #                     bishopSquare = [[0,2],[7,2]]

    #                     if not sqr_under_attack(boardState,color,bishopSquare[color],BWpieces,castlingStatus):
    #                         queenSquare = [[0,3],[7,3]]

    #                         if not sqr_under_attack(boardState,color,queenSquare[color],BWpieces,castlingStatus):

    #                             return True 
    #===============================================================================================

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
        cpc, dpc = movePiece(move,boardState,kingsExp,BWpieces,castlingStatus)

        # is king IN check?
        kingINcheck = sqr_under_attack(
            boardState, color, kingsExp[color], BWpieces,castlingStatus)

        undoMove(move, cpc, dpc, boardState, BWpieces,castlingStatus)

        if not kingINcheck:
            legalMoves.append(move)

    return legalMoves