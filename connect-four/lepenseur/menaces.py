from collections import defaultdict

from axiomes import *
# A double-threat is a combo of two active threats, where opfor does not have any active threats.
# Opfor can block one, but not both of the threats.
# the classic double-threat is turning a 2-group into a 3-group with blanks on both sides

# a more advanced one is the vertical, if a passive threat is just above an active threat for
# the same player, opfor cannot prevent defeat

# double-threats should be noticed by the tactics solver. It should notice the forced move and
# prioritise exploring where it leads.

# even better would be to see the possibilty of a forced move and to try to set up threats that
# could later become forced wins.

# when scoring a position, threats all contribute to the score. Individual threats are also scored
# though, based on context and how promising they are. (So, a threat directly above an enemy's
# threat counts for nothing, since it can never be reached)


def threats(board):
    # a threat is a win-opportunity

    # returns a list of tuples of the form (player, coordinate)
    # where coordinate is (column, row)
    # and player can win by placing a piece at coordinate

    # iterate over all the possible groups, run threatindicies on them, and map the results
    # into coordinate space.

    result = []

    for index, row in enumerate(board.rows):
        for threat in threatindicies(row):
            result += (threat[0], (threat[1], index))

    for index, col in enumerate(board.cols):
        # There's a much more efficient way to generate these.
        for threat in threatindicies(col):
            result += (threat[0], (index, threat[1]))

    def playerat(col, row):
        return board.cols[col][row]

    for diag in diag_indicies:
        group = [playerat(col, row) for col, row in diag]
        for threat in threatindicies(group):
            result += (threat[0], diag[threat[1]])

    return result


# TODO: Move into utils
def window(seq, size):
    result = seq[:size]
    yield result
    for elem in seq[size:]:
        result = result[1:] + [elem]
        yield result


def threatindicies(group):
    result = []
    for index, series in enumerate(window(group, 4)):
        threat = threateningplayer(series)
        if not threat:
            continue
        threat = (threat[0], threat[1] + index)
        if threat not in result:
            result.append(threat)
    return result


class AlreadyWon(Exception):
    pass


def threateningplayer(series):
    # returns a tuple (player, index) or None
    # where index is the position player can make a 4series by playing at
    assert len(series) == 4

    sums = defaultdict(int)
    for player in series:
        sums[player] += 1

    if red in sums and black in sums:
        return nobody

    if sums[blank] == 0:
        raise AlreadyWon('%s is a 4-series' % series)

    if sums[blank] != 1:
        return nobody

    return (red if red in sums else black, series.index(blank))
