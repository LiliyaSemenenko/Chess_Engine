import numpy as np
import pandas as pd
from colorama import Fore
import random
import time
import copy

# importing functions
from chessFunctions import *

# =============================================================================
# Parameters
# =============================================================================

depth = 2
engineColor = 0
engineMode = "AB" # "MM" , "random"
opponentMode = "user" # "user", "random"

# =============================================================================
# Main game execution loop
# =============================================================================

boardState = initialization()
print("")
printboard(boardState)

gameOver = False

moveNumber = 1

# initialize king's position
positionKing_W = [7,4] # e1
positionKing_B = [0,4] # e8
# both kings in array -> black: bothKings[0], white: bothKings[1]
positionKings = [positionKing_B, positionKing_W] 


# initialize pieces
BlackWhitePieces = [[],[]]

for i in range(8): # rows
    for j in range(8): # columns
        if boardState[i,j,0] != 0:
            BlackWhitePieces[boardState[i,j,1]].append([i,j])


# 0 = play
# 1 = mate
# 2 = draw by insufficient material
# 3 = stalemate

gameStatus ={
    0: "play",
    1: "MATE",
    2: "DRAW by insufficient material",
    3: "STALEMATE",
    }

# promotion piece number
promotion = {
  "q": 2, 
  "r": 3, 
  "b": 4, 
  'n': 5, 
}
# =============================================================================
# =============================================================================
# BRUTAL TESTING

# def TESTmovePiece(userMove,boardState,positionKings,BlackWhitePieces): 
    
#     i = 8-int(userMove[1]) # row
#     j = columnNum[userMove[0]] # column
    
#     k = 8-int(userMove[3]) # row
#     l = columnNum[userMove[2]] # column
    
    
#     # destination square
#     p = boardState[i,j,0] # 6
#     c = boardState[i,j,1] # 1
    
    
#     # update the king
#     if p == 1:
#         # positionKings[c] = userMove[2:4]
#         positionKings[c] = [k,l] # matrix format
    
#     # remove black/white piece from the list if on a current square
#     BlackWhitePieces[c].remove([i,j])
    
#     # adds black/white piece to the list if on a destination square
#     BlackWhitePieces[c].append([k,l])
    
#     dp = boardState[k,l,0]
    
#     if dp != 0:
        
#         BlackWhitePieces[1-c].remove([k,l])

#     # promotion
#     if len(userMove) == 5:
#         p = promotion[userMove[4]] 
        
#     boardState[k,l,0] = p  
#     boardState[k,l,1] = c 
    
#     # current square
#     # ex. a2     (0,6,0) = 6
#     boardState[i,j,0] = 0 
    
#     return boardState




def TESTallLegal(boardState,color,positionKings,BlackWhitePieces):

    listMoves = []    
    
    range_8 = range(8)
    
    listCol = BlackWhitePieces[color]
    listOpp = BlackWhitePieces[1-color]
    
    for piece in listCol:
        i,j = piece # i = 0, j = 1
        moveC = str(numColumn[j]) + str(8-i)
        
        for pieceOpp in listOpp:
            k,l = pieceOpp
        # for k in range_8: # destination rows
        #     for l in range_8: # columns
        #         if (boardState[k,l,1] == (1-color)) or boardState[k,l,0] == 0:
                    # locate the pieces of same color as the engine's turn
            move = moveC + str(numColumn[l]) + str(8-k) 
                    # a = 2+2
                    # promotion pawns
                    # if boardState[i,j,0] == 6 and ((i == 1 and k == 0) or (i == 6 and k == 7)):
                        # for key in promotion.keys():
                            # promMove = move + key
                            
                    #         if checkLegal(promMove,boardState,color,positionKings,BlackWhitePieces):
                    #             listMoves.append(promMove)
                
                    # else:
            if checkLegal(move,boardState,color,positionKings,BlackWhitePieces):
                listMoves.append(move)
                    

    return listMoves

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
    legalMoves = allLegal(boardState,color,positionKings,BlackWhitePieces)
    
    convert = [moveTOstring(userMove) for userMove in legalMoves]
    
    #print("legalMoves: ",convert)
    end1 = time.time()
    timeALL = end1-start1
    print("allLegal time: ", timeALL)

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
                
        print("")
        print("chosen move: ",userMove)
    
    # engine's turn
    else: 
        start = time.time()
        
        if engineMode == "AB":
            evalSc, userMove = alphabeta(boardState,color,positionKings,gameOver,depth,-np.Inf,np.Inf,BlackWhitePieces)
        if engineMode == "MM":
            evalSc, userMove = minimax(boardState,color,positionKings,gameOver,depth,BlackWhitePieces)
        if engineMode == "random":
            userMove = (random.choices(legalMoves, k=1))[0]
        
        end = time.time()

        print("engine time: ", end-start)
        print("chosen move: ",userMove)
        print("eval score: ", evalSc)
        
    
    # moves piece on the board & updates position kings after the move is made
    movePiece(userMove,boardState,positionKings,BlackWhitePieces)
    

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
    
    
    legalMoves = allLegal(boardState,color,positionKings,BlackWhitePieces)

    evaluation = None
    k = 100
    start2 = time.time()

    for i in range(k):
    # evaluation score            
        #print("\nEvaluation: ", Eval(boardState,color,positionKings,gameOver,BlackWhitePieces,legalMoves))
        evaluation = Eval(boardState,color,positionKings,gameOver,BlackWhitePieces,legalMoves)
    end2 = time.time()
    timeAVG = (end2-start2)/k
    print("\nEvaluation: ", evaluation)
    #print("Eval time: ", end2-start2)
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
    print("\nKing in check: ",king_in_check(boardState,opColor,positionKings,BlackWhitePieces))
    
    print("Number of moves: ",moveNumber)
    
    start2 = time.time()
    # checks if opponent is mated or it's a draw since opp not able to move
    status = DrawStalemateMate(boardState,1-color,positionKings,gameOver,BlackWhitePieces)

    
    if status != 0 and status != 4:
        print(Fore.RED  + "\nhehe " + gameStatus[status] + Fore.RESET)
        break
        
    print("_______________________________________")
    moveNumber += 1

# =============================================================================

    
            
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

