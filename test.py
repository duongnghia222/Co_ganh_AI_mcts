import numpy as np

# prev_board = [
#     [1, 1, 0, 0, 1],
#     [1, 0, 1, 1, 1],
#     [1, 0, 0, -1, 0],
#     [0, 1, 0, 0, -1],
#     [1,-1,-1,-1, -1]]
#
board = [
    [1, 1, 0, 0, 1],
    [1, 1, 0, 1, 1],
    [1, 0, 0, -1, 0],
    [0, 1, 0, 0, -1],
    [1,-1,-1,-1, -1]]
n = 8
m = n//5
print(m)
print(n - m*5)
#
# mask_board = np.subtract(board, prev_board)
# def foo(mask_board):
#     for i in range(5):
#         for j in range(5):
#             if mask_board[i][j] == -1:
#                 return i, j
#
# res = type(foo(mask_board))
# print(res)
# res = np.argwhere(board == 1)
# print (res)
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


# moves = {
#     (0,1): (0,2),
#     (1,1): []
# }
# moves[(0,2, '3ur')] = []
# moves[(0,2, '3ur')].append((1,3))
# print(list(moves)[0])
# for i in list(moves):
#     if not moves[i]:
#         moves.pop(i)
# for i in moves:
#     print(i)
#



# trap = []

# if trap:
#     print(trap)
# root = (0,)
#
# print(type(root))
# root1 = (1,)
# r = root1 + root
# print(r)
# n = 0
# m = n if n != 0 else 1e-4
# print(m)

# x1 = (1,0)
# x2 = (1,1)
# res = np.subtract(x1, x2)
# print(res)

#
# s = '1u'
# direction = s.lstrip('0123456789')
# print(type(direction))
# position = s[:-len(direction)]
# print(type(int(position)))

# x = 0;
# while True:
#     while True:
#         x+=1
#         print(x)
#         if x == 10000:
#             break
