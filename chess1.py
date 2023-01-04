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
engineColor = 1
engineMode = "AB" # "AB", "MM" , "random"
opponentMode = "ABd1" # "user", "random", "ABd1

# =============================================================================
# Main game execution loop
# =============================================================================

boardState, positionKings, BlackWhitePieces = initialization()

print("")
printboard(boardState)

gameOver = False

moveNumber = 1

evalPoints = 0

# =============================================================================
# =============================================================================
# BRUTAL TESTING

Emoves = 0
TEtime = 0

###### bl: ABd1  VS  wh: AB depth=2
# Number of moves:  55
# AVG engine time:  1.2 

###### bl: ABd1  VS  wh: AB depth=3
# Number of moves:  17
# AVG engine time:  13.5

#--------------------------------------------
# after sorting & move ordering improvement

###### bl: ABd1  VS  wh: AB depth=2
# Number of moves:  37
# AVG engine time:  0.9 

###### bl: ABd1  VS  wh: AB depth=3
# Number of moves:  23
# AVG engine time:  6.1

###### bl: ABd1  VS  wh: AB depth=4
# Number of moves:  43
# AVG engine time: 38.3

# RESULT: faster by a factor of 6

#--------------------------------------------


# BRUTAL TESTING
# =============================================================================
# =============================================================================

while not gameOver: # while True
    
    # for positionLegal
    color = moveNumber % 2
    
    # MAKE A DICTIONARY & remove from while !!!!!!!!!!!!!!
    # Current turn
    if color == 0: # even = black
        print("\nBlack to move\n")
        
    else: # odd = white
        print("\nWhite to move\n")
    
    start1 = time.time()
    OLD_legalMoves = OLD_allLegal(boardState,color,positionKings,BlackWhitePieces)
    for move in OLD_legalMoves:
        OLDmove = moveTOstring(move)
    end1 = time.time()
    
    timeALL = end1-start1
    print("OLD_legalMoves time: ", timeALL)
    

    start1 = time.time()

    k = 100
    for i in range(k):
        legalMoves = allLegal(boardState,color,positionKings,BlackWhitePieces)
    # for move in legalMoves:
    #     print('legalMoves: ',moveTOstring(move))
        
    end1 = time.time()
    timeAVG = (end1-start1)/k
    print("Avg allLegal time: ", timeAVG)
    
    timeALL = end1-start1
    
    #print("allLegal time: ", timeALL)
    print("")
    print("num legalMoves: ",len(legalMoves))
    


    lst1 = [moveTOstring(move) for move in OLD_legalMoves]
    lst2 = [moveTOstring(move) for move in legalMoves]
    
    def comparelists(list1, list2):
        return(list1.sort()==list2.sort())
    
    if not comparelists(lst1, lst2):
        print("unmatched lists")
        break
    
    #print(comparelists(lst1, lst2))
    
    # print("compare list: ",collections.Counter(OLD_legalMoves) == collections.Counter(legalMoves))

    # start1 = time.time()
    # k = 100
    # for i in range(k):
    #     test = TESTallLegal(boardState,color,positionKings,BlackWhitePieces)
    # end1 = time.time()
    # timeAVG = (end1-start1)/k
    # print("Avg TESTallLegal time: ", timeAVG)

    # print("time/avg time",timeALL/timeAVG)

    # opponent's turn
    if color == 1-engineColor: # black = 0, white = 1
        if opponentMode == "user" :
            userString = input('Enter current & destination square (ex. a2a3) or "r" to resign: ')
            
            # Legality check !!!!!!!!! FIX LEGAL INPUTS SHIT in validInput
            while (not validInput(userString)) or (not checkLegal(stringTOmove(userString),boardState,color,positionKings,BlackWhitePieces)): # while not True = False
                print(Fore.RED  + "\nThat move was illegal."+ Fore.RESET)
                print("")
                printboard(boardState)
                print("")
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
        
        if opponentMode == "ABd1":
            userMove = alphabeta(boardState,color,positionKings,1,-np.Inf,np.Inf,BlackWhitePieces,evalPoints)[1]
            
            
            
        print("")
        print("chosen move: ",moveTOstring(userMove))
        
    # engine's turn
    else: 
        start = time.time()
        
        if engineMode == "AB":
            evalSc, userMove = alphabeta(boardState,color,positionKings,depth,-np.Inf,np.Inf,BlackWhitePieces,evalPoints)
        if engineMode == "MM":
            evalSc, userMove = minimax(boardState,color,positionKings,depth,BlackWhitePieces)
        if engineMode == "random":
            userMove = (random.choices(legalMoves, k=1))[0]
        
        end = time.time()
        
        Etime = end-start
        print("engine time: ", Etime)
        print("userMove: ", userMove)
        print("chosen move: ",moveTOstring(userMove))
        print("engine eval score: ", evalSc)
        TEtime += Etime
        Emoves += 1
    
    
    
    
    # moves piece on the board & updates position kings after the move is made
    cpc,dpc,evalPoints = movePiece_EVAL(userMove,boardState,positionKings,BlackWhitePieces,evalPoints)
    

    # start1 = time.time()
    # k = 100
    # for i in range(k):
    #     test = movePiece(userMove,np.copy(boardState),np.copy(positionKings),copy.deepcopy(BlackWhitePieces))
    # end1 = time.time()
    # print("Avg TEST movePiece time: ", (end1-start1)/k)


            
                
    print("positionKings: ",positionKings)
    
    
    # castling check !!!!!!!!
    
    

    # print board
    printboard(boardState)
    
    # # TEST
    # if moveNumber == 7:
    #     undoMove(userMove,cpc,dpc,boardState,BlackWhitePieces)
    #     printboard(boardState)
    #     break
    # # TEST
    
    
    
    
    # legalMoves = allLegal(boardState,color,positionKings,BlackWhitePieces)

    evalt = None
    k = 100
    start2 = time.time()

    for i in range(k):
        
    # evaluation score            
        #print("\nEvaluation: ", Eval(boardState,color,positionKings,BlackWhitePieces,legalMoves))
        evalt = Eval(boardState,color,positionKings,BlackWhitePieces,legalMoves)
    end2 = time.time()
    timeAVG = (end2-start2)/k
    print("\nEvaluation: ", evalt)

    
    
    # print("New eval: ",evalPoints)
    # print("")
    # if round(evalPoints-evalt,10) != 0:
    #     print("eval NOT same")
    #     break
    
    
    print("Avg Eval time: ", timeAVG)
    
    
    
    
    
    
    # start1 = time.time()
    # k = 100
    # for i in range(k):
    #     test = TESTallLegal(boardState,color,positionKings,BlackWhitePieces)
    # end1 = time.time()
    # timeAVG = (end1-start1)/k
    # print("Avg TESTallLegal time: ", timeAVG)

    
    # opposite color from king
    opColor = 1 - color
    
    start = time.time()
    k = 100
    for i in range(k):
        check = king_in_check(boardState,opColor,positionKings,BlackWhitePieces)
    end = time.time()
    timeAVG = (end-start)/k
    print("\nKing in check: ",check)
    print("King in check AVG time: ", timeAVG)
    
    print("Number of moves: ",moveNumber)
    
    start2 = time.time()
    # checks if opponent is mated or it's a draw since opp not able to move
    status = DrawStalemateMate(boardState,1-color,positionKings,BlackWhitePieces)

    
    if status != 0 and status != 4:
        print(Fore.RED  + "\nhehe " + gameStatus[status] + Fore.RESET)
        break
        
    print("_______________________________________")
    moveNumber += 1

# =============================================================================
print("AVG engine time: ",TEtime/Emoves)
         




    #     # 0 = play
    #     # 1 = mate
    #     # 2 = draw by insufficient material
    #     # 3 = stalemate
        
    #     startD = time.time()
    #     # checks for game status
    #     status = DrawStalemateMate(boardState,color,positionKings,gameOver,legalMoves)
    #     endD = time.time()
    #     print(" DrawStalemateMate time in func: ", endD-startD)
        
    #     if status == 1:
    #         # black or white gets mated
    #         sumPoints = (1 - 2*color)*np.Inf # white or black wins
    #         return sumPoints
            
    #     if status == 2 or status == 3:
    #         sumPoints = 0
    #         return sumPoints
        
    #     startN = time.time()
    #     # calculates total evaluation score
    #     sumPoints = 0
        
    #     range_8 = range(8)
    #     Npieces_BL = 0
    #     Npieces_WH = 0
        
    #     for i in range_8:
    #         for j in range_8:
    #             b = boardState[i,j,:] 
    #             c = b[1]
                
    #             if b[0] != 0:
    #                 if c == 0:
    #                     Npieces_BL += 1
    #                 if c ==1:
    #                     Npieces_WH += 1
                        
    #     endN = time.time()
    #     print("search for num of pieces: ",endN-startN)
        
    #     startP = time.time()        
    #     for i in range_8:
    #         for j in range_8:
    #             b = boardState[i,j,:] 
    #             c = b[1]
                
    #             # add points for moving pawn towards promotion
    #             if b[0] == 6 and i < 7:
    #                 if c == 0 and Npieces_BL < 12: # black
    #                     BLprom = -(1e-5)*(i-1)
    #                     sumPoints += BLprom
                        
    #                 if c == 1 and Npieces_WH < 12: # white
    #                     WHprom = (1e-5)*(6-i)   
    #                     sumPoints += WHprom
    #             # add points when pushing pawns        
    #             if i in range(1,7) and j in range(2,6) and b[0] != 0:
    #                 #c = b[1]
    #                 centerPoints = (1e-5)*(2*c-1)
    #                 sumPoints += centerPoints
                    
    #             # piece, color
    #             sumPoints += pieceEval[(b[0],b[1])]
    #     endP = time.time()
    #     print("search all pieces and assign eval: ", endP-startP)
                
                
    #     return sumPoints # output evaluation score 
    
    
    # testEval(boardState,color,positionKings,gameOver,legalMoves)
    # endTE = time.time()
    # print("Test eval time: ", endTE-startTE)
    
    
    
    
    

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

