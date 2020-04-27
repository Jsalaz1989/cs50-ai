from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Puzzle structure
    And(Or(AKnight, AKnave), Implication(AKnight, Not(AKnave))),      # XOR for A

    # Statements
    Biconditional(AKnight, And(AKnight, AKnave))    # A says "I am both a knight and a knave."
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Puzzle structure
    And(Or(AKnight, AKnave), Implication(AKnight, Not(AKnave))),      # XOR for A
    And(Or(BKnight, BKnave), Implication(BKnight, Not(BKnave))),      # XOR for B

    # Statements
    Biconditional(AKnight, And(AKnave, BKnave))     # A says "We are both knaves."
    # B says nothing.
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # Puzzle structure
    And(Or(AKnight, AKnave), Implication(AKnight, Not(AKnave))),      # XOR for A
    And(Or(BKnight, BKnave), Implication(BKnight, Not(BKnave))),      # XOR for B

    # Statements
    Biconditional(AKnight, Or(And(AKnight,BKnight), And(AKnave,BKnave))),               # A says "We are the same kind."
    Biconditional(BKnight, Or(And(AKnight,Not(BKnight)), And(AKnave,Not(BKnave))))      # B says "We are of different kinds."
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Puzzle structure
    And(Or(AKnight, AKnave), Implication(AKnight, Not(AKnave))),      # XOR for A
    And(Or(BKnight, BKnave), Implication(BKnight, Not(BKnave))),      # XOR for B
    And(Or(CKnight, CKnave), Implication(CKnight, Not(CKnave))),      # XOR for C

    # Statements
    Biconditional(Or(AKnight, AKnight), Or(AKnight, AKnave)),       # A says either "I am a knight." or "I am a knave.", but you don't know which.
    Biconditional(BKnight, Biconditional(AKnight,AKnave)),          # B says "A said 'I am a knave'."
    Biconditional(BKnight, CKnave),                                 # B says "C is a knave."
    Biconditional(CKnight, AKnight)                                 # C says "A is a knight."
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
