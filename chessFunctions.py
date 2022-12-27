import numpy as np

# =============================================================================
# Piece initialization function
# =============================================================================

def initialization():
    
    # 3D board
    boardState = np.zeros((8,8,2),dtype = int)
    
    # Set up 3D matrix
    
    # A[r,c,0] = piece id
    # A[r,c,1] = piece color
    
    for i in [0, 7]: # pieces with 3+ value 
    
        # black(0) & white(7) pieces
        boardState[i,4,0] = 1 # king
        boardState[i,3,0] = 2 # queen
        boardState[i,0,0] = 3 # rook L
        boardState[i,7,0] = 3 # rook R
        boardState[i,2,0] = 4 # bishop L
        boardState[i,5,0] = 4 # bishop R
        boardState[i,1,0] = 5 # knight L
        boardState[i,6,0] = 5 # knight R
            
        
    for j in range(8): # columns: range(n) is 0:n-1
        
        # black pawns
        boardState[1,j,0] = 6 # id
        boardState[1,j,1] = 0 # color
        
        #white pawns
        boardState[6,j,0] = 6 # id
        boardState[6,j,1] = 1 # color  
        
        # color of black 3+ value pieces
        boardState[0,j,1] = 0 # black   
        
        # color of white 3+ value pieces
        boardState[7,j,1] = 1 # white   

    return boardState


# array slicing    
#print(boardState[:,:,0]) # 2D chess ids
#print(boardState[:,:,1]) # 2D colors (0: black, 1:white)

# =============================================================================
# Printing the board state function
# =============================================================================

def printboard(boardState):
    
    # dictionary of (chess piece, color): "unicode"
    
    piece_color = {
       # 0 = black
      (0,0): "\u2610", # empty
      (1,0): "\u265A", # King
      (2,0): "\u265B", # Queen
      (3,0): "\u265C", # Rook
      (4,0): "\u265D", # Bishop
      (5,0): "\u265E", # Knight
      (6,0): "\u265F", # Pawn
      # 1 = white
      (0,1): "\u2610",
      (1,1): "\u2654", 
      (2,1): "\u2655",
      (3,1): "\u2656", 
      (4,1): "\u2657", # Bishop
      (5,1): "\u2658", # Knight
      (6,1): "\u2659",
    }
    
    
    for i in range(8): # rows
        oneRow = str(8-i) + " "
        for j in range(8): # columns
            p = (boardState[i,j,0],boardState[i,j,1])
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

# Piece evaluation
pieceEval = {
    # black
    (0,0): 0, # empty
    (1,0): 0, # King
    (2,0): -9, # Queen
    (3,0): -5, # Rook
    (4,0): -3, # Bishop
    (5,0): -3, # Knight
    (6,0): -1, # Pawn
    # white
    (0,1): 0,
    (1,1): 0,
    (2,1): 9,
    (3,1): 5, 
    (4,1): 3, # Bishop
    (5,1): 3, # Knight
    (6,1): 1,
    } 

# =============================================================================
# Functions: move piece (1),check if legal (2), king in check (3)
# =============================================================================    

def validInput(userMove):
    
    allR = [str(i) for i in range(1,9)] # "1" - "8"
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



def movePiece(userMove,boardState): 
    
    # destination square
    # ex. a3 
    p = boardState[(8-int(userMove[1]),columnNum[userMove[0]],0)] # 6
    c = boardState[(8-int(userMove[1]),columnNum[userMove[0]],1)] # 1
    
    # promotion
    if len(userMove) == 5:
        p = promotion[userMove[4]] 
        
    boardState[(8-int(userMove[3]),columnNum[userMove[2]],0)] = p  
    boardState[(8-int(userMove[3]),columnNum[userMove[2]],1)] = c 
    
    # current square
    # ex. a2     (0,6,0) = 6
    boardState[(8-int(userMove[1]),columnNum[userMove[0]],0)] = 0 
    
    return boardState
        

# check if userMove is legal
def positionLegal(userMove,boardState,color):
    
    # pass 'r' through function
    if userMove == "r":
        return True
    
    # current horizontal sqr & vertical sqr
    # ex. a2
    ch = 8-int(userMove[1]) # 2 = row
    cv = columnNum[userMove[0]] # 1 = column
    
    # current square 
    # ex. a2     (6,0,0) = 6
    p = boardState[ch,cv,0] # 6
    c = boardState[ch,cv,1] # 1
    
    
    # destination horizontal sqr & vertical sqr
    dh = 8-int(userMove[3])
    dv = columnNum[userMove[2]]
    
    # destination square
    # ex. a3    (5,0,1) 
    dp = boardState[dh,dv,0] # 
    dc = boardState[dh,dv,1] # 1
    
    
    # horizontal and vertical differences
    # ex. a2a3
    h = dv - cv # 1-1 = 0
    v = ch - dh # 3-2 = 1

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
    if  p == 5:
        goodKnight = (abs(h) == 1 or abs(h) == 2) and (abs(h)+abs(v) == 3)
        if not goodKnight:
            return False
    
    ###### bishop check ######
    def bishopLegal():
        goodBishop = abs(h) == abs(v)
        if not goodBishop:
            return False
        i = 1
        sign_v = np.sign(v)
        sign_h = np.sign(h)
        while i < abs(h):
            if boardState[ch-sign_v*i,cv+sign_h*i,0] != 0:
                return False
            i += 1
    
    # check legal bishop
    if  p == 4:
        if bishopLegal() == False:
            return False
        
    ###### rook check ######
    def rookLegal(): 
        # allows only go horiz or vert
        if h == 0: # moves vertically
            a,b = np.sort([ch,dh])
            if sum(boardState[a+1:b,cv,0]) != 0:
                return False
        
        elif v == 0 : # moves horizontally
            a,b = np.sort([cv,dv])
            if sum(boardState[ch,a+1:b,0]) != 0:
                return False
        else:
            return False
    
    # check legal rook 
    if  p == 3:
        if rookLegal() == False:
            return False
        
    ###### queen check ######
    if  p == 2:
        if (h == 0 or v == 0):
            if (rookLegal() == False):
                return False
        
        elif (abs(h) == abs(v)):
            if (bishopLegal() == False):
                return False
        else:
            return False
   
    
    ###### king check ######
    if  p == 1:
        goodKing = abs(h) <= 1 and abs(v) <= 1
        if not goodKing:
            return False
     
    ###### pawn check ###### DO EN PASSANT !!!
    if p == 6:
        v_dir = (2*color - 1)*v # (2*1 - 1)*1 = 1
        
        # doesn't allow go 2 or more sqyares horizontally
        # ex. a2a3
        if abs(h) > 1: # skip since h=0
            return False
        
        # 1 square forward
        if v_dir == 1: # true
            if abs(h) == 1: # false
                if not (dc!=color and dp!=0): # 
                    return False
            # doesn't allow pawn to capture a piece in front    
            if h == 0 and dp != 0: # false
                return False
        
        # 2 squares forward    
        if v_dir == 2: # false
            if abs(h) == 0:
        
                # check if standing on initial square
                if not ((ch==1 and color==0) or (ch==6 and color==1)):
                    return False
                
                # doesn't allow to jump over a piece
                White2 = (ch == 6 and boardState[5,cv,0] != 0)
                Black2 = (ch == 1 and boardState[2,cv,0] != 0)
                if (White2 or Black2) or dp != 0:
                    return False
            else:
                return False
        # check that pawn doesn't go beyond 2 squares vertically 
        if (v_dir != 1) and (v_dir != 2): # false
            return False
    
    return True


# def kingLocation(userMove,boardState,color):
    
#     # current horizontal sqr & vertical sqr
#     # ex. 
#     ch = 8-int(userMove[1]) # 2 = row
#     cv = columnNum[userMove[0]] # 1 = column 
    
#     # current square 
#     # ex. a2     (6,0,0) = 6
#     p = boardState[ch,cv,0] # 6
#     c = boardState[ch,cv,1] # 1
    
    
#     # # destination horizontal sqr & vertical sqr
#     # dh = 8-int(userMove[3])
#     # dv = columnNum[userMove[2]]
    
#     # # destination square
#     # # ex. a3    (5,0,1) 
#     # dp = boardState[dh,dv,0] # 
#     # dc = boardState[dh,dv,1] # 1
    
#     # if king moved
#     if p == 1 and c == color:
#         #dh = 8-int(userMove[3]) # king horizontal destination
#         #dv = userMove[2] # king vertical destination
#         positionKing = userMove[2] + userMove[3]
#         #positionKing = boardState[ch,cv,0]
        
#     return positionKing

    
def king_in_check(boardState, color, positionKings):
    
    # opposite color from king
    opp_color = 1 - color
    
    #kingString = positionKings[color]
    
    listOpp = []    
    for i in range(8): # rows
        for j in range(8): # columns
        
            # locate the king of same color as the userMove input
            if boardState[i,j,0] == 1 and boardState[i,j,1] == color:
                kh = 8-i # king horizontal
                kv = numColumn[j] # king vertical
                kingString = str(kv) + str(kh)
            
            # locate all the pieces of opposite color    
            if boardState[i,j,1] == opp_color and  boardState[i,j,0] != 0:
                listOpp.append([i,j,1])
    
    # 
    for i in range(len(listOpp)):
        ap = listOpp[i] # attack piece of opposite color
        av = numColumn[ap[1]] # attack verical
        attackString = str(av) + str(8-ap[0])
        # opp color piece location + king location
        moveString = attackString + kingString # a2e1 format
    
        # tells if king of the same color as userMove is in check
        if positionLegal(moveString,boardState,opp_color): # if condition true
            return True
        
    return False # by default
    

def allLegal(boardState,color,positionKings):

    listMoves = []    
    for i in range(8): # rows
        for j in range(8): # columns
            for k in range(8): # rows
                for l in range(8): # columns
            # locate the pieces of same color as the engine's turn
                    move = str(numColumn[j]) + str(8-i) + str(numColumn[l]) + str(8-k)
                
                    if checkLegal(move,boardState,color,positionKings):
                        #print("Move: ",move)
                        listMoves.append(move)
                    
    return listMoves
                


# checks for both position and square IN check
def checkLegal(userMove, boardState, color, positionKings):
    
    ###### king IN check ######
    
    # is position of intended userMove legal ?
    positionL = positionLegal(userMove,boardState,color)
    
    if positionL:
        
        # expected board with last user input
        boardExp = movePiece(userMove,np.copy(boardState))
        
        # is king IN check?
        kingINcheck = king_in_check(boardExp, color, positionKings)
        
        if not kingINcheck:
            return True
            
    # returns True if: positionL = True and squareCheck = False
    return False


# subtract sum of total points of white and black
# output evaluation score  

def Eval(boardState):
    sumPoints = 0

    for i in range(8):
        for j in range(8):
            b = boardState[i,j,:] 
            sumPoints += pieceEval[(b[0],b[1])]
            
    return sumPoints