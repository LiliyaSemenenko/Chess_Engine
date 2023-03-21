import numpy as np
from colorama import Fore
import matplotlib.pyplot as plt


# importing functions
from global_parameters import *
from legal_checks import *

# ===========================================================================================
# Functions: printboard, stringTOmove, moveTOstring, getUserInput, validInput, plotEvl
# ===========================================================================================

#PB##########################################################################################

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
    
#SM##########################################################################################

def stringTOmove(userString):

    userMove = np.array([8-int(userString[1]), columnNum[userString[0]],
                        8-int(userString[3]), columnNum[userString[2]], 0])
    if len(userString) == 5:
        userMove[4] = promotion[userString[4]]

    return userMove

#MS##########################################################################################

def moveTOstring(userMove):

    if userMove is None: # checks of the type None
        return "None"

    userString = numColumn[userMove[1]] + str(8-userMove[0]) + numColumn[userMove[3]] + str(8-userMove[2])

    if userMove[4] != 0:
        userString = userString + numPromotion[userMove[4]]

    return userString

#GUI##########################################################################################

def getUserInput(boardState, color, positionKings, BWpieces, castlingStatus,moveCol):
    
    userString = input('Enter current & destination square or resign: ')
    
    if userString == "r":
        print("\n" +Fore.RED + moveCol[color] + " resigned" + Fore.RESET)
        return "r"
    
    # Legality check
    while (not validInput(userString)) or (not checkLegal(stringTOmove(userString),boardState,color,positionKings,BWpieces,castlingStatus)): # while not True = False
        
        print(Fore.RED  + "\nThat move was illegal.\n"+ Fore.RESET)
        
        printboard(boardState)
        
        print("\n" + Fore.GREEN  + moveCol[color]," to move" + Fore.RESET)
        userString = input('Enter current & destination square or resign: ')
        
        if userString == "r":
            print("\n" +Fore.RED + moveCol[color] + " resigned" + Fore.RESET)
            return "r"
        
        continue
    
    userMove = stringTOmove(userString)
    
    return userMove

#VI##########################################################################################

def validInput(userMove):

    allR = [str(i) for i in range(1, 9)]  # "1" - "8"

    if len(userMove) == 4 or len(userMove) == 5:
        
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

#PE##########################################################################################

def plotEvl(status, evalList, moveNumber):
    
    # plot game evaluation where x = move number, y = evaluation
    if status == 1 or status == 2 or status == 3: mn = np.array(range(0,moveNumber+1))
    else: mn = np.array(range(0,moveNumber))
    
    evl = np.array(evalList, dtype = float)
    evl = evl.astype(np.float32)

    if evl[-2] == 0: 
        evl = evl[:-1]
        mn = mn[:-1]
        
    if evl[-1] == 0: 
        evl*=1/np.abs(MATE_EVALSCORE)


    else: evl*=1/np.abs(evl[-1])

    plt.figure(figsize = (6,6))
    plt.plot(mn, evl, color='green')
    plt.ylim([-1,1])
    plt.axhline(0)
    plt.xlabel('Move number')
    plt.ylabel('Evaluation score')
    plt.title("Game evaluation")
    plt.savefig("evalplot.png")
    plt.show()
    
