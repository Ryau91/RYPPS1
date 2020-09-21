import pygame
import glob
import piece_sets_and_colours as psac
import random

pygame.init()
pygame.font.init()

initial_s_width = int(pygame.display.Info().current_w * 0.8)
initial_s_height = int(pygame.display.Info().current_h * 0.8)

initial_window = pygame.display.set_mode((initial_s_width, initial_s_height), pygame.RESIZABLE)
initial_fullscreen = False
initial_cell_size = 30

initial_play_music = True
initial_play_sounds = True
initial_music_volume = 1
initial_sound_effects_volume = 0.2


# backgrounds
background_paths = glob.glob("./images/*.jpg")

backgrounds = []
for path in background_paths:
    image = pygame.image.load(path)
    resized_image = pygame.transform.scale(image, (1920, 1080))
    backgrounds.append(resized_image)

initial_background = random.choice(backgrounds)

# text
initial_text_font = 'font\\Rubik-ExtraBoldItalic.ttf'
initial_font_size = 40

# piece
initial_piece_set_choice = 'not_specified'
initial_psps = psac.PieceSetPlaySettings(None, None, 0, 0, 0, 0, 0)
initial_piece_style = 'Normal'

# mode
initial_mode = 'not_specified'

# music and sounds # GET LIST OF SOUNDS and modify with FOR LOOP

# background music
music = pygame.mixer.music.load('sounds\\moonson3rdmove.mp3')
pygame.mixer_music.set_volume(initial_music_volume)

# menu sounds
ok_sound = pygame.mixer.Sound('sounds\\se_sys_ok.wav')

# cancel
cancel_sound = pygame.mixer.Sound('sounds\\se_sys_cancel.wav')

# win lose
youwin_sound = pygame.mixer.Sound('sounds\\me_game_iget.wav')
gameover_sound = pygame.mixer.Sound('sounds\\me_game_gameover.wav')

# pause
pause_sound = pygame.mixer.Sound('sounds\\se_game_pause.wav')

# control sounds
move_sound = pygame.mixer.Sound('sounds\\se_game_move.wav')
softdrop_sound = pygame.mixer.Sound('sounds\\se_game_softdrop.wav')
harddrop_sound = pygame.mixer.Sound('sounds\\se_game_harddrop.wav')
rotate_sound = pygame.mixer.Sound('sounds\\se_game_rotate.wav')
lock_sound = pygame.mixer.Sound('sounds\\se_game_fixa.wav')

# line clearing sounds
single_sound = pygame.mixer.Sound('sounds\\se_game_single.wav')
double_sound = pygame.mixer.Sound('sounds\\se_game_double.wav')
triple_sound = pygame.mixer.Sound('sounds\\se_game_triple.wav')
quad_sound = pygame.mixer.Sound('sounds\\se_game_quad.wav')

# level up sound
levelup_sound = pygame.mixer.Sound('sounds\\me_game_plvup.wav')

sounds = [ok_sound, cancel_sound, youwin_sound, gameover_sound, pause_sound, move_sound,
          softdrop_sound, harddrop_sound, rotate_sound, lock_sound,
          single_sound, double_sound, triple_sound, quad_sound, levelup_sound]

for sound in sounds:
    sound.set_volume(initial_sound_effects_volume)

# frame rate
fps = 60


pygame.display.set_caption('RYPPS1')

fall_speeds = [48, 43, 38, 33, 28, 23, 18, 13, 8, 6,
               5, 5, 5, 4, 4, 4, 3, 3, 3, 2]

# available_piece_sets and styles
available_piece_sets = ["Regular", "Pentris", "OLL", "Wacky"]
available_piece_styles = ["Normal", "Clear"]


class Settings(object):
    def __init__(self, surface, fullscreen, cell_size, play_music, play_sound_effects,
                 music_volume, sound_effects_volume, text_font, font_size,
                 piece_set_choice, psps, piece_style, mode, background):
        self.surface = surface
        self.fullscreen = fullscreen
        self.cell_size = cell_size
        self.play_music = play_music
        self.music_is_playing = not self.play_music
        self.play_sound_effects = play_sound_effects
        self.music_volume = music_volume
        self.sound_effects_volume = sound_effects_volume
        self.text_font = text_font
        self.font_size = font_size
        self.piece_set_choice = piece_set_choice
        self.psps = psps
        self.play_width = psps.play_width_cells * cell_size
        self.play_height = psps.play_height_cells * cell_size
        self.left_grid_x = (surface.get_width() - self.play_width) // 2
        self.right_grid_x = (surface.get_width() + self.play_width) // 2
        self.top_grid_y = (surface.get_height() - self.play_height) // 2
        self.bottom_grid_y = (surface.get_height() + self.play_height) // 2
        self.piece_style = piece_style
        self.mode = mode
        self.background = background


initial_settings = Settings(initial_window,
                            initial_fullscreen,
                            initial_cell_size,
                            initial_play_music,
                            initial_play_sounds,
                            initial_music_volume,
                            initial_sound_effects_volume,
                            initial_text_font,
                            initial_font_size,
                            initial_piece_set_choice,
                            initial_psps,
                            initial_piece_style,
                            initial_mode,
                            initial_background)
