# =============================================================================
# Parameters
# =============================================================================

range_8 = range(8)

# =============================================================================
# Dictionaries
# =============================================================================

# translating column letters to numbers
columnNum = {
    "a": 0,
    "b": 1,
    "c": 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7,
}

# translating numbers to column letters
numColumn = {
    0: "a",
    1: "b",
    2: "c",
    3: 'd',
    4: 'e',
    5: 'f',
    6: 'g',
    7: 'h',
}

# promotion piece number
promotion = {
    "q": 2,
    "r": 3,
    "b": 4,
    'n': 5,
}

# promotion piece number
numPromotion = {
    2: "q",
    3: "r",
    4: "b",
    5: 'n',
}

# Piece evaluation
pieceEval = {
    # black
    (0, 0): 0,  # empty
    (1, 0): 0,  # King
    (2, 0): -9,  # Queen
    (3, 0): -5,  # Rook
    (4, 0): -3,  # Bishop
    (5, 0): -3,  # Knight
    (6, 0): -1,  # Pawn
    # white
    (0, 1): 0,
    (1, 1): 0,
    (2, 1): 9,
    (3, 1): 5,
    (4, 1): 3,  # Bishop
    (5, 1): 3,  # Knight
    (6, 1): 1,
}


gameStatus ={
    0: "play",
    1: "MATE",
    2: "DRAW by insufficient material",
    3: "STALEMATE",
    }