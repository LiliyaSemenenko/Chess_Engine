import numpy as np
from colorama import Fore
import random
import time
import copy
import collections
import matplotlib.pyplot as plt

# plot games
# plt.plot(x,y) (move number, evaluation)

# importing functions
from chessFunctions import *

# =============================================================================
# Parameters
# =============================================================================

depth = 4
print("depth",depth)
# engine
engineColor = 1
engineMode = "negaAB" # "negaAB", "AB", "MM" , "random"

# opponent
opponentMode = "ABd1" # "negaABd1", "ABd1", "user", "random"

# =============================================================================
# Main game execution loop
# =============================================================================
    
boardState, positionKings, BWpieces, castlingStatus, evalPoints, moveCol = initialization()


print("")
printboard(boardState)

gameOver = False

moveNumber = 1

userMove2 = None
# =============================================================================
# =====================================================================5========
# BRUTAL TESTING

# try catch 
# total num of games vs number of moves it took

# TOP ISSUES:
    # 1) retarded moves from engine 
    # 2) as depth incr, numMoves increases
    # 3) Castling giving error when removing a piece from cast sqr
    
    
ABEmoves = 0
ABEtime = 0

ABmoves = 0
ABtime = 0

moveList = []
ABmoveList = []

def TESTmovePiece_EVAL(userMove, boardState, positionKings,BWpieces,evalPoints,castlingStatus):

    # current square, destination square, promotion
    i, j, k, l, prom = userMove  # r,c,r,c,prom

    ### current square
    p, c = boardState[i, j, :]
    cpc = np.copy(boardState[i, j, :])  # currentpiece & color
    
    ### destination square
    dp = boardState[k, l, 0]  # dpc[0] # destination piece
    dc = boardState[k, l, 1]  # dpc[1] # destination color
    dpc = np.copy(boardState[k, l, :])  # destination piece & color 
        
    #---------------------------------------
    ### update the king
    if p == 1:
        # positionKings[c] = userMove[2:4]
        positionKings[c] = [k, l]  # matrix format
    #---------------------------------------
    #### update bl/wh pieces set
    
    # remove black/white piece from the list if on a current square
    BWpieces[c].remove((i, j))

    # adds black/white piece to the list if on a destination square
    BWpieces[c].add((k, l))
    
    if dp != 0:
        BWpieces[1-c].remove((k, l))
        
    #---------------------------------------
    ### add evalPoints for eating a piece    
    if dp != 0: # taking a piece
        if c != dc: # of opposite color
            evalPoints -= pieceEval[(dp,dc)]
    
    #---------------------------------------
    ### evalPoints using Piece-Square tables
    numPieces = len(BWpieces[c])
    
    # MID game
    if numPieces > 10:
        table = pieceTable["m"][(p,c)]
      
    # END game
    else:
        table = pieceTable["e"][(p,c)]
   
    
    # adds points for moving to a sqr
    evalPoints += (table[k,l] - table[i,j])*signCol[c]
 
    
    # deducts Piece-Square points from opponent after being eaten
    if dp != 0:
        evalPoints -= (table[k,l])*signCol[1-c]

    #---------------------------------------
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
                #-----------------------------
                # add points for castling
                evalPoints += (50)*signCol[c]
                print("hi 6")
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
                #-----------------------------
                # add points for castling
                evalPoints += (50)*signCol[c]
             
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
            
    #---------------------------------------
    # boardstate update
    boardState[k, l, 0] = p
    boardState[k, l, 1] = c

    #---------------------------------------
    ### promotion
    if prom != 0:
        
        # promotion piece at destination
        boardState[k, l, 0] = prom
        
        #-----------------------------
        # adds evalPoints after promoting
        evalPoints += pieceEval[(prom,c)]
     
    #---------------------------------------        
    # current square becomes empty after the move
    # ex. a2     (0,6,0) = 6
    boardState[i, j, 0] = 0

    return cpc, dpc, evalPoints  # current[piece,color], destination[piece,color]

###############################################################################
###############################################################################
def TESTEval(boardState, color, positionKings, BWpieces,castlingStatus,legalMoves=None):

    # 0 = play
    # 1 = mate
    # 2 = draw by insufficient material
    # 3 = stalemate
    # 4 = player in check
    # 5 = opponent in check

    if legalMoves == None:
        legalMoves = allLegal(boardState, color, positionKings, BWpieces,castlingStatus)
    
    # checks for game status
    status = DrawStalemateMate(boardState, color, positionKings,BWpieces,castlingStatus,legalMoves)

    if status == 1:
        # black or white gets mated
        print("line 287")
        return (1 - 2*color)*MATE_EVALSCORE  # white or black wins

    if status == 2 or status == 3:
        print("line 291")
        return 0

    # calculates total evaluation score
    sumPoints = 0

    # player's king in check
    if status == 4:
        print("line 299")
        sumPoints += -(10)*signCol[color]

    # opponent's king in check
    if status == 5:
        print("line 304")
        sumPoints += (10)*signCol[color]
    
    # # add points for castling
    # if castlingStatus[(color)]:
    #     print("line 309")
    #     sumPoints += (50)*signCol[color]

    #--------------------------------------
    ### evalPoints using Piece-Square tables
    numPieces = len(BWpieces[color])
    
    # MID game
    if numPieces > 10:
        print("line 318")
        table = pieceTable["m"]
    
    # END game
    else:
        print("line 323")
        table = pieceTable["e"]
    Bl_pieces = 0
    Bl_pos = 0
    Wh_pieces = 0
    Wh_pos = 0
    
    Bl_bish = 0
    Wh_bish = 0
    
    BlPoints = []
    WhPoints = []
                
    for i in range_8:
        for j in range_8:
            b = boardState[i, j, :]
            p = b[0]
            c = b[1]
            
            sumPoints += pieceEval[(p,c)]
            
            if c == 0: # black
                Bl_pieces += pieceEval[(p,c)]
            else:
                Wh_pieces += pieceEval[(p,c)]
                
            if p != 0:

                # adds points for piece position
                sumPoints += (table[(p,c)][i,j])*signCol[c]
                # print(sumPoints)
            
                # # adds points for all pieces on the board
                # sumPoints += pieceEval[(p,c)]
            
            
                if c == 0: # black
                    Bl_pos += (table[(p,c)][i,j])*signCol[c]
                    
                    if p == 6: # bishop
                        ps = (table[(p,c)][i,j])*10000
                        ps = ps.astype('int')
                        Bl_bish += ps*signCol[c]
                    
                    
                else:
                    Wh_pos += (table[(p,c)][i,j])*signCol[c]
                    
                    if p == 6: # bishop
                        ps = (table[(p,c)][i,j])*10000
                        ps = ps.astype('int')
                        Wh_bish += ps*signCol[c]
            
    # print("BlPoints:",sum(BlPoints))
    # print("WhPoints:", sum(WhPoints))   
    # print("sum:", sum(WhPoints)+sum(BlPoints)) 
    
    return sumPoints, Bl_pieces, Wh_pieces, Bl_pos, Wh_pos, Bl_bish, Wh_bish  # output evaluation score

# BRUTAL TESTING
# =============================================================================
# =============================================================================

while 1: # while True
    
    # for positionLegal
    color = moveNumber % 2
    
    # MAKE A DICTIONARY & remove from while !!!!!!!!!!!!!!
    # Current turn
    if color == 0: # even = black
        col = "\nBlack"
        
    else: # odd = white
        col = "\nWhite"
        
    print(Fore.GREEN  + col," to move\n" + Fore.RESET)
    
    # start1 = time.time()
    # OLD_legalMoves = OLD_allLegal(boardState,color,positionKings,BWpieces,castlingStatus)
    # for move in OLD_legalMoves:
    #     OLDmove = moveTOstring(move)
    # end1 = time.time()
    
    # timeALL = end1-start1
    # print("OLD_legalMoves time: ", timeALL)

    
    # start1 = time.time()

    # k = 100
    # for i in range(k):
    legalMoves = allLegal(boardState,color,positionKings,BWpieces,castlingStatus)
        
    #----------------------------------------------------------------------------------------------
    # opponent's turn
    if color == 1-engineColor: # black = 0, white = 1
        if opponentMode == "user" :
            
            # # resign check
            # if userString == "r":
            #     gameOver = True
            #     print("hehe bye loser")
            #     break 
            
            userMove = getUserInput(boardState, color, positionKings, BWpieces, castlingStatus)
                
        if opponentMode == "random":
            legalMoves = allLegal(boardState,color,positionKings,BWpieces,castlingStatus)
            userMove = (random.choices(legalMoves, k=1))[0]
        
        if opponentMode == "negaABd1":
            userMove = negaAB(boardState,color,positionKings,1,-MATE_EVALSCORE,MATE_EVALSCORE,BWpieces, evalPoints,castlingStatus)[1]
            print("YES EvalPts engine exp bl move: ",moveTOstring(negaAB(boardState, color, positionKings,depth-1,-MATE_EVALSCORE,MATE_EVALSCORE, BWpieces, evalPoints,castlingStatus)[1]))

        if opponentMode == "ABd1":
            userMove = alphabeta(boardState, color, positionKings, 1, -MATE_EVALSCORE,MATE_EVALSCORE,BWpieces,castlingStatus)[1]
            print("engine exp bl move: ",moveTOstring(alphabeta(boardState, color, positionKings,depth-1,-MATE_EVALSCORE,MATE_EVALSCORE, BWpieces,castlingStatus)[1]))
            
        # print("engine exp bl move: ",moveTOstring(alphabeta_EVAL(boardState, color, positionKings,depth-1,-MATE_EVALSCORE,MATE_EVALSCORE, BWpieces,evalPoints,castlingStatus)[1]))    
        print("")
        print("chosen move: ",moveTOstring(userMove))
        
        
    # engine's turn
    else: 
        ### time start
        start = time.time()
        ### time start
        
        if engineMode == "negaAB":
            evalSc, userMove = negaAB(boardState,color,positionKings,depth,-MATE_EVALSCORE,MATE_EVALSCORE,BWpieces, evalPoints,castlingStatus)
            
            print("engine eval score: ", evalSc)
            
        if engineMode == "AB":
            evalSc, userMove = alphabeta(boardState, color, positionKings, depth, -MATE_EVALSCORE,MATE_EVALSCORE, BWpieces,castlingStatus)
            print("engine eval score: ", evalSc)
            
        if engineMode == "ABE":
            evalSc, userMove = alphabeta_EVAL(boardState, color, positionKings, depth, -MATE_EVALSCORE,MATE_EVALSCORE, BWpieces,evalPoints,castlingStatus)
            print("engine eval score: ", evalSc)    
            
        if engineMode == "MM":
            evalSc, userMove = minimax(boardState,color,positionKings,depth,BWpieces,castlingStatus)
            print("engine eval score: ", evalSc)
        
        ### time end
        end = time.time()
        ### time end
        
        if engineMode == "random":
            userMove = (random.choices(legalMoves, k=1))[0]
        
        if engineMode == "user" :
            
            # # resign check
            # if userString == "r":
            #     gameOver = True
            #     print("hehe bye loser")
            #     break 
            
            userMove = getUserInput(boardState, color, positionKings, BWpieces, castlingStatus)
            
        
        ABEtime = end-start
        # print("ABE engine time: ", ABEtime)
        # print("userMove: ", userMove)
        print("")
        
        print("chosen move: ",moveTOstring(userMove))
        print("")
        moveList.append(userMove)
        #----------------------------------
        ### test AB time w/out evalPoints
        
        ABstart = time.time()
        
        # ABeval, ABmove = alphabeta(boardState, color, positionKings, depth, -MATE_EVALSCORE,MATE_EVALSCORE, BWpieces,castlingStatus)
        ABeval, ABmove = alphabeta_EVAL(boardState, color, positionKings, depth, -MATE_EVALSCORE,MATE_EVALSCORE, BWpieces,evalPoints,castlingStatus)

        ABmoveList.append(ABmove)
        ABend = time.time()
        
        ABtime = ABend-ABstart
        print("AB time:", ABtime)
        print("ABE time:", ABEtime)
        
        print("AB-ABE =", ABtime - ABEtime)
        #----------------------------------
        
        ABEtime += ABEtime
        ABEmoves += 1
        
        ABtime += ABtime
        ABmoves += 1
        
        print("\nEngine mode move:",moveTOstring(moveList[-1]))
        print("ABE move:",moveTOstring(ABmoveList[-1]))
        print("")
    #----------------------------------------------------------------------------------------------    
    # print("moveList: ", moveList)
    # print("ABmoveList: ", ABmoveList)
    
    # evalt = Eval(boardState,color,positionKings,BWpieces,castlingStatus,legalMoves)
    # print("Eval(): ", evalt)
    
    # print("evalPoints: ",evalPoints)

    if moveList != ABmoveList:
        print("moves are NOT same")
        print("")
        print("Engine mode move:",moveTOstring(moveList[-1]))
        print("ABE move:",moveTOstring(ABmoveList[-1]))
        print("")
        # print("ABE list",moveList)
        # print("AB list",ABmoveList)
        break
     
        
     
        
    # ### BEFORE A MOVE IS MADE
    # LAST_Oppcheck = sqr_under_attack(boardState,1-color,positionKings[1-color],BWpieces,castlingStatus)
    # print("\n Opp King in check: ",LAST_Oppcheck)
    
    # LAST_Colcheck = sqr_under_attack(boardState,color,positionKings[color],BWpieces,castlingStatus)
    # print("\n Col King in check: ",LAST_Colcheck)
    
    # if LAST_Oppcheck or LAST_Colcheck:
    #     evalP = evalPoints
    #     finPoints = finalEval(boardState, color, positionKings, BWpieces,castlingStatus,evalPoints,legalMoves)
    #     print("evalP:",evalP)
    #     print("finPoints:",finPoints)
    
    #     evalPoints = finPoints
    



    ### MOVES PIECE on the board & updates position kings after the move is made
    cpc,dpc,evalPoints = movePiece_EVAL(userMove,boardState,positionKings,BWpieces,evalPoints,castlingStatus)
    
    # Oppcheck = sqr_under_attack(boardState,1-color,positionKings[1-color],BWpieces,castlingStatus)
    # print("\n Opp King in check: ",Oppcheck)
    
    # Colcheck = sqr_under_attack(boardState,color,positionKings[color],BWpieces,castlingStatus)
    # print("\n Col King in check: ",Colcheck)
    
    # if (LAST_Oppcheck and not Oppcheck) or (LAST_Colcheck and not Colcheck) or (not LAST_Oppcheck and Oppcheck) or (not LAST_Colcheck and Colcheck):
        
    #     # checks for game status
    #     # status = DrawStalemateMate(boardState, color, positionKings, BWpieces,castlingStatus,legalMoves)

    #     # player's king in check
    #     if not Oppcheck:
    #         evalPoints += (10)*signCol[color]

    #     # opponent's king in check
    #     if Oppcheck:
    #         evalPoints += -(10)*signCol[color]
        
    #     # player's king in check
    #     if not Colcheck:
    #         evalPoints += (10)*signCol[color]

    #     # opponent's king in check
    #     if Colcheck:
    #         evalPoints += -(10)*signCol[color]
        
        
        
        
    # evalP = evalPoints
    finPoints = finalEval(boardState, color, positionKings, BWpieces,castlingStatus,evalPoints,legalMoves)
    print("evalPoints:",evalPoints)
    print("finPoints:",finPoints)
    evalt = Eval(boardState,color,positionKings,BWpieces,castlingStatus)
    print("Eval(): ", evalt)
    # evalPoints = finPoints
        
        
          
    # print("Wh pieces: ",BWpieces[1])
    # print("Bl pieces: ",BWpieces[0])
    # print("positionKings: ",positionKings)
    
    #--------------------------------------------------------------------------
    ### expected sequence of moves by the ENGINE
    
    # if color == engineColor:
    #     seq = EXPmoveSequence(engineMode,boardState,color,positionKings,depth,BWpieces,evalPoints,castlingStatus)
    #     print("exp next moves: ",([moveTOstring(move) for move in seq]))    
    #--------------------------------------------------------------------------

    # start1 = time.time()
    # k = 100
    # for i in range(k):
    #     test = movePiece(userMove,np.copy(boardState),np.copy(positionKings),copy.deepcopy(BWpieces))
    # end1 = time.time()
    # print("Avg TEST movePiece time: ", (end1-start1)/k)


            
                
    # print("positionKings: ",positionKings)
    
    
    

    # print board
    printboard(boardState)
    
    # # TEST
    # if moveNumber == 7:
    #     undoMove(userMove,cpc,dpc,boardState,BWpieces)
    #     printboard(boardState)
    #     break
    # # TEST
    
    # legalMoves = allLegal(boardState,color,positionKings,BWpieces)

    # evalt = None
    # k = 100
    # legalMoves = allLegal(boardState,color,positionKings,BWpieces,castlingStatus)
    # start2 = time.time()

    # for i in range(k):
        
    # evaluation score            
    # print("\nEval(): ", Eval(boardState,color,positionKings,BWpieces,legalMoves))
    # evalt = Eval(boardState,color,positionKings,BWpieces,castlingStatus,legalMoves)
    # end2 = time.time()
    # timeAVG = (end2-start2)/k
    # print("")
    # print("Eval(): ", evalt)
    
    # print("evalPoints: ",evalPoints)
    # evalPointsis off by 0.0000000000000071

    
    # if evalt != finPoints:
    #     print("")
    #     print("Eval() - evalPoints =",evalt-evalPoints)
    #     undoMove_EVAL(userMove, cpc, dpc, boardState, BWpieces,evalPoints,castlingStatus)
    #     print(">>> TEST EVAL")
    #     # printboard(boardState)
    #     # ep = TESTmovePiece_EVAL(userMove,boardState,positionKings,BWpieces,evalPoints,castlingStatus)[2]
    #     e, Bl_pieces, Wh_pieces, Bl_pos, Wh_pos, Bl_bish, Wh_bish  = TESTEval(boardState, color, positionKings, BWpieces,castlingStatus)
    #     print("test Eval() total:",e)
    #     print("test Eval() Bl_pieces:",Bl_pieces)
    #     print("test Eval() Wh_pieces:",Wh_pieces)
    #     print("\ntest Eval() Bl_pos:",Bl_pos)
    #     print("test Eval() Wh_pos:",Wh_pos)
        
    #     print("\ntest Eval() Bl_bish:",Bl_bish)
    #     print("test Eval() Wh_bish:",Wh_bish)
    #     print("\nsum =",Bl_pieces+Wh_pieces+Bl_pos+Wh_pos)
    #     # print("sum =", Bl_+Wh)
    #     print("cpc",cpc)
    #     print("dpc",dpc)
        
    #     p = cpc[0]
    #     c = cpc[1]
    #     i, j, k, l, prom = userMove  # r,c,r,c,prom
    #     numPieces = len(BWpieces[c])
        
    #     # MID game
    #     if numPieces > 10:
    #         table = pieceTable["m"][(p,c)]
    #         print(table)
    #     # END game
    #     else:
    #         table = pieceTable["e"][(p,c)]
    #         print(table)
       
        
    #     # adds points for moving to a sqr
    #     print(table[k,l], "-", table[i,j])
    #     testPoints = 0
    #     testPoints += (table[k,l] - table[i,j])*signCol[c]
    #     print("testPoints:",testPoints)
    #     break
    
    # print("Fin eval: ",finalEval(boardState, color, positionKings, BWpieces,evalPoints,castlingStatus,legalMoves))
    # bfrMove = finalEval(boardState, color, positionKings, BWpieces,evalPoints,castlingStatus,legalMoves)
    # print("Undo Fin eval: ",undoMove_EVAL(userMove, cpc, dpc, np.copy(boardState),copy.deepcopy(BWpieces),evalPoints,copy.deepcopy(castlingStatus)))
    # aftrMove = undoMove_EVAL(userMove, cpc, dpc, np.copy(boardState),copy.deepcopy(BWpieces),evalPoints,copy.deepcopy(castlingStatus))
    # print("Points diff: ",bfrMove - aftrMove)
    # print("")
    # if round(evalPoints-evalt,10) != 0:
    #     print("eval NOT same")
    #     break
    
    
    # print("Avg Eval time: ", timeAVG)

    # opposite color from king
    opColor = 1 - color
    
    start = time.time()
    k = 100
    for i in range(k):
        check = sqr_under_attack(boardState,opColor,positionKings[opColor],BWpieces,castlingStatus)
    end = time.time()
    timeAVG = (end-start)/k
    print("\nKing in check: ",check)
    # print("King in check AVG time: ", timeAVG)
    
    print("Number of moves: ",moveNumber)
    
    start2 = time.time()
    # checks if opponent is mated or it's a draw since opp not able to move
    status = DrawStalemateMate(boardState,1-color,positionKings,BWpieces,castlingStatus)

    
    if status != 0 and status != 4:
        print(Fore.RED  + "\nhehe " + gameStatus[status] + Fore.RESET)
        break
        
    print("_______________________________________")
    moveNumber += 1

# =============================================================================
print("")
print("avg AB time: ",ABtime/ABmoves)
print("avg ABE time: ",ABEtime/ABEmoves)
print("avg AB-ABE: ",(ABtime/ABmoves)-(ABEtime/ABEmoves))
    
