import numpy as np
import random
import time
import copy

# importing functions
from global_parameters import *


# =============================================================================
# Functions: printboard, stringTOmove, moveTOstring, validInput
# =============================================================================

def printboard(boardState):

    # dictionary of (chess piece, color): "unicode"

    piece_color = {
        # 0 = black
        (0, 0): "\u2610",  # empty
        (1, 0): "\u265A",  # King
        (2, 0): "\u265B",  # Queen
        (3, 0): "\u265C",  # Rook
        (4, 0): "\u265D",  # Bishop
        (5, 0): "\u265E",  # Knight
        (6, 0): "\u265F",  # Pawn
        # 1 = white
        (0, 1): "\u2610",
        (1, 1): "\u2654",
        (2, 1): "\u2655",
        (3, 1): "\u2656",
        (4, 1): "\u2657",  # Bishop
        (5, 1): "\u2658",  # Knight
        (6, 1): "\u2659",
    }

    for i in range_8:  # rows
        oneRow = str(8-i) + " "
        for j in range_8:  # columns
            p = (boardState[i, j, 0], boardState[i, j, 1])
            oneRow += piece_color[p] + " "
        print(oneRow)

    print("  a  b  c  d  e  f  g  h")
    

def stringTOmove(userString):

    userMove = np.array([8-int(userString[1]), columnNum[userString[0]],
                        8-int(userString[3]), columnNum[userString[2]], 0])
    if len(userString) == 5:
        userMove[4] = promotion[userString[4]]

    return userMove


def moveTOstring(userMove):

    userString = numColumn[userMove[1]] + str(8-userMove[0]) + numColumn[userMove[3]] + str(8-userMove[2])

    if userMove[4] != 0:
        userString = userString + numPromotion[userMove[4]]

    return userString

def getUserInput(boardState, color, positionKings, BWpieces, castlingStatus):
    
    userString = input('Enter current & destination square (ex. a2a3) or "r" to resign: ')

    # Legality check !!!!!!!!! FIX LEGAL INPUTS SHIT in validInput
    while (not validInput(userString)) or (not checkLegal(stringTOmove(userString),boardState,color,positionKings,BWpieces,castlingStatus)): # while not True = False
        print(Fore.RED  + "\nThat move was illegal."+ Fore.RESET)
        print("")
        printboard(boardState)
        print("")
        print(Fore.GREEN  + col," to move\n" + Fore.RESET)
        userString = input('Enter current & destination square (ex. a2a3) or "r" to resign: ')
        userMove = stringTOmove(userString)
        print("")
    
    userMove = stringTOmove(userString)
    
    return userMove



def validInput(userMove):

    allR = [str(i) for i in range(1, 9)]  # "1" - "8"
    
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
            # short castling
                
            if current and destination:
                    return True

        elif len(userMove) == 5:

            letterP = userMove[4]
            promotionL = (letterP in promotion.keys())

            if current and destination and promotionL:
                return True
        
        
    else:
        return False
    