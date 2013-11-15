#!/usr/bin/env python
from axiomes import *
from champ_de_bataille import *

assert makecols([]) == [[]] * width

def testmakecols():
    unpadded = makecols([3, 3, 2])
    padded = makecols([3, 3, 2], pad=True)

    assert unpadded == [[], [], [red], [red, black], [], [], []]
    assert len(padded) == width
    for i in range(width):
        assert len(padded[i]) == height
        assert all([left == right for left, right in zip(padded[i], unpadded[i])])

testmakecols()

winner = fourconnected
assert winner([]) == nobody
assert winner([red] * 4) == red
assert winner([black] * 4) == black
assert winner([red, red, red, blank]) == nobody
assert winner([red, red, red, blank]) == nobody
assert winner([red, red, red, blank, red]) == nobody

desc = describe_moves
assert desc([]) == ''
assert desc([0]) == 'a1'
assert desc([0, 0]) == 'a1 a2'
assert desc([0, 6, 0]) == 'a1 g1 a2'

assert str(Board([3, 3, 0, 3, 6, 2])) ==\
'''  a b c d e f g
6              
5              
4              
3       o      
2       o      
1 x   o x     x'''

from menaces import *

assert threateningplayer([blank, blank, red, red]) == nobody
assert threateningplayer([red, black, black, black]) == nobody
assert threateningplayer([red, blank, red, red]) == (red, 1)
assert threateningplayer([black, blank, black, black]) == (black, 1)
assert threateningplayer([red, red, red, blank]) == (red, 3)

try:
    threateningplayer([red, red, red, red])
except AlreadyWon:
    pass
else:
    assert False, 'calling threateningplayer with a 4series should result in an exception'

assert list(window([1, 2, 3], 2)) == [[1, 2], [2, 3]]
expected = [
    [blank, red, red, black],
    [red, red, black, black],
    [red, black, black, black],
    [black, black, black, blank]
]
assert list(window([blank, red, red, black, black, black, blank], 4)) == expected

assert threatindicies([blank, red, red, black, black, black, blank]) == [(black, 6)]

# test that duplicates are collapsed
assert threatindicies([red, red, blank, red, red, red, blank]) == [(red, 2), (red, 6)]

manythreats = Board([0, 0, 1, 1, 2, 2, 2, 0, 2, 0, 2, 1])
print manythreats
print threats(manythreats)
