# to do
# pathlib thing
# All Mollerz stuff
# new record message:
# 40 lines: when game over: game over music, game over
# when win: victory music, if new record new record!, else complete!
# not 40 lines: when game over:
# if new record: victory music, new record!, else game over music, game over
# add feature for custom music
# lock delay ?
# halved music volume

import pygame
import sys
import copy
import random
import controls as cont
import functions as fun
import piece_sets_and_colours as psac
import settings_list as sl
import time


def main(settings, level, fall_speed, first_advance_lines):

    # music
    settings.music = random.choice(sl.music)
    song_end = pygame.USEREVENT + 1
    pygame.mixer.music.set_endevent(song_end)

    if settings.play_music:
        pygame.mixer.music.load(settings.music)
        pygame.mixer.music.play()
        settings.music_is_playing = True
    locked_positions = {}

    # choose random background
    settings.background = random.choice(sl.backgrounds)

    # prepare pieces and play_area

    change_piece = False
    change_piece_counter = 0
    run = True
    current_piece = fun.get_piece(settings)
    next_piece = fun.get_piece(settings)

    move_piece_x = 0
    move_piece_y = 0
    move_counter_x = 0
    move_counter_y = 0

    fall_time = 0
    level_meter = 0
    lines = 0
    score = 0
    single = 0
    double = 0
    triple = 0
    quad = 0
    pentris = 0
    hexis = 0
    drop_points = 0
    cleared_rows_count = 0

    clock = pygame.time.Clock()
    start_the_time = True
    first_advance_lines_reached = False

    while run:

        if start_the_time:
            start_time = time.time()
            start_the_time = False

        grid = fun.create_grid(settings, locked_positions)

        # ghost_grid = grid.copy()
        ghost_piece = copy.deepcopy(current_piece)

        # generate oll centre
        oll_centre = copy.deepcopy(current_piece)
        oll_centre.shape = psac.OLL_O

        clock.tick(sl.fps)
        fall_time += 1

        if (lines >= first_advance_lines) & (level_meter >= 10):
            sl.levelup_sound.play()
            if level < 8:
                fall_speed -= 5
            elif level == 8:
                fall_speed -= 2
            elif level in [9, 12, 15, 18, 28]:
                fall_speed -= 1

            settings.background = random.choice(sl.backgrounds)

            level += 1

            # only subtract first_advance_lines away once
            if first_advance_lines_reached:
                level_meter -= 10
            else:
                level_meter -= first_advance_lines
                first_advance_lines_reached = True

        # drop piece by 1
        if fall_time >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (fun.valid_space(current_piece, grid, settings)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece_counter += 1
            if change_piece_counter == 1:
                change_piece = True
                change_piece_counter = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                if not settings.fullscreen:
                    settings.surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                fun.update_settings(settings)

            # song ended, pick a random new song and play it
            if event.type == song_end:
                settings.music = random.choice(sl.music)
                pygame.mixer.music.load(settings.music)
                pygame.mixer.music.play()

            if event.type == pygame.KEYDOWN:
                # Quit
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    sl.cancel_sound.play()
                    settings.background = sl.initial_background
                    run = False
                if event.key == pygame.K_F11:
                    fun.toggle_fullscreen(settings)
                    fun.update_settings(settings)

                if event.key == cont.start:
                    sl.pause_sound.play()
                    pause_menu(settings)
                if event.key == pygame.K_m:
                    fun.mute_music(settings)

                # Move left
                if event.key == cont.move_left:
                    current_piece.x -= 1
                    if not (fun.valid_space(current_piece, grid, settings)):
                        current_piece.x += 1
                    move_piece_x = -1
                    move_counter_x = 0

                # Move right
                if event.key == cont.move_right:
                    current_piece.x += 1
                    if not (fun.valid_space(current_piece, grid, settings)):
                        current_piece.x -= 1
                    move_piece_x = 1
                    move_counter_x = 0

                # soft drop
                if event.key == cont.soft_drop:
                    current_piece.y += 1
                    if not (fun.valid_space(current_piece, grid, settings)):
                        current_piece.y -= 1
                    move_piece_y = 1
                    move_counter_y = 0

                # hard drop
                if event.key == cont.hard_drop:
                    sl.harddrop_sound.play()
                    while not change_piece:
                        current_piece.y += 1
                        drop_points += 1
                        if not (fun.valid_space(current_piece, grid, settings)) and current_piece.y > 0:
                            current_piece.y -= 1
                            change_piece = True

                # rotate clockwise
                if event.key == cont.rotate_cw:
                    sl.rotate_sound.play()
                    current_piece.rotation += 1
                    if not (fun.valid_space(current_piece, grid, settings)):
                        current_piece.rotation -= 1

                # rotate anti-clockwise
                if event.key == cont.rotate_acw:
                    sl.rotate_sound.play()
                    current_piece.rotation -= 1
                    if not (fun.valid_space(current_piece, grid, settings)):
                        current_piece.rotation += 1

            # Stop moving piece when key up
            if event.type == pygame.KEYUP:
                if (event.key == cont.move_left) or (event.key == cont.move_right):
                    move_piece_x = 0
                    move_counter_x = 0
                if event.key == cont.soft_drop:
                    move_piece_y = 0
                    move_counter_y = 0

        # if left or right is pressed and held down
        if move_piece_x != 0:
            move_counter_x += 1

        if move_piece_y == 1:
            move_counter_y += 1

        if move_counter_x == 8:
            current_piece.x += move_piece_x
            if not (fun.valid_space(current_piece, grid, settings)):
                current_piece.x -= move_piece_x
            move_counter_x = 7

        if move_counter_y == 8:
            current_piece.y += move_piece_y
            if not (fun.valid_space(current_piece, grid, settings)):
                current_piece.y -= move_piece_y
            move_counter_y = 7

        piece_pos = fun.convert_piece_orientation(current_piece)

        # move ghost piece to bottom
        ghost_thing = True
        while ghost_thing:
            ghost_piece.y += 1
            if not (fun.valid_space(ghost_piece, grid, settings)) and ghost_piece.y > 0:
                ghost_piece.y -= 1
                ghost_thing = False

        ghost_piece_pos = fun.convert_piece_orientation(ghost_piece)

        oll_centre_pos = fun.convert_piece_orientation(oll_centre)

        # colour stuff in
        for i in range(len(piece_pos)):
            x, y = piece_pos[i]
            # need to prevent pieces from appearing from bottom of screen
            if y > -1:
                grid[y][x] = current_piece.colour

        # update time
        elapsed_time = time.time() - start_time

        if settings.mode == '40 Lines':
            if fun.check_win(lines):
                fun.draw_window(settings, grid, ghost_piece, ghost_piece_pos, oll_centre_pos, score,
                                fun.max_score(settings), level, lines,
                                single, double, triple, quad, pentris, elapsed_time)
                fun.draw_next_piece(next_piece, settings)
                sl.lock_sound.stop()
                pygame.mixer.music.stop()

                font = pygame.font.Font(settings.text_font, 60)
                fun.draw_text_middle(settings, 'YOU WIN', font, 80, (255, 255, 255), (0, 0))

                pygame.display.update()
                sl.youwin_sound.play()
                pygame.time.delay(4000)
                fun.update_scores(settings, elapsed_time)
                settings.background = sl.initial_background
                break

        if fun.check_lost(piece_pos, locked_positions):
            fun.draw_window(settings, grid, ghost_piece, ghost_piece_pos, oll_centre_pos, score,
                            fun.max_score(settings), level, lines,
                            single, double, triple, quad, pentris, elapsed_time)
            fun.draw_next_piece(next_piece, settings)
            sl.lock_sound.stop()
            pygame.mixer.music.stop()

            font = pygame.font.Font(settings.text_font, 60)
            fun.draw_text_middle(settings, 'GAME OVER', font, 80, (255, 255, 255), (0, 0))

            pygame.display.update()
            sl.gameover_sound.play()
            pygame.time.delay(6000)
            fun.update_scores(settings, score)
            settings.background = sl.initial_background
            break

        if change_piece:
            # update locked positions (but don't draw it yet)
            for pos in piece_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.colour

            current_piece = next_piece
            ghost_piece = copy.deepcopy(current_piece)
            # next piece. if same as current piece, generate another one (can be the same)
            next_piece = fun.get_piece(settings)
            if next_piece.shape == current_piece.shape:
                next_piece = fun.get_piece(settings)
            change_piece = False
            cleared_rows_count = fun.clear_rows(grid, locked_positions, settings)

            # scoring
            if cleared_rows_count == 1:
                sl.single_sound.play()
                score += (level + 1) * 40
                single += 1
            elif cleared_rows_count == 2:
                sl.double_sound.play()
                score += (level + 1) * 100
                double += 1
            elif cleared_rows_count == 3:
                sl.triple_sound.play()
                score += (level + 1) * 300
                triple += 1
            elif cleared_rows_count == 4:
                sl.quad_sound.play()
                score += (level + 1) * 1200
                quad += 1
            elif cleared_rows_count == 5:
                score += (level + 1) * 6000
                pentris += 1
            else:
                sl.lock_sound.play()

            score += drop_points
            drop_points = 0

            level_meter += cleared_rows_count
            lines += cleared_rows_count

            # basic entry delay
            if settings.delay:
                time.sleep(0.01)

        fun.draw_window(settings, grid, ghost_piece, ghost_piece_pos, oll_centre_pos,
                        score, fun.max_score(settings), level, lines,
                        single, double, triple, quad, pentris, elapsed_time)
        fun.draw_next_piece(next_piece, settings)

        pygame.display.update()

        # basic line clear delay
        if settings.delay:
            if cleared_rows_count > 0:
                time.sleep(0.3)
                cleared_rows_count = 0


def pause_menu(settings):
    run = True

    while run:
        settings.surface.fill((0, 50, 60))

        font = pygame.font.Font(settings.text_font, 60)

        fun.draw_text_middle(settings, 'PAUSED', font, 1, (210, 230, 150), (0, 0))
        fun.draw_text_middle(settings, 'Resume (start)', font, 1, (255, 255, 255), (0, 80))
        fun.draw_text_middle(settings, 'Quit (ESC)', font, 1, (255, 255, 255), (0, 160))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                if not settings.fullscreen:
                    settings.surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sl.ok_sound.play()
                    quit_confirm_menu(settings)
                if event.key == pygame.K_F11:
                    fun.toggle_fullscreen(settings)
                if event.key == cont.start:
                    sl.ok_sound.play()
                    run = False

                if event.key == pygame.K_m:
                    fun.mute_music(settings)


def quit_confirm_menu(settings):
    run = True

    while run:
        settings.surface.fill((0, 50, 60))

        font = pygame.font.Font(settings.text_font, 60)

        fun.draw_text_middle(settings, 'Are you sure?', font, 1, (210, 230, 150), (0, -50))
        fun.draw_text_middle(settings, 'Yes (1)', font, 1, (255, 255, 255), (-120, 50))
        fun.draw_text_middle(settings, 'No (2)', font, 1, (255, 255, 255), (120, 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                settings.surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sl.cancel_sound.play()
                    run = False
                if event.key == pygame.K_F11:
                    fun.toggle_fullscreen(settings)

                # quit
                if event.key == pygame.K_1:
                    sys.exit()

                # don't quit
                if event.key == pygame.K_2:
                    sl.cancel_sound.play()
                    run = False


def start_menu(settings):
    run = True

    while run:
        settings.surface.fill((0, 50, 60))

        pygame.draw.ellipse(settings.surface, (208, 112, 80),
                            [(int(settings.surface.get_width() / 2)) - 400,
                             int(settings.surface.get_height() / 4) - 60,
                             800, 220], 0)
        pygame.draw.ellipse(settings.surface, (200, 200, 200),
                            [(int(settings.surface.get_width() / 2)) - 400,
                             int(settings.surface.get_height() / 4) - 60,
                             800, 220], 45)
        font = pygame.font.Font(settings.text_font, 60)
        fun.draw_text_middle(settings, 'ROBERT YAU\'S', font, 1, (255, 255, 255),
                             (0, -settings.surface.get_height() // 4))
        font = pygame.font.Font(settings.text_font, 65)
        fun.draw_text_middle(settings, 'PRO PIECE STACKER', font, 1, (255, 255, 255),
                             (0, -(settings.surface.get_height() // 4) + 65))
        font = pygame.font.Font(settings.text_font, 200)
        fun.draw_text_middle(settings, '1', font, 1, (255, 255, 255),
                             (350, -(settings.surface.get_height() // 4) + 40))

        font = pygame.font.Font(settings.text_font, 60)
        fun.draw_text_middle(settings, 'Press Start', font, 1, (210, 230, 150), (0, settings.surface.get_height() // 4))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                if not settings.fullscreen:
                    settings.surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_F11:
                    fun.toggle_fullscreen(settings)

                if event.key == cont.start:
                    sl.ok_sound.play()
                    main_menu(settings)


def main_menu(settings):
    run = True

    while run:
        settings.surface.fill((0, 50, 60))

        font = pygame.font.Font(settings.text_font, 60)

        fun.draw_text_middle(settings, 'Main Menu', font, 1, (210, 230, 150), (0, -200))
        fun.draw_text_middle(settings, 'Play (1)', font, 1, (255, 255, 255), (0, 0))
        fun.draw_text_middle(settings, 'Settings (2)', font, 1, (255, 255, 255), (0, 80))
        fun.draw_text_middle(settings, 'Quit (ESC)', font, 1, (255, 255, 255), (0, 160))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                if not settings.fullscreen:
                    settings.surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    fun.toggle_fullscreen(settings)
                if event.key == pygame.K_1:
                    sl.ok_sound.play()
                    select_mode_menu(settings)
                if event.key == pygame.K_2:
                    sl.ok_sound.play()
                    settings_menu(settings)
                if event.key == pygame.K_ESCAPE:
                    sys.exit()


def select_mode_menu(settings):
    run = True

    while run:
        settings.surface.fill((0, 50, 60))

        font = pygame.font.Font(settings.text_font, 60)

        fun.draw_text_middle(settings, 'Select Mode', font, 1, (210, 230, 150), (0, -200))
        fun.draw_text_middle(settings, 'Classic (1)', font, 1, (96, 192, 96), (0, 0))
        fun.draw_text_middle(settings, '40 Lines (2)', font, 1, (208, 112, 80), (0, 80))
        fun.draw_text_middle(settings, 'Invisible (3)', font, 1, (208, 224, 255), (0, 160))
        fun.draw_text_middle(settings, 'Go back (ESC)', font, 1, (255, 255, 255), (0, 320))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                if not settings.fullscreen:
                    settings.surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sl.cancel_sound.play()
                    run = False
                if event.key == pygame.K_F11:
                    fun.toggle_fullscreen(settings)
                if event.key == pygame.K_1:
                    sl.ok_sound.play()
                    settings.delay = True
                    settings.mode = 'Classic'
                if event.key == pygame.K_2:
                    sl.ok_sound.play()
                    settings.delay = False
                    settings.mode = '40 Lines'
                if event.key == pygame.K_3:
                    sl.ok_sound.play()
                    settings.delay = False
                    settings.mode = 'Invisible'

            if settings.mode != 'not_specified':
                sl.ok_sound.play()
                piece_set_menu(settings)


def piece_set_menu(settings):
    run = True

    while run:
        settings.surface.fill((0, 50, 60))

        font = pygame.font.Font(settings.text_font, 60)

        fun.draw_text_middle(settings, 'Select Piece Set', font, 1, (210, 230, 150), (0, -200))
        fun.draw_text_middle(settings, 'Regular (1)', font, 1, (255, 192, 96), (0, 0))
        fun.draw_text_middle(settings, 'Pentris (2)', font, 1, (255, 144, 96), (0, 80))
        fun.draw_text_middle(settings, 'OLL (3)', font, 1, (208, 176, 255), (0, 160))
        fun.draw_text_middle(settings, 'Wacky (4)', font, 1, (112, 208, 240), (0, 240))
        fun.draw_text_middle(settings, 'Go back (ESC)', font, 1, (255, 255, 255), (0, 320))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                if not settings.fullscreen:
                    settings.surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sl.cancel_sound.play()
                    settings.mode = 'not_specified'
                    run = False
                if event.key == pygame.K_F11:
                    fun.toggle_fullscreen(settings)

                if event.key == pygame.K_1:
                    settings.piece_set_choice = sl.available_piece_sets[0]
                    settings.psps = psac.regular_psps
                if event.key == pygame.K_2:
                    settings.piece_set_choice = sl.available_piece_sets[1]
                    settings.psps = psac.pentris_psps
                if event.key == pygame.K_3:
                    settings.piece_set_choice = sl.available_piece_sets[2]
                    settings.psps = psac.oll_psps
                if event.key == pygame.K_4:
                    settings.piece_set_choice = sl.available_piece_sets[3]
                    settings.psps = psac.wacky_psps

            if settings.piece_set_choice != 'not_specified':
                fun.update_settings(settings)
                sl.ok_sound.play()
                level_menu(settings)


def level_menu(settings):
    run = True

    add_ten = 0
    level_picker = -1

    while run:
        settings.surface.fill((0, 50, 60))

        font = pygame.font.Font(settings.text_font, 60)

        fun.draw_text_middle(settings, 'Level', font, 1, (210, 230, 150), (0, -80))
        fun.draw_text_middle(settings, '0   1   2   3   4', font, 1, (255, 255, 255), (0, 0))
        fun.draw_text_middle(settings, '5   6   7   8   9', font, 1, (255, 255, 255), (0, 80))
        fun.draw_text_middle(settings, 'Go back (ESC)', font, 1, (255, 255, 255), (0, 320))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                settings.surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    sl.cancel_sound.play()
                    settings.piece_set_choice = 'not_specified'
                    run = False
                if event.key == pygame.K_F11:
                    fun.toggle_fullscreen(settings)

                if event.key == cont.rotate_cw:
                    add_ten = 10

                if event.key == pygame.K_0:
                    level_picker = 0
                elif event.key == pygame.K_1:
                    level_picker = 1
                elif event.key == pygame.K_2:
                    level_picker = 2
                elif event.key == pygame.K_3:
                    level_picker = 3
                elif event.key == pygame.K_4:
                    level_picker = 4
                elif event.key == pygame.K_5:
                    level_picker = 5
                elif event.key == pygame.K_6:
                    level_picker = 6
                elif event.key == pygame.K_7:
                    level_picker = 7
                elif event.key == pygame.K_8:
                    level_picker = 8
                elif event.key == pygame.K_9:
                    level_picker = 9

            if level_picker >= 0:
                sl.ok_sound.play()
                pygame.time.delay(1000)
                level = level_picker + add_ten
                fall_speed = sl.fall_speeds[level]
                first_advance_lines = sl.first_advance_lines[level]
                # reset add_ten
                add_ten = 0
                # reset level_picker
                level_picker = -1
                main(settings, level, fall_speed, first_advance_lines)


def settings_menu(settings):
    run = True

    while run:
        settings.surface.fill((0, 50, 60))

        font = pygame.font.Font(settings.text_font, 60)

        fun.draw_text_middle(settings, 'Settings', font, 1, (210, 230, 150), (0, -200))
        fun.draw_text_middle(settings, 'Go Back (ESC)', font, 1, (255, 255, 255), (0, 320))

        font = pygame.font.Font(settings.text_font, 40)

        fun.draw_text_middle(settings, 'Reset High Scores (1)', font, 1, (255, 255, 255), (0, 0))

        if settings.play_music:
            fun.draw_text_middle(settings, 'Music [ON] (2)', font, 1, (255, 255, 255), (0, 60))
        else:
            fun.draw_text_middle(settings, 'Music [OFF] (2)', font, 1, (255, 255, 255), (0, 60))

        if settings.play_sound_effects:
            fun.draw_text_middle(settings, 'SFX [ON] (3)', font, 1, (255, 255, 255), (0, 120))
        else:
            fun.draw_text_middle(settings, 'SFX [OFF] (3)', font, 1, (255, 255, 255), (0, 120))

        if settings.piece_style == 'Normal':
            fun.draw_text_middle(settings, 'Piece Style [Normal] (4)', font, 1, (255, 255, 255), (0, 180))
        elif settings.piece_style == 'Clear':
            fun.draw_text_middle(settings, 'Piece Style [Clear] (4)', font, 1, (255, 255, 255), (0, 180))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                if not settings.fullscreen:
                    settings.surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sl.cancel_sound.play()
                    run = False
                if event.key == pygame.K_F11:
                    fun.toggle_fullscreen(settings)

                if event.key == pygame.K_1:
                    sl.ok_sound.play()
                    reset_high_scores_menu(settings)
                if event.key == pygame.K_2:
                    sl.ok_sound.play()
                    settings.play_music = not settings.play_music
                if event.key == pygame.K_3:
                    sl.ok_sound.play()
                    fun.mute_sounds(settings)
                if event.key == pygame.K_4:
                    sl.ok_sound.play()
                    leng = len(sl.available_piece_styles)
                    cur_sty = sl.available_piece_styles.index(settings.piece_style)
                    settings.piece_style = sl.available_piece_styles[(cur_sty + 1) % leng]


def reset_high_scores_menu(settings):
    run = True

    while run:
        settings.surface.fill((0, 50, 60))

        font = pygame.font.Font(settings.text_font, 60)

        fun.draw_text_middle(settings, 'Are you sure?', font, 1, (210, 230, 150), (0, -50))
        fun.draw_text_middle(settings, 'Yes (1)', font, 1, (255, 255, 255), (-120, 50))
        fun.draw_text_middle(settings, 'No (2)', font, 1, (255, 255, 255), (120, 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                settings.surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sl.cancel_sound.play()
                    run = False
                if event.key == pygame.K_F11:
                    fun.toggle_fullscreen(settings)

                # reset high scores
                if event.key == pygame.K_1:
                    sl.ok_sound.play()
                    fun.reset_high_scores()
                    run = False

                # don't reset high scores
                if event.key == pygame.K_2:
                    sl.cancel_sound.play()
                    run = False


start_menu(sl.initial_settings)  # start game

pygame.quit()

sys.exit()
