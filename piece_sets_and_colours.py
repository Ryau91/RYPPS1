import random


class PieceSetPlaySettings(object):
    def __init__(self, pieces, piece_colours, piece_offset_x, piece_offset_y,
                 play_width_cells, play_height_cells, line_clear_labels):
        self.pieces = pieces
        self.piece_colours = piece_colours
        self.piece_offset_x = piece_offset_x
        self.piece_offset_y = piece_offset_y
        self.play_width_cells = play_width_cells
        self.play_height_cells = play_height_cells
        self.line_clear_labels = line_clear_labels


def random_colour():
    return random.choice(range(64, 256)), random.choice(range(64, 224)), random.choice(range(64, 256))


def piece_orientation_definer(piece):
    # do stuff 3 times max to find all possible orientations
    for i in range(3):

        listed_piece = []
        candidate_orientation = []

        # turn strings into lists
        for row in piece[i]:
            listed_piece.append(list(row))

        # rotate lists WHAT IS ASTERISK THING? HOW DOES IT WORK? FIND OUT
        rot_listed_piece = list(zip(*listed_piece[::-1]))

        # revert lists into strings
        for row in rot_listed_piece:
            candidate_orientation.append("".join(row))

        # if candO is new, add it to piece (i.e. the list of possible orientations for the piece)
        if piece[0] != candidate_orientation:
            piece.append(candidate_orientation)
        else:
            return piece
    return piece


# PIECE###

# Regular

reg_S = [['.....',
          '.....',
          '..00.',
          '.00..',
          '.....']]

reg_Z = [['.....',
          '.....',
          '.00..',
          '..00.',
          '.....']]

reg_I = [['.....',
          '.....',
          '0000.',
          '.....',
          '.....']]

reg_O = [['.....',
          '.....',
          '.00..',
          '.00..',
          '.....']]

reg_L = [['.....',
          '.....',
          '.000.',
          '.0...',
          '.....']]

reg_J = [['.....',
          '.....',
          '.000.',
          '...0.',
          '.....']]

reg_T = [['.....',
          '.....',
          '.000.',
          '..0..',
          '.....']]

regular_piece_set = [reg_S, reg_Z, reg_I, reg_O, reg_L, reg_J, reg_T]

for i in range(len(regular_piece_set)):
    regular_piece_copy = regular_piece_set[i].copy()
    regular_piece_set[i] = piece_orientation_definer(regular_piece_copy)

regular_colours = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 240, 0), (255, 128, 0), (0, 0, 255), (160, 0, 160)]

regular_psps = PieceSetPlaySettings(regular_piece_set,
                                    regular_colours,
                                    0, 3, 10, 21, 4)

# Pentominoes

pent_F = [['.....',
           '.0...',
           '.000.',
           '..0..',
           '.....']]

pent_mF = [['.....',
            '...0.',
            '.000.',
            '..0..',
            '.....']]

pent_I = [['.....',
           '.....',
           '00000',
           '.....',
           '.....']]

pent_leftbolt = [['.....',
                  '.....',
                  '000..',
                  '..00.',
                  '.....']]

pent_rightbolt = [['.....',
                   '.....',
                   '..000',
                   '.00..',
                   '.....']]

pent_J = [['.....',
           '.....',
           '0000.',
           '...0.',
           '.....']]

pent_L = [['.....',
           '.....',
           '.0000',
           '.0...',
           '.....']]

pent_P = [['.....',
           '.....',
           '.000.',
           '..00.',
           '.....']]

pent_Q = [['.....',
           '.....',
           '.000.',
           '.00..',
           '.....']]

pent_T = [['.....',
           '.000.',
           '..0..',
           '..0..',
           '.....']]

pent_U = [['.....',
           '.....',
           '.000.',
           '.0.0.',
           '.....']]

pent_V = [['.....',
           '.....',
           '000..',
           '..0..',
           '..0..']]

pent_W = [['.....',
           '.0...',
           '.00..',
           '..00.',
           '.....']]

pent_X = [['.....',
           '..0..',
           '.000.',
           '..0..',
           '.....']]

pent_Y = [['.....',
           '.....',
           '.0000',
           '..0..',
           '.....']]

pent_mY = [['.....',
            '.....',
            '0000.',
            '..0..',
            '.....']]

pent_Z = [['.....',
           '.00..',
           '..0..',
           '..00.',
           '.....']]

pent_S = [['.....',
           '..00.',
           '..0..',
           '.00..',
           '.....']]

pentomino_piece_set = [pent_F, pent_mF, pent_I, pent_J, pent_L, pent_leftbolt,
                       pent_rightbolt, pent_P, pent_Q, pent_T, pent_U, pent_V,
                       pent_W, pent_X, pent_Y, pent_mY, pent_Z, pent_S]

# pentomino_piece_set = [pent_I] ### for debugging

for i in range(len(pentomino_piece_set)):
    pentomino_piece_copy = pentomino_piece_set[i].copy()
    pentomino_piece_set[i] = piece_orientation_definer(pentomino_piece_copy)

pentomino_colours = [(224, 224, 224), (255, 0, 0), (96, 255, 96), (0, 128, 255), (255, 128, 0), (255, 240, 0),
                     (0, 255, 255), (144, 0, 208), (96, 96, 96), (255, 0, 255), (96, 144, 224), (255, 160, 128),
                     (160, 255, 48), (240, 128, 240), (192, 128, 16), (64, 64, 144), (192, 144, 144), (48, 160, 48)]

pentris_psps = PieceSetPlaySettings(pentomino_piece_set,
                                    pentomino_colours,
                                    0, 3, 12, 21, 5)

# pentris_psps = PieceSetPlaySettings(pentomino_piece_set, pentomino_colours, 0, 3, 5, 21, 5) ### for debugging

# OLL

Sune = [['.0.',
         '000',
         '00.']]

Cross = [['.0.',
          '000',
          '.0.']]

TU = [['.0.',
       '000',
       '000']]

Bowtie = [['.00',
           '000',
           '00.']]

Dot = [['...',
        '.0.',
        '...']]

DotDot = [['..0',
           '.0.',
           '...']]

Slash = [['..0',
          '.0.',
          '0..']]

Mickey = [['0.0',
           '.0.',
           '...']]

P = [['00.',
      '00.',
      '0..']]

Q = [['.00',
      '.00',
      '..0']]

W = [['0..',
      '00.',
      '.00']]

TinyL = [['.0.',
          '.00',
          '...']]

C = [['.00',
      '.0.',
      '.00']]

T = [['000',
      '.0.',
      '.0.']]

OLL_I = [['.0.',
          '.0.',
          '.0.']]

Square = [['...',
           '.00',
           '.00']]

BigZ = [['..0',
         '000',
         '0..']]

BigS = [['0..',
         '000',
         '..0']]

Z = [['..0',
      '.00',
      '.0.']]

S = [['.0.',
      '.00',
      '..0']]

Y = [['.0.',
      '.00',
      '0..']]

Ray = [['0..',
        '.00',
        '.00']]

L = [['...',
      '000',
      '0..']]

J = [['...',
      '000',
      '..0']]

AwkwardS = [['0.0',
             '00.',
             '.0.']]

AwkwardZ = [['0.0',
             '.00',
             '.0.']]

Arrow = [['000',
          '00.',
          '0.0']]

H = [['0.0',
      '000',
      '0.0']]

OLL_X = [['0.0',
          '.0.',
          '0.0']]

OLL_O = [['000',
          '000',
          '000']]

twenty_four_times = [TinyL]
twelve_times = [OLL_I]
eight_times = [Sune, TU, DotDot, Mickey, P, Q, W, C, T, Square, Z, S, Y, Ray, L, J, AwkwardS, AwkwardZ]
six_times = [Cross, Dot]
four_times = [Bowtie, Slash, BigZ, BigS, Arrow]
twice = [H]
once = [OLL_X, OLL_O]

OLL_piece_set = []

OLL_subsets = [(twenty_four_times, 24),
               (twelve_times, 12),
               (eight_times, 8),
               (six_times, 6),
               (four_times, 4),
               (twice, 2),
               (once, 1)]

for x in OLL_subsets:
    for i in x[0]:
        for j in range(int(x[1])):
            OLL_piece_set.append(i)

for i in range(len(OLL_piece_set)):
    OLL_piece_copy = OLL_piece_set[i].copy()
    OLL_piece_set[i] = piece_orientation_definer(OLL_piece_copy)

OLL_colours = [random_colour() for j in range(len(OLL_piece_set))]

oll_psps = PieceSetPlaySettings(OLL_piece_set,
                                OLL_colours, 1, 4, 15, 21, 3)


def zorp1():
    return random.choice(["0", "0", "."])


def zorp2():
    return random.choice(["0", ".", "."])


def zorp3():
    return random.choice(["0", ".", ".", "."])


def four_three_madness_piece():
    # initialize piece_mould
    piece_mould = [['.', '0', '0', '.'], ['.', '.', '.', '.'], ['.', '.', '.', '.']]
    piece = ['....']

    # layer 1
    step1 = [(0, 0), (1, 1), (1, 2), (0, 3)]

    for cell in step1:
        piece_mould[cell[0]][cell[1]] = zorp1()

    # layer 2
    if piece_mould[1][1] == '0':
        piece_mould[1][0] = zorp2()
    else:
        if piece_mould[0][0] == '0':
            piece_mould[1][0] = zorp3()

    if piece_mould[1][2] == '0':
        piece_mould[1][3] = zorp2()
    else:
        if piece_mould[0][3] == '0':
            piece_mould[1][3] = zorp3()

    if piece_mould[1][1] == '0':
        piece_mould[2][1] = zorp2()

    if piece_mould[1][2] == '0':
        piece_mould[2][2] = zorp2()

    # layer 3 (far corners)
    if piece_mould[1][0] == '0' or piece_mould[2][1] == '0':
        piece_mould[2][0] = zorp3()

    if piece_mould[1][3] == '0' or piece_mould[2][2] == '0':
        piece_mould[2][3] = zorp3()

    # hooks

    # outer hook 1
    if piece_mould[1] == ['0', '.', '.', '.']:
        if piece_mould[2][0] == '0':
            piece_mould[2][1] = zorp2()
            if piece_mould[2][1] == '0':
                piece_mould[2][2] = zorp2()
                if piece_mould[2][2] == '0':
                    piece_mould[2][3] = zorp2()

    # outer hook 2
    if piece_mould[1] == ['.', '.', '.', '0']:
        if piece_mould[2][3] == '0':
            piece_mould[2][2] = zorp2()
            if piece_mould[2][2] == '0':
                piece_mould[2][1] = zorp2()
                if piece_mould[2][1] == '0':
                    piece_mould[2][0] = zorp2()

    # inner hooks 1
    if piece_mould[1] == ['.', '0', '.', '.']:
        if piece_mould[2][1] == '0':
            piece_mould[2][0] = zorp2()
            piece_mould[2][2] = zorp2()
            if piece_mould[2][2] == '0':
                piece_mould[2][3] = zorp2()

    # inner hooks 2
    if piece_mould[1] == ['.', '.', '0', '.']:
        if piece_mould[2][2] == '0':
            piece_mould[2][3] = zorp2()
            piece_mould[2][1] = zorp2()
            if piece_mould[2][1] == '0':
                piece_mould[2][0] = zorp2()

    # convert to strings
    for row in piece_mould:
        piece.append("".join(row))

    piece = [piece]

    return piece


wacky_piece_set = [four_three_madness_piece() for i in range(667)]

one_by_two = [['....', '.00.', '....', '....']]
one_by_three = [['....', '.000', '....', '....']]
one_by_four = [['....', '0000', '....', '....']]
two_by_two = [['....', '.00.', '.00.', '....']]
little_l = [['....', '.00.', '..0.', '....']]
basic_J = [['....', '000.', '..0.', '....']]
basic_L = [['....', '.000', '.0..', '....']]
basic_T = [['....', '.000', '..0.', '....']]
basic_S = [['....', '.00.', '00..', '....']]
basic_Z = [['....', '.00.', '..00', '....']]

four_by_four = [['0000', '0000', '0000', '0000']]
four_by_four_holo_square = [['0000', '0..0', '0..0', '0000']]
four_by_four_swasty = [['00.0', '.000', '000.', '00.0']]

wacky_piece_set_nice = [one_by_two,
                        one_by_three,
                        one_by_four,
                        two_by_two,
                        little_l,
                        basic_J,
                        basic_L,
                        basic_T,
                        basic_S,
                        basic_Z]

for i in range(33):
    for nice_piece in wacky_piece_set_nice:
        wacky_piece_set.append(nice_piece)

# Add the three bonus pieces
wacky_piece_set.append(four_by_four)
wacky_piece_set.append(four_by_four_holo_square)
wacky_piece_set.append(four_by_four_swasty)

for i in range(len(wacky_piece_set)):
    wacky_piece_copy = wacky_piece_set[i].copy()
    wacky_piece_set[i] = piece_orientation_definer(wacky_piece_copy)

four_three_madness_colours = [random_colour() for i in range(len(wacky_piece_set))]

wacky_psps = PieceSetPlaySettings(wacky_piece_set,
                                  four_three_madness_colours,
                                  0, 4, 20, 21, 4)
