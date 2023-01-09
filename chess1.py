import numpy as np
import pandas as pd
from colorama import Fore
import random
import time
import copy
import collections

# importing functions
from chessFunctions import *

# =============================================================================
# Parameters
# =============================================================================

depth = 4

# engine
engineColor = 1
engineMode = "AB" # "negaAB", "AB", "MM" , "random"

# opponent
opponentMode = "random" # "negaABd1", "ABd1", "user", "random"

# =============================================================================
# Main game execution loop
# =============================================================================
    
boardState, positionKings, BWpieces, castlingStatus, evalPoints = initialization()


print("")
printboard(boardState)

gameOver = False

moveNumber = 1

userMove2 = None
# =============================================================================
# =============================================================================
# BRUTAL TESTING

# TOP ISSUES:
    # 1) retarded moves from engine 
    # 2) as depth incr, numMoves increases
    # 3) Castling giving error when removing a piece from cast sqr
    
    
Emoves = 0
TEtime = 0

# BRUTAL TESTING
# =============================================================================
# =============================================================================

while not gameOver: # while True
    
    # for positionLegal
    color = moveNumber % 2
    
    # MAKE A DICTIONARY & remove from while !!!!!!!!!!!!!!
    # Current turn
    if color == 0: # even = black
        col = "\nBlack"
        
    else: # odd = white
        col = "\nWhite"
        
    print(Fore.GREEN  + col," to move\n" + Fore.RESET)
    
    start1 = time.time()
    OLD_legalMoves = OLD_allLegal(boardState,color,positionKings,BWpieces,castlingStatus)
    for move in OLD_legalMoves:
        OLDmove = moveTOstring(move)
    end1 = time.time()
    
    timeALL = end1-start1
    # print("OLD_legalMoves time: ", timeALL)

    
    # start1 = time.time()

    k = 100
    for i in range(k):
        legalMoves = allLegal(boardState,color,positionKings,BWpieces,castlingStatus)
    # for move in legalMoves:
    #     print('legalMoves: ',moveTOstring(move))
        
    # end1 = time.time()
    # timeAVG = (end1-start1)/k
    # print("Avg allLegal time: ", timeAVG)
    
    # timeALL = end1-start1
    
    #print("allLegal time: ", timeALL)
    # print("")
    # print("num legalMoves: ",len(legalMoves))


    # lst1 = [moveTOstring(move) for move in OLD_legalMoves]
    # lst2 = [moveTOstring(move) for move in legalMoves]
    
    # def comparelists(list1, list2):
    #     return(list1.sort()==list2.sort())
    
    # if not comparelists(lst1, lst2):
    #     print("unmatched lists")
    #     break
    
    #print(comparelists(lst1, lst2))
    
    # print("compare list: ",collections.Counter(OLD_legalMoves) == collections.Counter(legalMoves))

    # start1 = time.time()
    # k = 100
    # for i in range(k):
    #     test = TESTallLegal(boardState,color,positionKings,BWpieces)
    # end1 = time.time()
    # timeAVG = (end1-start1)/k
    # print("Avg TESTallLegal time: ", timeAVG)

    # print("time/avg time",timeALL/timeAVG)

    # opponent's turn
    if color == 1-engineColor: # black = 0, white = 1
        if opponentMode == "user" :
            
            # resign check
            if userString == "r":
                gameOver = True
                print("hehe bye loser")
                break 
            
            userMove = getUserInput(boardState, color, positionKings, BWpieces, castlingStatus)
                
        if opponentMode == "random":
            userMove = (random.choices(legalMoves, k=1))[0]
        
        if opponentMode == "negaABd1":
            userMove = negaAB(boardState,color,positionKings,1,-np.Inf,np.Inf,BWpieces, evalPoints,castlingStatus)[1]
            print("YES EvalPts engine exp bl move: ",moveTOstring(negaAB(boardState, color, positionKings,depth-1,-np.Inf,np.Inf, BWpieces, evalPoints,castlingStatus)[1]))
            

        if opponentMode == "ABd1":
            userMove = alphabeta(boardState, color, positionKings, 1, -np.Inf,np.Inf,BWpieces,castlingStatus)[1]
            print("engine exp bl move: ",moveTOstring(alphabeta(boardState, color, positionKings,depth-1,-np.Inf,np.Inf, BWpieces,evalPoints,castlingStatus)[1]))
            
        print("engine exp bl move: ",moveTOstring(alphabeta(boardState, color, positionKings,depth-1,-np.Inf,np.Inf, BWpieces,castlingStatus)[1]))    
        print("")
        print("chosen move: ",moveTOstring(userMove))
        
    # engine's turn
    else: 
        ### time end
        start = time.time()
        ### time end
        
        if engineMode == "negaAB":
            evalSc, userMove = negaAB(boardState,color,positionKings,depth,-np.Inf,np.Inf,BWpieces, evalPoints,castlingStatus)
            
            print("engine eval score: ", evalSc)
            
        if engineMode == "AB":
            evalSc, userMove = alphabeta(boardState, color, positionKings, depth, -np.Inf,np.Inf, BWpieces,castlingStatus)
            print("engine eval score: ", evalSc)
            
        if engineMode == "MM":
            evalSc, userMove = minimax(boardState,color,positionKings,depth,BWpieces,castlingStatus)
            print("engine eval score: ", evalSc)
        
        ### time end
        end = time.time()
        ### time end
        
        if engineMode == "random":
            userMove = (random.choices(legalMoves, k=1))[0]
        
        if opponentMode == "user" :
            
            # resign check
            if userString == "r":
                gameOver = True
                print("hehe bye loser")
                break 
            
            userMove = getUserInput(boardState, color, positionKings, BWpieces, castlingStatus)
            
        end = time.time()
        
        Etime = end-start
        print("engine time: ", Etime)
        # print("userMove: ", userMove)
        print("")
        print("chosen move: ",moveTOstring(userMove))
        TEtime += Etime
        Emoves += 1
    
    
    
    
    # moves piece on the board & updates position kings after the move is made
    cpc,dpc,evalPoints = movePiece_EVAL(userMove,boardState,positionKings,BWpieces,evalPoints,castlingStatus)
    
    # print("Wh pieces: ",BWpieces[1])
    # print("Bl pieces: ",BWpieces[0])
    # print("positionKings: ",positionKings)
    
    
    ### expected sequence of moves by the ENGINE
    
    if color == engineColor:
        seq = EXPmoveSequence(engineMode,boardState,color,positionKings,depth,BWpieces,evalPoints,castlingStatus)
        print("exp next moves: ",([moveTOstring(move) for move in seq]))    

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

    evalt = None
    k = 100
    start2 = time.time()

    for i in range(k):
        
    # evaluation score            
        #print("\nEvaluation: ", Eval(boardState,color,positionKings,BWpieces,legalMoves))
        evalt = Eval(boardState,color,positionKings,BWpieces,castlingStatus,legalMoves)
    end2 = time.time()
    timeAVG = (end2-start2)/k
    print("\nEvaluation: ", evalt)

    
    print("evalPoints: ",evalPoints)
    print("Fin eval: ",finalEval(boardState, color, positionKings, BWpieces,evalPoints,castlingStatus,legalMoves))
    bfrMove = finalEval(boardState, color, positionKings, BWpieces,evalPoints,castlingStatus,legalMoves)
    print("Undo Fin eval: ",undoMove_EVAL(userMove, cpc, dpc, np.copy(boardState),copy.deepcopy(BWpieces),evalPoints,copy.deepcopy(castlingStatus)))
    aftrMove = undoMove_EVAL(userMove, cpc, dpc, np.copy(boardState),copy.deepcopy(BWpieces),evalPoints,copy.deepcopy(castlingStatus))
    print("Points diff: ",bfrMove - aftrMove)
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
print("AVG engine time: ",TEtime/Emoves)
    
