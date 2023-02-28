import numpy as np
import matplotlib.pyplot as plt

# importing functions
from main import *
from ui import *

def testEngine(status, evalList, moveNumber):
    
    status, evalList, moveNumber = main()
    
    # plot game evaluation
    plotEvl(status, evalList, moveNumber)
    
    while status != 3:
        if __name__ == '__main__':
            status, evalList, moveNumber = main()
        if status == 3:
            break
        
    if status == 3:
        
        # plot game evaluation
        plotEvl(status, evalList, moveNumber)
        
        
# calling the engine
status, evalList, moveNumber = main()

# calling a test function
testEngine(status, evalList, moveNumber)


