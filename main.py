import numpy as np
from colorama import Fore
import random
import time
import copy
import collections
import matplotlib.pyplot as plt

# importing functions
from chessFunctions import *

# ===========================================================================================
# Parameters
# ===========================================================================================

'''
Depth options:
    any whole number in range [1,inf).
    
Color options: 
    0: black, 
    1: white.
    
Mode options:
    "user": user mannualy inputs their move in console in long algebraic notation (ex: "a2a3"),
    "random": any random legal move is played,
    "MM": MiniMax algorithm, 
    "AB": Alpha–beta pruning algorithm without incremental heuristic value updating,
    "ABE": Alpha–beta pruning algorithm with incremental heuristic value updating.
'''

depth = 3
engineColor = 1

# engine
engineMode = "ABE" # Options: "random", "MM", "AB", "ABE"
                   # Recommended/fastest mode: "ABE"
                    
# opponent/user
opponentMode = "random" # Options: "user", "random"

# ===========================================================================================
# Initialization
# ===========================================================================================
    
boardState, positionKings, BWpieces, castlingStatus, evalPoints, moveCol = initialization()

moveNumber = 1
engine_moves = 0
evalList = []
evalList.append(0)

print("Welcome to the game!\n")
printboard(boardState)
print("\nTotal number of moves: 0")
print("_________________________\n")
  
# ===========================================================================================
# Main game execution loop
# ===========================================================================================

while 1: 
    
    color = moveNumber % 2
    print(Fore.GREEN  + moveCol[color]," to move" + Fore.RESET)
            
    # opponent's turn
    if color == 1-engineColor:
        
        if opponentMode == "user" :
            userMove = getUserInput(boardState, color, positionKings, BWpieces, castlingStatus,moveCol)

            if str(userMove) == "r": break
            
        if opponentMode == "random":
            legalMoves = allLegal(boardState,color,positionKings,BWpieces,castlingStatus)
            userMove = (random.choices(legalMoves, k=1))[0]
        
        print("\nchosen move:", moveTOstring(userMove),"\n")
        
    # engine's turn
    else: 
        
        start = time.time()
            
        if engineMode == "AB":
            evalSc, userMove = alphabeta(boardState, color, positionKings, depth, -MATE_EVALSCORE,MATE_EVALSCORE, BWpieces,castlingStatus)
            
        if engineMode == "ABE":
            evalSc, userMove = alphabeta_EVAL(boardState, color, positionKings, depth, -MATE_EVALSCORE,MATE_EVALSCORE, BWpieces,evalPoints,castlingStatus) 
            
        if engineMode == "MM":
            evalSc, userMove = minimax(boardState,color,positionKings,depth,BWpieces,castlingStatus)

        if engineMode == "random":
            legalMoves = allLegal(boardState,color,positionKings,BWpieces,castlingStatus)
            userMove = (random.choices(legalMoves, k=1))[0]
        
        if engineMode == "user" :
            userMove = getUserInput(boardState, color, positionKings, BWpieces, castlingStatus)
            
        end = time.time()
    
        engine_time = end-start
        engine_moves += 1
        
        print("\nchosen move:", moveTOstring(userMove),"\n")

    # update the board
    cpc,dpc,evalPoints = movePiece_EVAL(userMove,boardState,positionKings,BWpieces,evalPoints,castlingStatus)
    
    evalBoard = Eval(boardState,color,positionKings,BWpieces,castlingStatus)
    evalList.append(evalBoard)
    
    printboard(boardState)

    print("\nTotal number of moves: ",moveNumber)
    
    # check if opponent is mated or it's a draw/stalemate
    status = DrawStalemateMate(boardState,1-color,positionKings,BWpieces,castlingStatus)
    
    if status != 0 and status != 4:
        print("\n" +Fore.RED + gameStatus[status] + Fore.RESET)
        break
    
    print("_________________________")
    
    moveNumber += 1
    

# ===========================================================================================
# Testing portion 
# ===========================================================================================

print("\nAverage engine time per move: ",engine_time/engine_moves)

# plot game evaluation where x = move number, y = evaluation
plt.plot(np.array(range(0,moveNumber+1)),np.array(evalList), color='green', marker = "o",) 
plt.xlabel('Move number')
plt.ylabel('Evaluation score')
plt.title("Game evaluation")
plt.show()