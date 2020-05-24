import nltk
import sys
import re

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to" | "until"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

# NONTERMINALS = """
# S -> N V
# """

# Based on NONTERMINALS in http://cdn.cs50.net/ai/2020/spring/lectures/6/src6/cfg/cfg1.py
# NONTERMINALS = """
# S -> NP VP | NP VP NP | NP VP PP Conj NP VP | NP VP PP | NP Adv VP NP PP VP PP Adv 
# S -> NP VP Adv Conj VP | NP VP NP PP Conj VP PP

# AP -> Adj | Adj AP
# NP -> N | Det NP | AP NP | N PP
# PP -> P NP
# VP -> V | V NP | V NP PP
# """
NONTERMINALS = """
S -> NP VP | NP VP NP | NP VP PP Conj NP VP | NP VP PP | NP Adv VP NP PP VP PP Adv 
S -> NP VP Adv Conj VP | NP VP NP PP Conj VP PP

AP -> Adj | Adj AP
NP -> N | NP | Det N | Det N VP | AP NP | N PP | N VP | Det Adj NP
PP -> P NP
VP -> V | V NP | V NP PP | V PP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    pattern = re.compile("[A-Za-z]+")
    tokens = nltk.tokenize.word_tokenize(sentence)
    tokens = [token.lower() for token in tokens if pattern.fullmatch(token)]
    return tokens


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # # print(f'{tree=}')
    # np_chunks = []
    
    # for subtree in tree.subtrees():
    #     if subtree.label() == 'NP':
    #         np_chunks.append(subtree)

    # return np_chunks

    # # print(f'{tree=}')
    # chunks = []
    
    # for sub in tree.subtrees():
    #     # print(f'{sub=}\t{sub.height()=}')
    #     if sub.height() <= 3 and sub.label() == 'NP' and sub not in chunks:
    #         # print(f'Appending {sub=} to {chunks=}')
    #         chunks.append(sub)
    #         # print(f'{chunks=}')
    #         return chunks
    #     elif sub.height() > 3:
    #         break    
    #     chunks = np_chunk(sub)

    # return chunks

    # print(f'{tree=}')
    chunks = []
    for sub in tree.subtrees():
        # print(f'{sub=}\t{sub.label()=}\t{sub.height()=}')
        if sub.height() == 3 and sub.label() == 'NP':
            # print(f'Appending {sub=} to {chunks=}')
            chunks.append(sub)  #;print(f'{chunks=}')
    return chunks
    

if __name__ == "__main__":
    main()
