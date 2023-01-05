import numpy as np
import time

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
    (0, 2): [(0, 1), (0, 3), (1, 2), (1, 1), (1, 3)],
    (0, 3): [(0, 2), (0, 4), (1, 3)],
    (1, 0): [(0, 0), (2, 0), (1, 1)],
    (2, 0): [(1, 0), (3, 0), (2, 1), (1, 1), (3, 1)],
    (3, 0): [(2, 0), (4, 0), (3, 1)],
    (4, 1): [(4, 0), (4, 2), (3, 1)],
    (4, 2): [(4, 1), (4, 3), (3, 2), (3, 3), (3, 1)],
    (4, 3): [(4, 2), (4, 4), (3, 3)],
    (3, 4): [(2, 4), (4, 4), (3, 3)],
    (2, 4): [(1, 4), (3, 4), (2, 3), (3, 3), (1, 3)],
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
        self.prev_board = [x[:] for x in prev_board] if prev_board is not None else None  # copy
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

    def check_win(self):
        win_player = None
        if self.number_of_chessmen(ai) == 0 and \
                self.number_of_chessmen(human) == 16:
            win_player = human
        if self.number_of_chessmen(ai) == 16 and \
                self.number_of_chessmen(human) == 0:
            win_player = ai
        return win_player

    def get_all_possible_moves(self, player):
        possible_moves = dict()
        traps = self.check_trap()
        if traps:
            old_position = self.get_old_position()
            moves = move_lookup_table[old_position]
            for m in moves:
                if get_board_at_tuple(self.board, m) == self.player:
                    possible_moves[m] = [old_position]
                    return possible_moves
        chessmen = self.find_all_chessmen(player)
        for c in chessmen:
            all_position = move_lookup_table[c]
            possible_moves[c] = []
            for position in all_position:
                if get_board_at_tuple(self.board, position) == 0:
                    possible_moves[c].append(position)
        # clean the dict
        for i in list(possible_moves):
            if not possible_moves[i]:
                possible_moves.pop(i)
        return possible_moves

    def number_of_chessmen(self, player):
        chessmen = self.find_all_chessmen(player)
        return len(chessmen)


class MCTS:
    def __init__(self, iterations=100, c=2.0, tree=None, prev_board=None, board=None, player=None):
        self.iterations = iterations
        self.c = c
        self.game = game(prev_board, board, player)
        self.total_n = 0
        if tree is None:
            self.tree = self.set_tree()
        else:
            self.tree = tree

    def set_tree(self):
        root_id = (0,)
        tree = {root_id: {'game': self.game,
                          'children': [],
                          'parent': None,
                          'n': 0,
                          'w': 0,
                          'ucb': None}}
        return tree

    def ucb_value(self, w, n):
        exploitation_value = w / n
        exploration_value = np.sqrt(np.log(self.total_n) / n)
        ucb_value = exploitation_value + self.c * exploration_value
        print("explore:", exploration_value, ' w  ', w, '  n ', n)
        print('exploi: ', exploitation_value, 'total_n', self.total_n)
        print('ucb', ucb_value)
        return ucb_value

    def selection(self):
        leaf_id = (0,)
        while True:
            node_id = leaf_id
            no_of_children = len(self.tree[node_id]['children'])
            if no_of_children:
                max_ucb = -9999
                for i in range(no_of_children):
                    action = self.tree[node_id]['children'][i]
                    child_id = node_id + (action,)
                    w = self.tree[child_id]['w']
                    n = self.tree[child_id]['n']
                    if n == 0:
                        return child_id
                    ucb_value = self.ucb_value(w, n)
                    if ucb_value > max_ucb:
                        max_ucb = ucb_value
                        leaf_id = child_id
            else:
                leaf_id = node_id
                break
        return leaf_id

    def expansion(self, leaf_id):
        current_game = self.tree[leaf_id]['game']
        winner = current_game.check_win()
        player = current_game.player
        possible_moves = current_game.get_all_possible_moves(player)
        child_node_id = leaf_id
        if not winner:
            children = []
            for position in possible_moves:
                to_position = possible_moves[position]
                for d in to_position:
                    temp_game = game(current_game.prev_board, current_game.board, player)
                    temp_game.update_board((position, d))
                    gen_id = id_generator_from_move(position, d)
                    child_id = leaf_id + (gen_id,)
                    children.append(child_id)
                    child = game(current_game.board, temp_game.board, -1*player)
                    self.tree[child_id] = {
                        'game': child,
                        'children': [],
                        'parent': leaf_id,
                        'n': 0, 'w': 0, 'ucb': 0
                    }
                    self.tree[leaf_id]['children'].append(gen_id)
            rand_idx = np.random.randint(low=0, high=len(children), size=1)
            child_node_id = children[rand_idx[0]]
        return child_node_id

    def simulation(self, child_node_id):
        self.total_n += 1
        current_game = self.tree[child_node_id]['game']
        move_threshold = 50
        prev_board = current_game.prev_board
        board = current_game.board
        player = current_game.player
        simulation_game = game(prev_board, board, player)
        while not simulation_game.check_win():
            if move_threshold < 0:
                break
            possible_moves = simulation_game.get_all_possible_moves(simulation_game.player)
            found_ganh_move = False
            for position in possible_moves:
                to_position = possible_moves[position]
                for d in to_position:
                    ganh_position = symmetric_lookup_table[d]
                    for gp in ganh_position:
                        if get_board_at_tuple(simulation_game.board, gp[0]) == -1*simulation_game.player and \
                                get_board_at_tuple(simulation_game.board, gp[1]) == -1 * simulation_game.player:
                            my_move = (position, d)
                            found_ganh_move = True
            if not found_ganh_move:
                # get random move
                rand_idx = np.random.randint(low=0, high=len(possible_moves), size=1)[0]
                from_position = list(possible_moves)[rand_idx]
                rand_idx = np.random.randint(low=0, high=len(possible_moves[from_position]), size=1)[0]
                to_position = possible_moves[from_position][rand_idx]
                my_move = (from_position, to_position)
            temp_board = [x[:] for x in simulation_game.board]
            simulation_game.update_board(my_move)
            simulation_game.prev_board = temp_board
            simulation_game.player *= -1
            move_threshold -= 1
        if simulation_game.check_win() == current_game.player:
            return 1
        else:
            return 0
        # return simulation_game.number_of_chessmen(player)*0.0625 + move_threshold*0.01

    def backpropagation(self, child_node_id, value):
        node_id = child_node_id
        while True:
            self.tree[node_id]['n'] += 1
            self.tree[node_id]['w'] += value
            self.tree[node_id]['ucb'] = self.tree[node_id]['w'] / self.tree[node_id]['n']
            parent_id = self.tree[node_id]['parent']
            if parent_id == (0, ):
                self.tree[parent_id]['n'] += 1
                self.tree[parent_id]['w'] += value
                self.tree[parent_id]['ucb'] = self.tree[parent_id]['w'] / self.tree[parent_id]['n']
                break
            else:
                node_id = parent_id

    def solver(self):
        for i in range(self.iterations):
            print('---- new iteration -------')
            leaf_id = self.selection()
            child_node_id = self.expansion(leaf_id)
            value = self.simulation(child_node_id)
            self.backpropagation(child_node_id, value)
        nodes = self.tree[(0, )]['children']
        max_ucb = -999
        for n in nodes:
            ucb = self.tree[(0, ) + (n, )]['ucb']
            print('----node ucb:', ucb)
            if ucb > max_ucb:
                max_ucb = ucb
                best_node = n
        print("best: ", self.tree[(0, ) + (best_node,)]['ucb'])
        return get_move_from_gen_id(best_node)


def get_move_from_gen_id(gen_id):
    direction = gen_id.lstrip('0123456789')
    position = int(gen_id[:-len(direction)])
    x = position//5
    y = position - x*5
    from_position = (x, y)
    to_position = None
    if direction == 'ul':
        to_position = (x - 1, y - 1)
    elif direction == 'u':
        to_position = (x - 1, y)
    elif direction == 'ur':
        to_position = (x - 1, y + 1)
    elif direction == 'r':
        to_position = (x, y + 1)
    elif direction == 'dr':
        to_position = (x + 1, y + 1)
    elif direction == 'd':
        to_position = (x + 1, y)
    elif direction == 'dl':
        to_position = (x + 1, y - 1)
    elif direction == 'l':
        to_position = (x, y - 1)
    return from_position, to_position


def id_generator_from_move(key, value):
    from_position = key
    to_position = value
    board_index = from_position[0]*5 + from_position[1]
    res = (from_position[0] - to_position[0], from_position[1] - to_position[1])
    direction = ''
    if res == (1, 1):
        direction = 'ul'
    elif res == (1, 0):
        direction = 'u'
    elif res == (1, -1):
        direction = 'ur'
    elif res == (0, -1):
        direction = 'r'
    elif res == (-1, -1):
        direction = 'dr'
    elif res == (-1, 0):
        direction = 'd'
    elif res == (-1, 1):
        direction = 'dl'
    elif res == (0, 1):
        direction = 'l'
    gen_id = str(board_index) + direction
    return gen_id


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
            if get_board_at_tuple(ai_game.board, m) == ai:
                result = (m, old_position)
        if result:
            ai_game.update_board(result)  # update board
            return result

    solver = MCTS(iterations=1000, c=2.0, tree=None, prev_board=prev_board, board=ai_game.board, player=ai)
    return solver.solver()


def test():
    prev_board = [
        [1, 0, 0, 0, -1],
        [0, 0, 0, 0, 1],
        [-1, -1, 1, 0, 0],
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1]]

    board = [
        [1, 0, 0, 0, -1],
        [0, 0, 0, 1, 0],
        [-1, -1, 1, 0, 0],
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1]]
    #
    res = move(prev_board, board, None, None, None)
    print(res)


test()
