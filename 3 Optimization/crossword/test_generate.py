import pytest

from crossword import *
from generate import *

import os

structure_files = []
word_files = []
for f in os.listdir('data'):
    print(f'{f=}')
    if 'structure' in f:
        structure_files.append(f'data/{f}')
    elif 'word' in f:       
        word_files.append(f'data/{f}')

# @pytest.mark.skip()
def test_enforce_node_consistency():

    for structure_file in structure_files:
        print(f'{structure_file=}')

        for words_file in word_files:
            print(f'{words_file=}')

            crossword = Crossword(structure_file, words_file)
            creator = CrosswordCreator(crossword)
            # print(f'Before enforcing consistency: {creator.domains=}')
            creator.enforce_node_consistency()
            # print(f'After enforcing consistency: {creator.domains=}')
            for variable, words in creator.domains.items():
                variable_length = variable.length
                print(f'{variable=}\t{variable_length=}')
                for word in words.copy():
                    # print(f'\t{word=}') 
                    assert len(word) == variable_length

@pytest.mark.skip()
def test_revise():
    crossword = Crossword('data/structure0.txt', 'data/words0.txt')
    creator = CrosswordCreator(crossword)
    creator.enforce_node_consistency()

    print(f'\nBefore revision, {creator.domains=}')
    for x in creator.domains:
        for y in creator.domains.copy():
            revised = creator.revise(x,y)
            print(f'{revised=}')

    print(f'\nAfter revision, {creator.domains=}')
    for x in creator.domains:
        for y in creator.domains.copy():
            revised = creator.revise(x,y)
            print(f'{revised=}')


@pytest.mark.skip()
def test_ac3():
    crossword = Crossword('data/structure0.txt', 'data/words0.txt')
    creator = CrosswordCreator(crossword)
    creator.enforce_node_consistency()

    creator.ac3()
    # print(f'\nBefore revision, {creator.domains=}')
    # for x in creator.domains:
    #     for y in creator.domains.copy():
    #         revised = creator.revise(x,y)
    #         print(f'{revised=}')

    # print(f'\nAfter revision, {creator.domains=}')
    # for x in creator.domains:
    #     for y in creator.domains.copy():
    #         revised = creator.revise(x,y)
    #         print(f'{revised=}')