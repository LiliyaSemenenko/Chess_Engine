import numpy as np
import matplotlib.pyplot as plt

# importing functions
from main import *

def testEngine(status, evalList, moveNumber):
    
    status, evalList, moveNumber = main()
     
    while status != 3:
        if __name__ == '__main__':
            status, evalList, moveNumber = main()
        if status == 3:
            break
        
    if status == 3:
        print("status:", status)
        
        # plot game evaluation where x = move number, y = evaluation
        mn = np.array(range(0,moveNumber+1))
        evl = np.array(evalList, dtype = float)
        evl = evl.astype(np.float32)
        print("original:",evl)
        
        if evl[-2] == 0: 
            evl = evl[:-1]
            mn = mn[:-1]
            
        if evl[-1] == 0: 
            evl*=1/np.abs(MATE_EVALSCORE)
        
        
        else: evl*=1/np.abs(evl[-1])
        
        print("scaled",evl)
        
        plt.figure(figsize = (6,6))
        plt.plot(mn, evl, color='green')
        plt.ylim([-1,1])
        plt.axhline(0)
        plt.xlabel('Move number')
        plt.ylabel('Evaluation score')
        plt.title("Game evaluation")
        plt.savefig("evalplot.png")
        plt.show()
        
        
# calling the engine
status, evalList, moveNumber = main()

# calling a test function
testEngine(status, evalList, moveNumber)