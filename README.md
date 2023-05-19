## Introduction

Liliya_Bot is a chess engine fully written in Python that utilizes:

- [minimax](https://en.wikipedia.org/wiki/Minimax) algorithm for move searching the best legal moves. The time complexity: O(b^d), where b is the number of legal moves at each point and d is the maximum depth of the tree;
- [alpha-beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning), a simplified and much faster version of the minimax algorithm. Best-case time complexity: O(b^d/2).
- simple evaluation function and an alternative incremental board evaluation. Both evaluation options include piece-square tables;
- [move ordering](https://www.chessprogramming.org/Move_Ordering) based on heuristics like captures, positions on the board, and promotions;
- a [Universal Chess Interface](http://wbec-ridderkerk.nl/html/UCIProtocol.html) to communicate with lichess.org and other GUI of your preference. Liliya_Bot is registered on [lichess](https://lichess.org/@/Liliya_Bot)!
- a command-line user interface.

# Play against Liliya-Bot!
## Use it via command-line

The simplest way to run Liliya_Bot is through the terminal interface. Here's an example of a game when the engine is playing as white at depth 2 vs a random player with black pieces:

`python main.py`

<img src="https://github.com/LiliyaSemenenko/Chess_Engine/blob/master/plots/chess_animation.gif" width="300" height="500">


## Use it as a UCI engine

`python uci.py`

This is how the communication between the engine and GUI can look like (responses have '#'):

```
uci
# id name Liliya-Bot
# id author Liliya
# uciok
isready
# readyok
ucinewgame
position startpos moves e2e4
go
# bestmove g8f6
b1c3
# bestmove b8c6 
```
To quit the game, type `quit`

Note: Liliya_Bot does not accept a FEN string.

<br>

See the [UCI interface doc](https://www.wbec-ridderkerk.nl/html/UCIProtocol.html) for more information on communicating with the engine.

## Connect it to Lichess.org

To play Liliya_Bot on lichess.org, you'll need to use a tool [ShailChoksi/lichess-bot](https://github.com/ShailChoksi/lichess-bot), which acts as a bridge between the Lichess API and chess engines. Additionally, you'll need a BOT account. To use this tool, you'll also need to generate an engine executable file using [pyinstaller](https://www.pyinstaller.org/).

# Tests

To test the engine's performance, an average time engine has used to choose the best move and an evaluation plot are printed after every game. A positive evaluation score means white is winning, negative means black is winning, and 0 is a draw.

Output example where white was clearly winning:

`Average engine time per move:  0.209038734436035` 

![game eval](https://github.com/LiliyaSemenenko/Chess_Engine/blob/master/plots/evalplot.png)

In addition, `python test.py` could be used to run n number of games and test their result and the number of moves it took Liliya_Bot to win. It will also record the number of games, which failed to run till the end due to a bug.

An experiment involving a compilation of 100 games at depth 3, where the engine operated as the white player against a random black player (random mode uses no heuristics and picks any legal move available), was carried out. The outcomes are illustrated in the plots displayed below:
![100 games reslut](https://github.com/LiliyaSemenenko/Chess_Engine/blob/master/plots/testBar_depth_3.png)
![100 games distribution](https://github.com/LiliyaSemenenko/Chess_Engine/blob/master/plots/testHist_depth_3.png)

`Failed games: 0`

# Limitations

Liliya_Bot supports all chess rules, except:

- threefold repetition rule
- fifty-move rule
- fivefold repetition
- seventy-five-move rule
- draw by mutual agreement
- en passant capture

# Contribution

If you would like to contribute by proposing a bug fix or a new feature, please raise an issue. You can also choose to work on an existing issue. If you need any help along the way, feel free to reach out to ([@LiliyaSemenenko](https://github.com/LiliyaSemenenko)).

