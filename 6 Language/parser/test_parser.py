import pytest
from parser_mine import *

import os
import sys

fileNames = []
for root, dirs, files in os.walk('sentences'):
    for name in files:
        fileNames.append(int(name.replace('.txt','')))
fileNames.sort()  #;print(f'{fileNames=}')
filePaths = set(os.path.join('sentences',f'{fileName}.txt') for fileName in fileNames)
print(f'{filePaths=}')

could_not_parse = 'Could not parse sentence.'

# @pytest.mark.skip
def test_preprocess():
    for filePath in filePaths:
        with open(filePath) as f:
            s = f.read()
        print(preprocess(s))

# @pytest.mark.skip
def test_nonterminal_sysargv(capsys):
    for filePath in filePaths:
        print(f'Testing nonterminals on {filePath}')
        sys.argv = ['parser_mine.py', filePath] 
        main()
        out, err = capsys.readouterr()
        assert could_not_parse not in out

# @pytest.mark.skip
@pytest.mark.parametrize("sentence,accept_reject",[
    (
        'Holmes sat in the armchair.',
        'accept'
    ),
    (
        'Holmes sat in the red armchair.',
        'accept'
    ),
    (
        'Armchair on the sat Holmes.',
        'reject'
    ),
    (
        'Holmes sat in the the armchair.',
        'reject'
    )
])
def test_nonterminal_input(sentence, accept_reject, monkeypatch, capsys):

    sys.argv = ['parser_mine.py'] 

    print(f'Testing nonterminals on {sentence=}')
    monkeypatch.setattr('builtins.input', lambda input_prompt: sentence)
    main()
    out, err = capsys.readouterr()
    # print(f'{out=}')

    if accept_reject == 'accept':
        assert could_not_parse not in out
    elif accept_reject == 'reject':
        assert could_not_parse in out

@pytest.mark.parametrize('fileNum,expected',[
    ('1', ('holmes',)),
    ('2', ('holmes','a pipe')),
    ('3', ('we', 'the day', 'thursday')),
    ('4', ('holmes', 'armchair', 'he')),
    ('5', ('my companion', 'smile')),
    ('6', ('holmes', 'himself')),
    ('7', ('she', 'a word', 'we', 'the door')),
    ('8', ('holmes', 'his pipe')),
    ('9', ('i', 'walk', 'thursday', 'home', 'mess')),
    ('10', ('i', 'paint', 'the palm', 'my hand'))
])
# @pytest.mark.timeout(4)
def test_np_chunks(fileNum, expected):
    grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
    parser = nltk.ChartParser(grammar)

    with open(os.path.join('sentences',f'{fileNum}.txt')) as f:
        s = f.read()    ;print(f'{s=}')
    s = preprocess(s)
    trees = list(parser.parse(s))
    for tree in trees:
        tree.pretty_print()
        np_chunks = np_chunk(tree)
        # assert len(np_chunks) == len(expected) 
        assert all([" ".join(np.flatten()) in expected for np in np_chunks])