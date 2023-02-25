# importing modules
import logging # look for logs file in a directory to find a history of executions and errors
import sys

# importing files
from chessFunctions import *

def main():
    
    #----------------------------------------------
    # Parameters
    #----------------------------------------------
    userColor = 1 # user is white by default
    depth = 4
    MATE_EVALSCORE = 1e3
    
    #----------------------------------------------
    
    logging.basicConfig(filename='logs.txt', level=logging.INFO,
                        format='%(asctime)s %(message)s')
    logging.info('Liliya-Bot started')

    try:
        while True:
                
            msg = input()
            
            logger = logging.getLogger(__name__)

            def send_response(msg: str):
                logger.info(f"< {msg}")
                print(msg)
      
        
            logger.info(f"> {msg}")
        
            if msg == "uci":
        
                send_response("id name Liliya-Bot")
                send_response("id author Liliya")
                send_response("uciok")
                continue
        
            elif msg == "isready":
                send_response("readyok")
                continue
        
            elif msg == "ucinewgame":
                boardState, positionKings, BWpieces, castlingStatus, evalPoints = initialization()
                continue
            
            elif "position startpos" in msg:
                
                if 'moves' in msg: # user: white by default
                    
                    move = msg.split(" ")[-1] # takes last move printed
                    userMove = stringTOmove(move)
                    cpc,dpc,evalPoints = movePiece_EVAL(userMove,boardState,positionKings,BWpieces,evalPoints,castlingStatus)

                else:
                    userColor = 0 # user: black
                    
                continue
                
            # TO DO: implement fen string to set up a board
            elif "position fen" in msg:
                # fen = " ".join(msg.split(" ")[2:])
                # board.set_fen(fen)
                Exception("no fen allowed ")
                continue
        
            elif "go" in msg:
                
                engColor =  1 - userColor
                
                evalSc, Emove = alphabeta(boardState, engColor, positionKings, depth, -MATE_EVALSCORE,MATE_EVALSCORE, BWpieces,castlingStatus)
                cpc,dpc,evalPoints = movePiece_EVAL(Emove,boardState,positionKings,BWpieces,evalPoints,castlingStatus)
                _move = moveTOstring(Emove)
                send_response(f"bestmove {_move}")

                continue
        
            elif msg == "quit":
                sys.exit(0)
                
            else:
                continue
            
    except Exception:
        logging.exception('Fatal error in main loop')


if __name__ == '__main__':
    main()