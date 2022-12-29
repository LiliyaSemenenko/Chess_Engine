import numpy as np
import pandas as pd
import colorama
from colorama import Fore
import random
import time


# importing functions
from chessFunctions import *

# =============================================================================
# Main game execution loop
# =============================================================================

boardState = initialization()
print("")
printboard(boardState)

gameOver = False

count = 1

# initialize king's position
positionKing_W = str("e") + str(1)
positionKing_B =str("e") + str(8)
# both kings in array
# black: bothKings[0], white: bothKings[1]
positionKings = [positionKing_B, positionKing_W] 

moveNumber = 0
   
depth = 4



 
while not gameOver: # while True
    
    # for positionLegal
    color = count % 2
    
    def moveCount(color):
        # Current turn
        if color == 0: # even = black
            print("\nBlack to move\n")
            
        else: # odd = white
            print("\nWhite to move\n")
        
    moveCount(color)
    
    legalMoves = allLegal(boardState,color,positionKings)
    # if count > 1:
    #     print("legal moves: ", legalMoves)
        
    # me vs engine
    if color == 0: # black = 0, white = 1
# 
        # Obtaining user's input
        #userMove = input('Enter current & destination square (ex. a2a3) or "r" to resign: ')
        userMove = (random.choices(legalMoves, k=1))[0]
        print("")
        
    else: # 
        start = time.time()
        #evalSc, userMove = minimax(boardState,color,positionKings,gameOver,depth)
        evalSc, userMove = alphabeta(boardState,color,positionKings,gameOver,depth,-np.Inf,np.Inf)
        end = time.time()
        
        print("alphabeta time: ", end-start)
        print("chosen move: ",userMove)
        print("eval score: ", evalSc)
        
        #userMove = input('Enter current & destination square (ex. a2a3) or "r" to resign: ')
        
        #userMove = (random.choices(legalMoves, k=1))[0]
    
    # # checks for both position and square IN check
    # def TESTcheckLegal(userMove, boardState, color, positionKings):
        
    #     ###### king IN check ######
        
    #     # is position of intended userMove legal ?
    #     positionL = positionLegal(userMove,boardState,color)
        
    #     if positionL:
            
    #         # expected board with last user input
    #         boardExp = movePiece(userMove,boardState)
            
    #         # is king IN check?
    #         kingINcheck = king_in_check(boardExp, color, positionKings)
            
    #         if not kingINcheck:
    #             return True
                
    #     # returns True if: positionL = True and squareCheck = False
    #     return False
    
    # start2 = time.time()
    # RunLegal = checkLegal(userMove, boardState, color, positionKings)
    # end2 = time.time()
    # print("with copy: ",end2 - start2)
    
    # start = time.time()
    # testLegal = TESTcheckLegal(userMove, boardState, color, positionKings)
    # end = time.time()
    # print("no copy: ",end-start)
    

    
    
    # Legality check
    while (not validInput(userMove)) or (not checkLegal(userMove,boardState,color,positionKings)): # while not True = False
        print(Fore.RED  + "\nThat move was illegal."+ Fore.RESET)
        print("")
        printboard(boardState)
        print("")
        moveCount(color)
        userMove = input('Enter current & destination square (ex. a2a3) or "r" to resign: ')
        print("")
     
    
    # resign check
    if userMove == "r":
        gameOver = True
        print("hehe bye loser")
        break 
    
    # record current king's square 
    # if king moved
    if userMove[0:2] == positionKings[1]: # white
        positionKings[1] = userMove[2:4]
    
    if userMove[0:2] == positionKings[0]: # black
        positionKings[0] = userMove[2:4] 
    
    # moves piece on the board
    movePiece(userMove,boardState)
    
    
    # castling check
    
    
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

    # print board
    printboard(boardState)

    # evaluation score            
    print("\nEvaluation: ", Eval(boardState,color,positionKings,gameOver))
    
    # opposite color from king
    opColor = 1 - color
    print("\nKing in check: ",king_in_check(boardState,opColor,positionKings))
    moveNumber += 1
    print("Number of moves: ",moveNumber)
    
    # checks if opponent is mated or it's a draw since opp not able to move
    status = DrawStalemateMate(boardState,1-color,positionKings,gameOver)
    
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
    
    if status != 0:
        print(Fore.RED  + "\nhehe " + gameStatus[status] + Fore.RESET)
        break
        
    print("_________________________________________________")
    count += 1

# =============================================================================




































# Set up 2D board
# =============================================================================
# for i in range(8): # column_size
#     #for j in [0,1,6,7]:
#         
#         board2D[0,i] = piece_col[(boardState[0,i,0],boardState[0,i,1])]
#     
#     
# #print((boardState[6,1,0],boardState[6,1,1]))
# 
# print(piece_col[(boardState[6,1,0],boardState[6,1,1])])
# 
# 
# =============================================================================




# board = insert([1,2,3],2, value)

# x=np.zeros((8,8,2))
# x[0,0,0] = 11
# x[1,0,0] = 21
# x[0,1,1] = 111
# print(x)

# function accepts the matrix as input, prints out that board in Unicode
# def setboard():
#     positionsList = 
#     boardState = insert(array,position, value, axis)
# setboard()

# #Declaring an empty 1D array.
# a = []
# #Declaring an empty 1D array.
# b = []
# #Initialize the column.
# for j in range(0, column_size):
#     b.append(0)
# #Append the column to each row.
# for i in range(0, row_size):
#     a.append(b)
# #Printing the 2d created array
# print(a)



