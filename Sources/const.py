import os

# screen
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 760

# board
BOARD_SIZE = 600
BOARD_LOCATION_X = (SCREEN_WIDTH-BOARD_SIZE)//2 + 240
BOARD_LOCATION_Y = (SCREEN_HEIGHT-BOARD_SIZE)//2 + 40

# title
font_title_path = os.getcwd() + '\\..\\Assets\\font\\title_font.ttf'
TITLE_BASE_X = SCREEN_WIDTH//2
TITLE_BASE_Y = 100
TITLE_COLOR = '#FDD250'
TITLE_SIZE = 120

# text
font_text_path = os.getcwd() + '\\..\\Assets\\font\\text_font.otf'
TEXT_COLOR = '#A4925F'
TEXT_SIZE = 35

#textchat
font_textchat_path = os.getcwd() + '\\..\\Assets\\gameFont.ttf'
#logchat
logchat_path = os.getcwd() + '\\..\\Logchatfull\\full_log_all_time.txt'
# button
button_path = os.getcwd() + '\\..\\Assets\\png\\button.png'
hover_button_path = os.getcwd() + '\\..\\Assets\\png\\hover_button.png'
BUTTON_BASE_X = SCREEN_WIDTH//2
BUTTON_BASE_Y = 320

# button_map
map_path = os.getcwd() + '\\..\\Assets\\png\\map.png'
map_locked_path = os.getcwd() + '\\..\\Assets\\png\\map_locked.png'
BUTTON_MAP_SIZE = 120
BUTTON_MAP_MARGIN = 25
BUTTON_MAP_BASE_X = (SCREEN_WIDTH-BUTTON_MAP_SIZE*5-BUTTON_MAP_MARGIN*4)//2
BUTTON_MAP_BASE_Y = 280
MAP_COLOR='#FDE294'

# icon
icon_path = os.getcwd() + '\\..\\Assets\\icon\\'

# color
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREY = (200, 200, 200)
TRANSPARENT = (255, 255, 255, 25)

TEXTBOX_COLOR = 'white'
TEXTBOX_COLOR_ACTIVE = 'yellow' # light blue
BUTTON_LOGIN_COLOR = (152, 251, 152) # green_pale
BUTTON_LOGIN_COLOR_HOVER = (0, 128, 0)
BUTTON_EXIT_COLOR = (255, 182, 193) # light pink
BUTTON_EXIT_COLOR_HOVER = (255, 105, 97) # pink darker

BUTTON_COLOR = (192, 192, 192) # light gray
BUTTON_COLOR_HOVER = (128, 128, 128) # gray


BUTTON_WIDTH = 140
BUTTON_HEIGHT = 40


BUTTON_MAP_X = 55
BUTTON_MAP_Y = 30

MAP_EACH_LEVEL = 15

png_path = os.getcwd() + '\\..\\Assets\\png\\'
login_path = os.getcwd() + '\\..\\Assets\\login\\'
assets_path = os.getcwd() + '\\..\\Assets\\'
click_sound_path = os.getcwd() + '\\..\\Assets\\clicksound.wav'