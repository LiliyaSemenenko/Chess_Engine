import matplotlib.pyplot as plt

# importing functions
from main import *
from chessFunctions import *
from ui import *

# ===========================================================================================
# Test functions: testPlot, testEngine
# ===========================================================================================

def testPlot(testData, engineColor, Whmoves, Blmoves, Drmoves, over100moves):
        
    ### plot 1
    gameResult = list(testData.keys())
    totalMoves = list(testData.values())
      
    plt.figure(figsize = (6,6))
            
    # creating the bar plot
    plt.bar(gameResult, totalMoves, color ='maroon', width = 0.4)
    
    plt.xlabel('Game result')
    plt.ylabel('Number of games')
    
    moveCol = initialization()[5]
    
    plt.title("Game evaluation for " + moveCol[engineColor])
    plt.savefig("testBar_depth_"+str(depth)+".png")
    plt.show()
    
    ### plot 2
    plt.figure(figsize = (6,6))
    
    if engineColor == 0: TM = Blmoves
    elif engineColor == 1: TM = Whmoves
    
    if (engineColor == 1 and testData['white wins'] == 0) or (engineColor == 0 and testData['black wins'] == 0): 
        if Drmoves: TM = Drmoves
        else: TM = over100moves
    
    numbins = max(TM) - min(TM) + 1

    plt.hist(TM, rwidth = 0.7, bins = numbins)
    
    plt.xlabel('Number of moves')
    plt.ylabel('Count')
    
    moveCol = initialization()[5]
    
    if TM == Whmoves or TM == Blmoves: plt.title("Distibution of the number of moves when " + moveCol[engineColor] + " wins")
    if TM == Drmoves: plt.title("Distibution of the number of moves after a draw")
    
    if TM == over100moves: pass
    else:   
        plt.savefig("testHist_depth_"+str(depth)+".png")
        plt.show()
    
    
def testEngine(engineColor, engineMode, depth, opponentMode, numberGames):
    
    testData = {}
    whiteWon = 0
    blackWon = 0
    draw = 0
    over100 = 0
    failedGames = 0
    Whmoves = []
    Blmoves = []
    Drmoves = []
    over100moves = []
    n = 1
    
    while n <= numberGames:
        
        try:
            status, evalList, moveNumber = main(engineColor, engineMode, depth, opponentMode)
            plotEvl(status, evalList, moveNumber)
            
            ### checkmate
            if status == 1: 
                
                if engineColor == 0: # black
                    blackWon += 1
                    Blmoves.append(moveNumber)
                    
                if engineColor == 1: # white
                    whiteWon += 1
                    Whmoves.append(moveNumber)
                    
            ### draw/stalemate
            if status == 2 or status == 3: 
                draw += 1
                Drmoves.append(moveNumber)
            
            ### over 100 moves
            if status == 8: 
                over100 += 1
                over100moves.append(100)

            testData['white wins'] = whiteWon
            testData['black wins'] = blackWon
            testData['draw'] = draw
            testData['100 moves'] = over100
            
            n+= 1

        except:
            print('Fatal error in main loop')
            failedGames += 1
            continue
            
        
    testPlot(testData, engineColor, Whmoves, Blmoves, Drmoves, over100moves)
    
    print("Failed games:", failedGames)
    print("Passed")
            
# ===========================================================================================
# Parameters
# ===========================================================================================
'''
Number of games: 
    pick a number of times an engine will execute.

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

numberGames = 100

# engine
depth = 3

engineColor = 1 # Options: 
                # 0: black, 1: white.

engineMode = "ABE" # Options: "random", "MM", "AB", "ABE"
                    # Recommended/fastest mode: "ABE"
                    
# opponent/user
opponentMode = "random" # Options: "user", "random" 

# ===========================================================================================
# Calling a test function
# ===========================================================================================

testEngine(engineColor, engineMode, depth, opponentMode, numberGames)

