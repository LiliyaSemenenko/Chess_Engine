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

depth = 3

# engine
engineColor = 1
engineMode = "negaAB" # "negaAB", "AB", "MM" , "random"

# opponent
opponentMode = "random" # "negaABd1", "ABd1", "user", "random"

# =============================================================================
# Main game execution loop
# =============================================================================
    
boardState, positionKings, BWpieces, castlingStatus, evalPoints = initialization()

print("positionKings: ",positionKings)

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

###### bl: ABd1  VS  wh: AB depth= 2
# Number of moves:  55
# AVG engine time:  1.2 

###### bl: ABd1  VS  wh: AB depth= 3
# Number of moves:  17
# AVG engine time:  13.5

#--------------------------------------------
# after sorting & move ordering improvement

###### bl: ABd1  VS  wh: AB depth= 2
# Number of moves:  37
# AVG engine time:  0.9 

###### bl: ABd1  VS  wh: AB depth= 3
# Number of moves:  23
# AVG engine time:  6.1

###### bl: ABd1  VS  wh: AB depth= 4
# Number of moves:  43
# AVG engine time: 38.3

# RESULT: faster by a factor of 6
#--------------------------------------------
# after fixing retarded promotion

###### bl: negaABd1  VS  wh: negaAB depth= 2
# Number of moves:  13
# AVG engine time:  0.4

###### bl: negaABd1  VS  wh: negaAB depth= 3
# Number of moves:  63
# AVG engine time:  5.3

###### bl: negaABd1  VS  wh: negaAB depth= 4
# Number of moves:  65
# AVG engine time:  13.5

# RESULT:
    # 1) retarded moves from engine 
    # 2) as depth incr, numMoves increases
    # 3) runtime decreased :)
    
#--------------------------------------------           
# NO evalPoints TEST                                    

###### bl: negaABd1  VS  wh: negaAB depth= 2
# Number of moves:  
# AVG engine time:  

###### bl: negaABd1  VS  wh: negaAB depth= 3
# Number of moves:  63
# AVG engine time:  5.6
# Mistakes: h2h3 instead of eating pawn on d5 or c7
# Move num:  9
# Mate: rk+qn
    
###### bl: negaABd1  VS  wh: negaAB depth= 4
# Number of moves:  
# AVG engine time:  

    #__________________________________________
    # YES evalPoints TEST
    ###### bl: negaABd1  VS  wh: negaAB depth= 3
    # Number of moves:  63
    # AVG engine time:  5.6
    # Mistakes: h2h3 instead of eating pawn on d5 or c7
    # Move num:  9
    # Mate: rk+qn
#--------------------------------------------
# AB test, NO evalPoints

###### bl: ABd1  VS  wh: AB depth= 3
# Number of moves: 29
# AVG engine time:  7.5
# Mistakes: none
# Move num:  
# Mate: bs+qn


# BRUTAL TESTING
# =============================================================================
# =============================================================================

while not gameOver: # while True
    
    # for positionLegal
    color = moveNumber % 2
    
    # MAKE A DICTIONARY & remove from while !!!!!!!!!!!!!!
    # Current turn
    if color == 0: # even = black
        col = "Black"
        
    else: # odd = white
        col = "White"
        
    print("\n",col," to move\n")
    
    ############################################################
    # print("line 155")
    # print("Wh pieces: ",BWpieces[1])
    # print("Bl pieces: ",BWpieces[0])
    
    # printboard(boardState)
    ############################################################
    
    start1 = time.time()
    OLD_legalMoves = OLD_allLegal(boardState,color,positionKings,BWpieces,castlingStatus)
    for move in OLD_legalMoves:
        OLDmove = moveTOstring(move)
    end1 = time.time()
    
    timeALL = end1-start1
    # print("OLD_legalMoves time: ", timeALL)
    
    ############################################################
    # print("line 172")
    # print("Wh pieces: ",BWpieces[1])
    # print("Bl pieces: ",BWpieces[0])
    
    # printboard(boardState)
    ############################################################
    
    
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
    
    ############################################################
    # print("line 199")
    # print("Wh pieces: ",BWpieces[1])
    # print("Bl pieces: ",BWpieces[0])
    
    # printboard(boardState)
    ############################################################


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
            userString = input('Enter current & destination square (ex. a2a3) or "r" to resign: ')
            
            ############################################################
            # print("line 220")
            # print("Wh pieces: ",BWpieces[1])
            # print("Bl pieces: ",BWpieces[0])
            
            # printboard(boardState)
            ############################################################
            

            # Legality check !!!!!!!!! FIX LEGAL INPUTS SHIT in validInput
            while (not validInput(userString)) or (not checkLegal(stringTOmove(userString),boardState,color,positionKings,BWpieces,castlingStatus)): # while not True = False
                print(Fore.RED  + "\nThat move was illegal."+ Fore.RESET)
                print("")
                printboard(boardState)
                print("")
                print("\n",col," to move\n")
                userString = input('Enter current & destination square (ex. a2a3) or "r" to resign: ')
                userMove = stringTOmove(userString)
                print("")
            
            # resign check
            if userString == "r":
                gameOver = True
                print("hehe bye loser")
                break 
            
            userMove = stringTOmove(userString)
                

        if opponentMode == "random":
            userMove = (random.choices(legalMoves, k=1))[0]
        
        if opponentMode == "negaABd1":
            userMove = negaAB(boardState,color,positionKings,1,-np.Inf,np.Inf,BWpieces, evalPoints,castlingStatus)[1]
            print("YES EvalPts engine exp bl move: ",moveTOstring(negaAB(boardState, color, positionKings,depth-1,-np.Inf,np.Inf, BWpieces, evalPoints,castlingStatus)[1]))
            
            
            # TEST: no evalPoints & _EVAL in movePiece, undoMove
            # userMove = negaAB(boardState,color,positionKings,1,-np.Inf,np.Inf,BWpieces)[1]
            # print("NO EvalPts engine exp bl move: ",moveTOstring(negaAB(boardState, color, positionKings,depth-1,-np.Inf,np.Inf, BWpieces)[1]))


        if opponentMode == "ABd1":
            userMove = alphabeta(boardState, color, positionKings, 1, -np.Inf,np.Inf,BWpieces,castlingStatus)[1]
            print("NO EvalPts engine exp bl move: ",moveTOstring(alphabeta(boardState, color, positionKings,depth-1,-np.Inf,np.Inf, BWpieces,castlingStatus)[1]))
            
             
        print("")
        print("chosen move: ",moveTOstring(userMove))
        
    # engine's turn
    else: 
        start = time.time()
        
        if engineMode == "negaAB":
            evalSc, userMove = negaAB(boardState,color,positionKings,depth,-np.Inf,np.Inf,BWpieces, evalPoints,castlingStatus)
            
            
            # TEST: no evalPoints & _EVAL in movePiece, undoMove
            # evalSc, userMove = negaAB(boardState,color,positionKings,depth,-np.Inf,np.Inf,BWpieces)
            
            
            
            print("engine eval score: ", evalSc)
            
        if engineMode == "AB":
            evalSc, userMove = alphabeta(boardState, color, positionKings, depth, -np.Inf,np.Inf, BWpieces,castlingStatus)
            print("engine eval score: ", evalSc)
            
        if engineMode == "MM":
            evalSc, userMove = minimax(boardState,color,positionKings,depth,BWpieces,castlingStatus)
            print("engine eval score: ", evalSc)
            
        if engineMode == "random":
            userMove = (random.choices(legalMoves, k=1))[0]
        
        if opponentMode == "user" :
            userString = input('Enter current & destination square (ex. a2a3) or "r" to resign: ')
            
            
            ###################################33#######################
            # print("line 297")
            # print("Wh pieces: ",BWpieces[1])
            # print("Bl pieces: ",BWpieces[0])
            
            # printboard(boardState)
            ############################################################
            
            
            # Legality check !!!!!!!!! FIX LEGAL INPUTS SHIT in validInput
            while (not validInput(userString)) or (not checkLegal(stringTOmove(userString),boardState,color,positionKings,BWpieces,castlingStatus)): # while not True = False
                print(Fore.RED  + "\nThat move was illegal."+ Fore.RESET)
                print("")
                printboard(boardState)
                print("")
                print("\n",col," to move\n")
                userString = input('Enter current & destination square (ex. a2a3) or "r" to resign: ')
                userMove = stringTOmove(userString)
                print("")
            
            # resign check
            if userString == "r":
                gameOver = True
                print("hehe bye loser")
                break 
            
            userMove = stringTOmove(userString)
            
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
    print("positionKings: ",positionKings)
    
    # castlingStatus = {
    #     # black
    #     "B_castled": False,
    #     # (r,c)
    #     (0,4): 0, # "e8K"  King
    #     (0,7): 0, # "h8R"  short - right
    #     (0,0): 0, # "a8R"  long - left

    #     # white
    #     "W_castled": False,
    #     (7,4): 0, # "e1K"  King
    #     (7,7): 0, # "h1R"  short - right
    #     (7,0): 0, # "a1R"  long - left
    #     }
    
    print("WH castled: ",castlingStatus[(1)])
    print("WH king: ",castlingStatus[(7,4)])
    print("WH rk right: ",castlingStatus[(7,7)])
    print("WH rk left: ",castlingStatus[(7,0)])
    print("")
    print("BL castled: ",castlingStatus[(0)])
    print("BL king: ",castlingStatus[(0,4)])
    print("BL rk right: ",castlingStatus[(0,7)])
    print("BL rk left: ",castlingStatus[(0,0)])
    
    
    
    
    
    
    
    
    
    # if color == engineColor:
    #     seq = moveSequence_negaAB(boardState,color,positionKings,depth,BWpieces,evalPoints,castlingStatus)
            
    #     print("exp next moves: ",([moveTOstring(move) for move in seq]))    

    # start1 = time.time()
    # k = 100
    # for i in range(k):
    #     test = movePiece(userMove,np.copy(boardState),np.copy(positionKings),copy.deepcopy(BWpieces))
    # end1 = time.time()
    # print("Avg TEST movePiece time: ", (end1-start1)/k)


            
                
    # print("positionKings: ",positionKings)
    
    
    # castling check !!!!!!!!
    
    

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
    
    

    # # short castling
    # if userMove == 'e1g1': # white
    #     movePiece('h1f1')
        
    # if userMove == 'e8g8': # black
    #     movePiece('h8f8')

    # # long castling
    # if userMove == 'e1c1': # white
    #     movePiece('a1d1')
        
    # if userMove == 'e8c8': # black
    #     movePiece('a8d8')

