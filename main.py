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

def main():
    
    '''
    Depth options:
        any whole number in a range [1,inf).
        
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
    
    # opponent/user
    opponentMode = "random" # Options: "user", "random"
    
    # engine
    depth = 3
    engineColor = 0 # Options: 
                    # 0: black, 1: white.
    
    engineMode = "random" # Options: "random", "MM", "AB", "ABE"
                        # Recommended/fastest mode: "ABE"
                        
    # ===========================================================================================
    # Initialization
    # ===========================================================================================
        
    boardState, positionKings, BWpieces, castlingStatus, evalPoints, moveCol = initialization()
    
    
    moveNumber = 1
    engine_moves = 0
    evalList = []
    evalList.append(0)
    
    print("""
          Welcome to liliya-bot!
          Author: Liliya Semenenko\n
    The new game begins here!
    """)
    
    printboard(boardState)
    
    print("\nTotal number of moves: 0")
    line = "_________________________"
    print(line)
      
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
          
        # compute current evaluation score
        ''' white wins via checkmate: 3000 
            black wins via checkmate: -3000 '''   
        evalBoard = Eval(boardState,color,positionKings,BWpieces,castlingStatus)
        print("Eval:",evalBoard)
        evalList.append(evalBoard)
        
        printboard(boardState)
            
        print("\nTotal number of moves: ",moveNumber, line)
        
        
        # check if opponent is mated or it's a draw/stalemate
        status = DrawStalemateMate(boardState,1-color,positionKings,BWpieces,castlingStatus)

        # 0 = play
        # 1 = mate
        # 2 = draw by insufficient material
        # 3 = stalemate
        # 4 = player in check
        
        if status != 0 and status != 4:
                
            # checkmate 
            if status == 1: 
                print("\n" + Fore.RED + moveCol[color] + " wins by " + gameStatus[status] + Fore.RESET)
            
            # draw/stalemate
            if status == 2 or status == 3: 
                print("\n" + Fore.RED +  gameStatus[status] + Fore.RESET)
                
            print("\nAverage engine time per move: ",engine_time/engine_moves)
                        
            return status, evalList, moveNumber 
            break
        
    
        moveNumber += 1
    
    return status, evalList, moveNumber

# ===========================================================================================
# Calling functions
# ===========================================================================================

# calling main function
status, evalList, moveNumber = main()

# plot the evaluation after each move
plotEvl(status, evalList, moveNumber)