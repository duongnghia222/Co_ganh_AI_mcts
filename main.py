import numpy as np
"""
    ganh -> vay
    no ganh -> ganh
    1 is o, -1 is x, 0 is empty
    the AI holds x -> ai = -1
"""
human = 1
ai = -1
empty = 0
symmetric_lookup_table = {
    (0, 1): [((0, 0), (0, 2))],
    (0, 2): [((0, 1), (0, 3))],
    (0, 3): [((0, 2), (0, 4))],
    (1, 0): [((0, 0), (2, 0))],
    (2, 0): [((1, 0), (3, 0))],
    (3, 0): [((2, 0), (4, 0))],
    (4, 1): [((4, 0), (4, 2))],
    (4, 2): [((4, 1), (4, 3))],
    (4, 3): [((4, 2), (4, 4))],
    (3, 4): [((2, 4), (4, 4))],
    (2, 4): [((1, 4), (3, 4))],
    (1, 4): [((0, 4), (2, 4))],
    (1, 1): [((0, 1), (2, 1)), ((0, 2), (2, 0)), ((1, 2), (1, 0)), ((2, 2), (0, 0))],
    (1, 3): [((0, 3), (2, 3)), ((0, 4), (2, 2)), ((1, 4), (1, 2)), ((2, 4), (0, 2))],
    (2, 2): [((1, 2), (3, 2)), ((1, 3), (3, 1)), ((2, 3), (2, 1)), ((3, 3), (1, 1))],
    (3, 1): [((2, 1), (4, 1)), ((2, 2), (4, 0)), ((3, 2), (3, 0)), ((4, 2), (2, 0))],
    (3, 3): [((2, 3), (4, 3)), ((2, 4), (4, 2)), ((3, 4), (3, 2)), ((4, 4), (2, 2))],
    (1, 2): [((0, 2), (2, 2)), ((1, 3), (1, 1))],
    (3, 2): [((2, 2), (4, 2)), ((3, 3), (3, 1))],
    (2, 1): [((1, 1), (3, 1)), ((2, 2), (2, 0))],
    (2, 3): [((1, 3), (3, 3)), ((2, 4), (2, 2))],
    (0, 0): [],
    (0, 4): [],
    (4, 0): [],
    (4, 4): [],
}

move_lookup_table = {
    (0, 1): [(0, 0), (0, 2), (1, 1)],
    (0, 2): [(0, 1), (0, 3), (1, 2)],
    (0, 3): [(0, 2), (0, 4), (1, 3)],
    (1, 0): [(0, 0), (2, 0), (1, 1)],
    (2, 0): [(1, 0), (3, 0), (2, 1)],
    (3, 0): [(2, 0), (4, 0), (3, 1)],
    (4, 1): [(4, 0), (4, 2), (3, 1)],
    (4, 2): [(4, 1), (4, 3), (3, 2)],
    (4, 3): [(4, 2), (4, 4), (3, 3)],
    (3, 4): [(2, 4), (4, 4), (3, 3)],
    (2, 4): [(1, 4), (3, 4), (2, 3)],
    (1, 4): [(0, 4), (2, 4), (1, 3)],
    (1, 1): [(0, 1), (2, 1), (0, 2), (2, 0), (1, 2), (1, 0), (2, 2), (0, 0)],
    (1, 3): [(0, 3), (2, 3), (0, 4), (2, 2), (1, 4), (1, 2), (2, 4), (0, 2)],
    (2, 2): [(1, 2), (3, 2), (1, 3), (3, 1), (2, 3), (2, 1), (3, 3), (1, 1)],
    (3, 1): [(2, 1), (4, 1), (2, 2), (4, 0), (3, 2), (3, 0), (4, 2), (2, 0)],
    (3, 3): [(2, 3), (4, 3), (2, 4), (4, 2), (3, 4), (3, 2), (4, 4), (2, 2)],
    (1, 2): [(0, 2), (2, 2), (1, 3), (1, 1)],
    (3, 2): [(2, 2), (4, 2), (3, 3), (3, 1)],
    (2, 1): [(1, 1), (3, 1), (2, 2), (2, 0)],
    (2, 3): [(1, 3), (3, 3), (2, 4), (2, 2)],
    (0, 0): [(0, 1), (1, 1), (1, 0)],
    (0, 4): [(1, 4), (1, 3), (0, 3)],
    (4, 0): [(3, 0), (3, 1), (4, 1)],
    (4, 4): [(4, 3), (3, 3), (3, 4)],

}


class game:
    def __init__(self, prev_board, board, player):
        self.player = player
        self.opponent = -1 * self.player
        self.prev_board = [x[:] for x in prev_board]  # copy
        self.board = [x[:] for x in board]

    def get_old_position(self):
        """
        get move of the human: find the position that in board its value is 0 but in the
        previous board its value is 1 (human)
        :return: old position of chessman which human moved
        """
        mask_board = np.subtract(self.prev_board, self.board)  # board - prev_board
        # find position has value = -1 -> old position
        for i in range(5):
            for j in range(5):
                if mask_board[i][j] == self.opponent:
                    return i, j
        return None

    def check_trap(self):
        pre_pos = self.get_old_position()
        symmetric_tuples = symmetric_lookup_table[pre_pos]
        traps = []
        for p in symmetric_tuples:
            if get_board_at_tuple(self.board, p[0]) == self.opponent and \
                    get_board_at_tuple(self.board, p[1]) == self.opponent:
                traps.append(p)
        return traps

    def find_all_chessmen(self, player):
        chessmen = []
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == player:
                    chessmen.append((i, j))
        return chessmen

    def execute_ganh(self, position):
        symmetric_points = symmetric_lookup_table[position]
        for p in symmetric_points:
            if get_board_at_tuple(self.board, p[0]) == self.opponent and \
                    get_board_at_tuple(self.board, p[1]) == self.opponent:
                set_board_at_tuple(self.board, p[0], self.player)
                set_board_at_tuple(self.board, p[1], self.player)

    def is_trapped(self, position):
        moves = move_lookup_table[position]
        for m in moves:
            if get_board_at_tuple(self.board, m) == 0:
                return False
        return True

    def execute_vay(self):
        chessmen = self.find_all_chessmen(player=self.opponent)
        trapped_chessmen = []
        untrapped_chessmen = []
        for c in chessmen:
            if self.is_trapped(c):
                trapped_chessmen.append(c)
            else:
                untrapped_chessmen.append(c)
        finished = False

        while finished:
            changed = False
            for c in trapped_chessmen:
                #  get neighbor chessmen
                neighbor_chessmen = move_lookup_table[c]
                for nc in neighbor_chessmen:
                    if get_board_at_tuple(self.board, nc) == self.opponent and nc in untrapped_chessmen:
                        untrapped_chessmen.append(nc)
                        trapped_chessmen.remove(nc)
                        changed = True
                        continue
            if not changed:
                finished = True
        for c in trapped_chessmen:
            set_board_at_tuple(self.board, c, value=self.player)

    def board_after_move(self, my_move):
        x0, y0, x1, y1 = [my_move[0][0], my_move[0][1], my_move[1][0], my_move[1][1]]
        self.board[x0][y0] = 0
        self.board[x1][y1] = self.player

    def update_board(self, my_move):
        if get_board_at_tuple(self.board, my_move[0]) != self.player or \
                get_board_at_tuple(self.board, my_move[1]) != 0:
            print("invalid move")
            return
        self.board_after_move(my_move)
        self.execute_ganh(my_move[1])
        self.execute_vay()


def set_board_at_tuple(board, position_tuple, value):
    x = position_tuple[0]
    y = position_tuple[1]
    board[x][y] = value


def get_board_at_tuple(board, position_tuple):
    x = position_tuple[0]
    y = position_tuple[1]
    return board[x][y]


def move(prev_board, board, player, remain_time_x, remain_time_o):
    result = None
    ai_game = game(prev_board, board, player=ai)
    old_position = ai_game.get_old_position()
    traps = ai_game.check_trap()
    if traps:
        moves = move_lookup_table[old_position]
        for m in moves:
            if get_board_at_tuple(ai_game.board, m) == -1:
                result = (m, old_position)
        if result:
            ai_game.update_board(result)  # update board
            return result

    print('xu ly')

def test():
    prev_board = [
        [1, 1, 1, 1, 1],
        [-1, -1, 1, 1, 1],
        [1, 0, 0, -1, 0],
        [0, 1, 0, 0, -1],
        [1,-1,-1,-1, -1]]

    board = [
        [1, 1, 1, 1, 1],
        [-1, -1, 1, 1, 1],
        [1, 1, 0, -1, 0],
        [0, 0, 0, 0, -1],
        [1,-1,-1,-1, -1]]
    #
    res = move(prev_board, board, None, None, None)
    print(res)

test()