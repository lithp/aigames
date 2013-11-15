from axiomes import *


class InvalidMove(Exception):
    pass


def nextplayer(moves):
    # red is always first
    return red if len(moves) % 2 == 0 else black
assert nextplayer([]) == red
assert nextplayer([3]) == black


class Board(object):
    # todo: instead of generating self.cols from scratch each time, pass them to child boards.

    def __init__(self, moves=[]):
        self.cols = [[blank] * height for _ in range(width)]
        self.moves = []
        self.unsafe_move(moves)

    def __str__(self):
        assert width == 7  # ugly but too much effort to remove for now

        rows =  ['  a b c d e f g']
        for i in range(height, 0, -1):
            row = [str(i)] + [self.cols[col][i-1] for col in range(width)]
            rows.append(' '.join(row))

        return '\n'.join(rows)

    def unsafe_move(self, moves):
        if isinstance(moves, list):
            for move in moves:
                self.unsafe_move(move)
            return self
        col = moves

        try:
            colheight = self.cols[col].index(blank)
        except ValueError:
            raise InvalidMove('no empty space left in col %s' % col)

        self.cols[col][colheight] = nextplayer(self.moves)
        self.moves.append(col)
        return self

    def move(self, move):
        return Board(self.moves).unsafe_move(move)

    def row(self, row):
        return [col[row] for col in self.cols]

    @property
    def rows(self):
        return [self.row(i) for i in range(height)]

    @property
    def diags(self):
        def mapper(coords):
            return [self.columns[col][row] for col, row in coords]
        return [mapper(coords) for coords in diag_indicies]

    def valid_moves(self):
        def valid(move):
            return any([row == ' ' for row in self.columns[move]])
        return [i for i in range(self.COLUMNS) if valid(i)]

    def winner(self):
        def four_connected(row):
            curr = None
            count = 0
            for char in row:
                if char == ' ':
                    curr = None
                    continue
                if char == curr:
                    count += 1
                    if count == 3:
                        return char
                elif char != curr:
                    curr = char
                    count = 0
            return None

        for col in self.columns:
            if four_connected(col):
                return four_connected(col)

        for row in self.rows:
            if four_connected(row):
                return four_connected(row)

        for diag in self.diags:
            if four_connected(diag):
                return four_connected(diag)

        return None

def describe_moves(moves):
    def column(col):
        return chr(ord('a') + col)
    assert column(0) == 'a'
    assert column(6) == 'g'

    rowheights = [0] * width
    result = []
    for move in moves:
        rowheights[move] += 1
        result.append(column(move) + str(rowheights[move]))
    return ' '.join(result)


def makecols(moves, pad=False):
    # a col is a series of moves, starting from the bottom row
    # if reversed, starts from top row
    cols = [[] for _ in range(width)]
    player = red
    for move in moves:
        cols[move].append(player)
        player = black if player == red else red
    if pad:
        for index, col in enumerate(cols):
            cols[index] = col + [blank] * (height - len(col))
    return cols


# predicate.
def fourconnected(group):
    player = nobody
    while group:
        newplayer = group.pop()
        if newplayer in (red, black):
            count = 1 if newplayer != player else count + 1
            player = newplayer
        else:
            assert newplayer == blank
            count = 0
            player = nobody
        if count >= 4:
            return player

    return nobody
