'''
le penseur

functional
instrumented
weighted monte carlo search
tactics solver

run alpha-beta but always search the most promising part of the tree first

solved positions are memoized

taunts annotations
'''

from axiomes import *
import criteres  # run self test
import champ-de-bataille

def score(position):
    if position.winner() == red:
        return infinity

    if position.winner() == black:
        return -infinity

    # and smarter things

def weight(position):
    pass
