## Introduction

Liliya_Bot is a chess engine fully written in Python that utilizes:

- [minimax](https://en.wikipedia.org/wiki/Minimax#Minimax_algorithm_with_alternate_moves) algorithm for move searching the best legal moves. The time complexity: O(b^d), where b is the number of legal moves at each point and m is the maximum depth of the tree;
- [alpha-beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning), a simplified and much faster version of the minimax algorithm. Best-case time complexity: O(b^d/2).
- simple evaluation function and an alternative incremental board evaluation. Both evaluation options include piece-square tables;
- [move ordering](https://www.chessprogramming.org/Move_Ordering) based on heuristics like captures, positions on the board, and promotions;
- a [Universal Chess Interface](http://wbec-ridderkerk.nl/html/UCIProtocol.html) to communicate with lichess.org and other GUI of your preference. Liliya_Bot is registered on [lichess](https://lichess.org/@/Liliya_Bot)!
- a command-line user interface.

# Play against Liliya-Bot!
## Use it via command-line

The simplest way to run Liliya_Bot is through the terminal interface:

`python main.py`

<pre>
_________________________
White  to move

Enter current & destination square or resign: e2e4

evaluation:  40 

8 ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜ 
7 ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟ 
6 ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ 
5 ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ 
4 ☐ ☐ ☐ ☐ ♙ ☐ ☐ ☐ 
3 ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ 
2 ♙ ♙ ♙ ♙ ☐ ♙ ♙ ♙ 
1 ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖ 
  a  b  c  d  e  f  g  h

Total number of moves:  1 
_________________________
Black  to move

chosen move: g8f6 

evaluation:  -10 

8 ♜ ♞ ♝ ♛ ♚ ♝ ☐ ♜ 
7 ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟ 
6 ☐ ☐ ☐ ☐ ☐ ♞ ☐ ☐ 
5 ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ 
4 ☐ ☐ ☐ ☐ ♙ ☐ ☐ ☐ 
3 ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ 
2 ♙ ♙ ♙ ♙ ☐ ♙ ♙ ♙ 
1 ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖ 
  a  b  c  d  e  f  g  h

Total number of moves:  2 
_________________________
</pre>

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

<br>

## Lichess.org

To play Liliya_Bot on lichess.org, you'll need to use a tool [ShailChoksi/lichess-bot](https://github.com/ShailChoksi/lichess-bot), which acts as a bridge between the Lichess API and chess engines. Additionally, you'll need a BOT account. To use this tool, you'll also need to generate an engine executable file using [pyinstaller](https://www.pyinstaller.org/).

<br>

# Tests

`python test.py`

![game eval](https://raw.github.com/thomasahle/sunfish/master/docs/logo/sunfish_large.png)
![number of wins](https://raw.github.com/thomasahle/sunfish/master/docs/logo/sunfish_large.png)
![number of moves to win](https://raw.github.com/thomasahle/sunfish/master/docs/logo/sunfish_large.png)

<br>

# Limitations

Liliya_Bot supports all chess rules, except:

- threefold repetition rule
- fifty-move rule
- fivefold repetition
- seventy-five-move rule
- draw by mutual agreement
- en passant capture

<br>

# Contribution

If you would like to contribute by proposing a bug fix or a new feature, please raise an issue. You can also choose to work on an existing issue. If you need any help along the way, feel free to reach out to ([@LiliyaSemenenko](https://github.com/LiliyaSemenenko)).

