import pygame
import random
import settings_list


class Piece(object):
    def __init__(self, x, y, shape, piece_colour):
        self.x = x
        self.y = y
        self.shape = shape
        self.colour = piece_colour
        self.rotation = 0


def check_lost(piece_pos, positions):
    for pos in piece_pos:
        if pos in positions:
            return True
    return False


def check_win(lines):
    if lines >= 40:
        return True
    return False


def clear_rows(grid, locked_positions, settings):
    inc = 0
    for counter in range(settings.psps.line_clear_labels):
        for i in range(len(grid) - 1, -1, -1):
            row = grid[i]
            # if there no black spaces
            if (0, 0, 0) not in row:
                inc += 1
                for j in range(len(row)):
                    # try:
                    del locked_positions[(j, i)]
                    # except:
                    #    continue
                for key in sorted(list(locked_positions), key=lambda x: x[1])[::-1]:
                    x, y = key
                    # if locked position is above the cleared row then:
                    if y < i:
                        # shift locked positions down
                        new_key = (x, y + 1)
                        locked_positions[new_key] = locked_positions.pop(key)
            # update grid
            grid = create_grid(settings, locked_positions)
    return inc


def convert_piece_orientation(piece):
    positions = []
    orientation = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(orientation):
        # convert the string into row
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))

    for i, pos in enumerate(positions):
        # test this
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def create_grid(settings, locked_positions=None):
    if locked_positions is None:
        locked_positions = {}
    grid = [[(0, 0, 0) for x in range(settings.psps.play_width_cells)]
            for y in range(settings.psps.play_height_cells)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                grid[i][j] = locked_positions[(j, i)]
    return grid


def get_piece(settings):
    random_number = random.choice(range(len(settings.psps.pieces)))
    # print(random_number)
    return Piece(settings.psps.play_width_cells // 2 + settings.psps.piece_offset_x,
                 settings.psps.piece_offset_y,
                 settings.psps.pieces[random_number],
                 settings.psps.piece_colours[random_number])


def valid_space(shape, grid, settings):

    # produce list of coordinates for all positions in the grid for each row if position is empty (i.e. black)
    accepted_pos = [[(j, i) for j in range(settings.psps.play_width_cells) if grid[i][j] == (0, 0, 0)] for i
                    in range(settings.psps.play_height_cells)]

    # return list of coordinates for all positions in the grid
    accepted_pos = [j for sub in accepted_pos for j in sub]

    oriented = convert_piece_orientation(shape)

    for pos in oriented:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


# alter settings


def toggle_fullscreen(settings):
    settings.fullscreen = not settings.fullscreen
    if settings.fullscreen:
        settings.surface = pygame.display.set_mode((settings.surface.get_width(),
                                                    settings.surface.get_height()), pygame.FULLSCREEN)
    else:
        settings.surface = pygame.display.set_mode((settings.surface.get_width(),
                                                    settings.surface.get_height()), pygame.RESIZABLE)


def mute_music(settings):
    if settings.play_music:
        if settings.music_is_playing:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        settings.music_is_playing = not settings.music_is_playing
    else:
        pygame.mixer.music.play(-1)
        settings.play_music = not settings.play_music


def mute_sounds(settings):
    if settings.play_sound_effects:
        settings.sound_effects_volume = 0
    else:
        settings.sound_effects_volume = 0.1

    for sound in settings_list.sounds:
        sound.set_volume(settings.sound_effects_volume)

    settings.play_sound_effects = not settings.play_sound_effects


def update_settings(settings):
    settings.play_width = settings.psps.play_width_cells * settings.cell_size
    settings.play_height = settings.psps.play_height_cells * settings.cell_size
    settings.left_grid_x = (settings.surface.get_width() - settings.play_width) // 2
    settings.right_grid_x = (settings.surface.get_width() + settings.play_width) // 2
    settings.top_grid_y = (settings.surface.get_height() - settings.play_height) // 2
    settings.bottom_grid_y = (settings.surface.get_height() + settings.play_height) // 2


# colour functions

def brighten_colour(colour):
    new_colour = []
    for i in range(3):
        new_colour.append(colour[i] + (int((255 - colour[i]) / 2)))
    return new_colour[0], new_colour[1], new_colour[2]


def darken_colour(colour):
    new_colour = []
    for i in range(3):
        new_colour.append(int(colour[i] * 0.75))
    return new_colour[0], new_colour[1], new_colour[2]


def darken_colour_more(colour):
    new_colour = []
    for i in range(3):
        new_colour.append(int(colour[i] * 0.65))
    return new_colour[0], new_colour[1], new_colour[2]


def prettify_blocks(settings, colour, start_pos_x, start_pos_y):

    cs = settings.cell_size

    for k in (range(1, (cs // 2))):
        # draw horizontal bright lines
        pygame.draw.line(settings.surface, brighten_colour(colour),
                         (start_pos_x + k, start_pos_y + k),
                         (start_pos_x + (cs - 1) - k, start_pos_y + k), 1)

        # draw horizontal dark lines
        pygame.draw.line(settings.surface, darken_colour(colour),
                         (start_pos_x + k, start_pos_y + (cs - 1) - k),
                         (start_pos_x + (cs - 1) - k, start_pos_y + (cs - 1) - k), 1)
    # draw darker squares
    pygame.draw.rect(settings.surface, darken_colour_more(colour),
                     (start_pos_x, start_pos_y, cs, cs), 2)


# draw functions

def draw_grid(settings):
    sx = settings.left_grid_x
    sy = settings.top_grid_y
    grid_line_colour = (32, 32, 32)

    # draw horizontal lines across grid. x is fixed, y needs to change
    for i in range(1, settings.psps.play_height_cells + 1):
        pygame.draw.line(settings.surface, grid_line_colour, (sx, sy + i * settings.cell_size),
                         (sx + settings.play_width, sy + i * settings.cell_size), 3)
    # draw vertical lines across grid. y is fixed, x needs to change
    for j in range(settings.psps.play_width_cells + 1):
        pygame.draw.line(settings.surface, grid_line_colour, (sx + j * settings.cell_size, sy + settings.cell_size),
                         (sx + j * settings.cell_size, sy + settings.play_height), 3)


def draw_labels(settings, score, high_score, level, lines, single, double, triple, quad, pentris, elapsed_time):

    cs = settings.cell_size
    lgx = settings.left_grid_x
    rgx = settings.right_grid_x
    tgy = settings.top_grid_y
    sw = settings.surface.get_width()
    sh = settings.surface.get_height()

    pygame.font.init()

    font = pygame.font.Font(settings.text_font, 35)

    # level
    label1 = font.render('Level', 1, (240, 240, 180))
    label2 = font.render(str(level), 1, (255, 255, 255))
    settings.surface.blit(label1, (rgx + 20, (sh // 2) + (cs * 3)))
    settings.surface.blit(label2, (rgx + 205 - label2.get_width(), (sh // 2) + (cs * 3)))

    if settings.mode != '40 Lines':
        # high score
        label1 = font.render('High Score', 1, (210, 230, 150))
        label2 = font.render(str(high_score), 1, (255, 255, 255))
        settings.surface.blit(label1, (rgx + 20, tgy))
        settings.surface.blit(label2, (rgx + 205 - label2.get_width(), tgy + 40))

        # current score
        label1 = font.render('Score', 1, (210, 210, 150))
        label2 = font.render(str(score), 1, (255, 255, 255))
        settings.surface.blit(label1, (rgx + 20, tgy + 80))
        settings.surface.blit(label2, (rgx + 205 - label2.get_width(), tgy + 120))

    if settings.mode == '40 Lines':
        # high score
        label1 = font.render('Best Time', 1, (210, 230, 150))
        label2 = font.render(str(high_score), 1, (255, 255, 255))
        settings.surface.blit(label1, (rgx + 20, tgy))
        settings.surface.blit(label2, (rgx + 205 - label2.get_width(), tgy + 40))

        # Time
        label1 = font.render('Time', 1, (192, 192, 192))
        if elapsed_time % 60 < 10:
            label2 = font.render(str(int(elapsed_time // 60)) + ":0" + str("{:.2f}".format(elapsed_time % 60)),
                                 1, (255, 255, 255))
        else:
            label2 = font.render(str(int(elapsed_time // 60)) + ":" + str("{:.2f}".format(elapsed_time % 60)),
                                 1, (255, 255, 255))
        settings.surface.blit(label1, (rgx + 20, tgy + 80))
        settings.surface.blit(label2, (rgx + 205 - label2.get_width(), tgy + 120))

    # Lines
    label1 = font.render('Lines ', 1, (210, 255, 150))
    settings.surface.blit(label1, (((sw // 2) - int(label1.get_width())) + 10, tgy - 35))
    label2 = font.render(' ' + str(lines), 1, (255, 255, 255))
    settings.surface.blit(label2, (((sw // 2) + int(label1.get_width()) - int(label2.get_width())) - 10, tgy - 35))

    # Line clear counters
    hexis = 0

    labels = ["Hexis", "Pentris", "Quad", "Triple", "Double", "Single"]
    counters = [hexis, pentris, quad, triple, double, single]
    text_colours = [(255, 215, 0), (255, 128, 0), (128, 64, 255), (0, 128, 255), (0, 255, 0), (64, 64, 64)]

    for i in range(settings.psps.line_clear_labels):
        label1 = font.render(labels[i + (6 - settings.psps.line_clear_labels)], 1, text_colours[i])
        label2 = font.render(str(counters[i + (6 - settings.psps.line_clear_labels)]), 1, (255, 255, 255))
        settings.surface.blit(label1, (lgx - 160, tgy + (70 * i)))
        settings.surface.blit(label2, (lgx - (label2.get_width() + 30), tgy + 35 + (70 * i)))


def draw_next_piece(piece, settings):
    font = pygame.font.Font(settings.text_font, 35)
    rgx = settings.right_grid_x
    cs = settings.cell_size
    centre_y = (settings.surface.get_height() // 2)

    # For clear pieces
    if settings.piece_style == "Normal":
        colour = piece.colour
    elif settings.piece_style == "Clear":
        colour = (255, 255, 255)

    offset_x = 110
    offset_y = 0

    orientation = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(orientation):
        row = list(line)

        for j, column in enumerate(row):
            # declare the starting coordinates of the pieces
            square_origin_x = (rgx + offset_x + (j * cs)) - ((len(piece.shape[0]) * cs) // 2)
            square_origin_y = (centre_y + offset_y + (i * cs)) - ((len(piece.shape[0]) * cs) // 2)

            if column == '0':
                if settings.piece_style == "Normal":
                    pygame.draw.rect(settings.surface, colour,
                                     (square_origin_x, square_origin_y, cs, cs), 0)

                    prettify_blocks(settings, piece.colour, square_origin_x, square_origin_y)

                else:
                    pygame.draw.rect(settings.surface, colour,
                                     (square_origin_x, square_origin_y, cs, cs), 2)

    label = font.render('Next Piece', 1, (240, 210, 150))
    settings.surface.blit(label, (rgx + 20, centre_y - (settings.cell_size * 3)))


def draw_text_middle(settings, text, font_name, size, colour, offset):
    label = font_name.render(text, size, colour)

    settings.surface.blit(label, (((int(settings.surface.get_width() / 2) - int(label.get_width() / 2)) + offset[0],
                                   (int(settings.surface.get_height() / 2) - int(label.get_height() / 2)) + offset[1])))


def draw_window(settings, grid, ghost_piece, ghost_piece_pos, oll_centre_pos,
                score, high_score, level, lines,
                single, double, triple, quad, pentris, elapsed_time):
    # settings.surface.fill((0, 50, 60))
    cs = settings.cell_size
    lgx = settings.left_grid_x
    rgx = settings.right_grid_x
    tgy = settings.top_grid_y
    bgy = settings.bottom_grid_y
    sw = settings.surface.get_width()
    sh = settings.surface.get_height()

    # Play_area colours
    if settings.mode != 'Invisible':
        for i in range(1, len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == (0, 0, 0):
                    pygame.draw.rect(settings.surface, grid[i][j],
                                     ((lgx + j * cs), (tgy + i * cs), cs, cs), 0)

    if settings.mode == 'Invisible':
        for i in range(1, len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(settings.surface, (0, 0, 0),
                                 ((lgx + j * cs), (tgy + i * cs), cs, cs), 0)

    settings.surface.blit(settings.background, (sw // 2 - (settings.background.get_width() // 2),
                                                sh // 2 - (settings.background.get_height() // 2)))

    # draw labels
    draw_labels(settings, score, high_score, level, lines, single, double, triple, quad, pentris, elapsed_time)

    # Play_area colours
    if settings.mode != 'Invisible':
        for i in range(1, len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == (0, 0, 0):
                    pygame.draw.rect(settings.surface, grid[i][j],
                                     ((lgx + j * cs), (tgy + i * cs), cs, cs), 0)

    if settings.mode == 'Invisible':
        for i in range(1, len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(settings.surface, (0, 0, 0),
                                 ((lgx + j * cs), (tgy + i * cs), cs, cs), 0)

    # Grid Lines
    draw_grid(settings)

    # Ghost piece

    if settings.piece_style == "Normal":
        colour = ghost_piece.colour
    elif settings.piece_style == "Clear":
        colour = (255, 255, 255)

    for i, j in ghost_piece_pos:
        if j > 0:
            pygame.draw.rect(settings.surface, colour,
                             ((lgx + i * cs) + 1, (tgy + j * cs) + 1, cs - 2, cs - 2), 1)

    # OLL grid
    if settings.mode != 'Invisible':
        if settings.piece_style == "Normal":

            # OLL centre
            if settings.piece_set_choice == "OLL":
                for i, j in oll_centre_pos:
                    if 0 <= i < settings.psps.play_width_cells and 0 < j < settings.psps.play_height_cells:
                        pygame.draw.rect(settings.surface, (128, 128, 128),
                                         ((lgx + i * cs) + 1, (tgy + j * cs) + 1, cs - 2, cs - 2), 1)

            # all other colours
            for i in range(1, len(grid)):
                for j in range(len(grid[i])):
                    if grid[i][j] != (0, 0, 0):
                        pygame.draw.rect(settings.surface, grid[i][j],
                                         ((lgx + j * cs) + 1, (tgy + i * cs) + 1, cs - 2, cs - 2), 0)

                        # make blocks look pretty
                        prettify_blocks(settings, grid[i][j], lgx + j * cs, tgy + i * cs)

    # play area border
    pygame.draw.rect(settings.surface, (255, 120, 120), (
        lgx - 4, tgy + cs - 4,
        settings.play_width + 7,
        settings.play_height + 7 - cs),
                     6)


# score functions


def max_score(settings):
    f = open('high_scores.txt', 'r')
    lines = f.readlines()
    if settings.mode == 'Classic':
        high_score = lines[settings_list.available_piece_sets.index(settings.piece_set_choice)].strip()
    if settings.mode == '40 Lines':
        high_score = lines[settings_list.available_piece_sets.index(settings.piece_set_choice)+4].strip()
    if settings.mode == 'Invisible':
        high_score = lines[settings_list.available_piece_sets.index(settings.piece_set_choice)+8].strip()
    f.close()
    return high_score


def update_scores(settings, new_score):
    high_score = max_score(settings)
    # open scores txt read mode
    f = open('high_scores.txt', 'r')
    lines = f.readlines()

    # open score txt write mode

    if settings.mode != '40 Lines':
        if new_score > int(high_score):
            f = open('high_scores.txt', 'w')
            if settings.mode == 'Classic':
                lines[settings_list.available_piece_sets.index(settings.piece_set_choice)] = str(new_score) + "\n"
            if settings.mode == 'Invisible':
                lines[settings_list.available_piece_sets.index(settings.piece_set_choice)+8] = str(new_score) + "\n"
            f.writelines(lines)

    if settings.mode == '40 Lines':
        minutes = int(high_score[0]) * 60
        seconds = float(high_score[2:])
        best_time = minutes + seconds
        if new_score < best_time:
            f = open('high_scores.txt', 'w')
            if new_score % 60 < 10:
                elapsed_time = str(int(new_score // 60)) + ":0" + str("{:.2f}".format(new_score % 60))
            else:
                elapsed_time = str(int(new_score // 60)) + ":" + str("{:.2f}".format(new_score % 60))
            lines[settings_list.available_piece_sets.index(settings.piece_set_choice) + 4] = str(elapsed_time) + "\n"
            f.writelines(lines)
    f.close()


def reset_high_scores():
    f = open('high_scores.txt', 'w')
    f.write("0\n0\n0\n0\n9:59.99\n9:59.99\n9:59.99\n9:59.99\n0\n0\n0\n0")
    f.close()
