import pygame
import re

# for each line, take last characters after = as string
# set control = key_dict[thing]

key_dict = {
    "a": pygame.K_a,
    "b": pygame.K_b,
    "c": pygame.K_c,
    "d": pygame.K_d,
    "e": pygame.K_e,
    "f": pygame.K_f,
    "g": pygame.K_g,
    "h": pygame.K_h,
    "i": pygame.K_i,
    "j": pygame.K_j,
    "k": pygame.K_k,
    "l": pygame.K_l,
    "m": pygame.K_m,
    "n": pygame.K_n,
    "o": pygame.K_o,
    "p": pygame.K_p,
    "q": pygame.K_q,
    "r": pygame.K_r,
    "s": pygame.K_s,
    "t": pygame.K_t,
    "u": pygame.K_u,
    "v": pygame.K_v,
    "w": pygame.K_w,
    "x": pygame.K_x,
    "y": pygame.K_y,
    "z": pygame.K_z,
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "right": pygame.K_RIGHT,
    "left": pygame.K_LEFT,
    "keypad_0": pygame.K_KP0,
    "keypad_1": pygame.K_KP1,
    "keypad_2": pygame.K_KP2,
    "keypad_3": pygame.K_KP3,
    "keypad_4": pygame.K_KP4,
    "keypad_5": pygame.K_KP5,
    "keypad_6": pygame.K_KP6,
    "keypad_7": pygame.K_KP7,
    "keypad_8": pygame.K_KP8,
    "keypad_9": pygame.K_KP9,
    "keypad_period": pygame.K_KP_PERIOD,
    "keypad_divide": pygame.K_KP_DIVIDE,
    "keypad_multiply": pygame.K_KP_MULTIPLY,
    "keypad_minus": pygame.K_KP_MINUS,
    "keypad_plus": pygame.K_KP_PLUS,
    "keypad_enter": pygame.K_KP_ENTER,
    "keypad_equals": pygame.K_KP_EQUALS,
    "insert": pygame.K_INSERT,
    "delete": pygame.K_DELETE,
    "home": pygame.K_HOME,
    "end": pygame.K_END,
    "page_up": pygame.K_PAGEUP,
    "page_down": pygame.K_PAGEDOWN,
    "backspace": pygame.K_BACKSPACE,
    "tab": pygame.K_TAB,
    "clear": pygame.K_CLEAR,
    "return": pygame.K_RETURN,
    "pause": pygame.K_PAUSE,
    "space": pygame.K_SPACE,
    "exclaim": pygame.K_EXCLAIM,
    "quotedbl": pygame.K_QUOTEDBL,
    "hash": pygame.K_HASH,
    "dollar": pygame.K_DOLLAR,
    "ampersand": pygame.K_AMPERSAND,
    "quote": pygame.K_QUOTE,
    "left_parenthesis": pygame.K_LEFTPAREN,
    "right_parenthesis": pygame.K_RIGHTPAREN,
    "asterisk": pygame.K_ASTERISK,
    "plus_sign": pygame.K_PLUS,
    "comma": pygame.K_COMMA,
    "minus_sign": pygame.K_MINUS,
    "period": pygame.K_PERIOD,
    "forward_slash": pygame.K_SLASH,
    "colon": pygame.K_COLON,
    "semicolon": pygame.K_SEMICOLON,
    "less_than_sign": pygame.K_LESS,
    "equals_sign": pygame.K_EQUALS,
    "greater_than_sign": pygame.K_GREATER,
    "question mark": pygame.K_QUESTION,
    "at": pygame.K_AT,
    "left_bracket": pygame.K_LEFTBRACKET,
    "backslash": pygame.K_BACKSLASH,
    "right_bracket": pygame.K_RIGHTBRACKET,
    "caret": pygame.K_CARET,
    "underscore": pygame.K_UNDERSCORE,
    "grave": pygame.K_BACKQUOTE,
}

f = open('Controls.txt', 'r')
matches = []
# match on pattern but only capture what is in parentheses
pattern = re.compile("[=][\s]?([a-z_]+)")
for line in f:
    matches += pattern.findall(line)
f.close()


move_left = key_dict[matches[0]]
move_right = key_dict[matches[1]]
soft_drop = key_dict[matches[2]]
hard_drop = key_dict[matches[3]]
rotate_cw = key_dict[matches[4]]
rotate_acw = key_dict[matches[5]]
start = key_dict[matches[6]]
