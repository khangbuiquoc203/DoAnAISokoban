import pygame
from pygame.locals import *
import sys
import const as c
from build_map import *

def init():
    pygame.init()
    screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT)) 
    pygame.display.set_caption('Sokoban')

    run = True
    while run:
        screen.fill('white')
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        check = login(screen)
        if check == 1:
            pygame.quit()
            sys.exit()
        elif check == 0:
            continue
        else:
            print("success!\nHello",check)
            game(screen, check)

def draw_background(screen):
    # background
    screen.fill('white')
    background = pygame.image.load(c.assets_path + 'init_background.png')
    background = pygame.transform.scale(background, (c.SCREEN_WIDTH,c.SCREEN_HEIGHT))
    screen.blit(background, (0,0))
    
def draw_title(screen, text):
    # title
    font_title = pygame.font.Font(c.font_title_path, c.TITLE_SIZE)
    title = font_title.render(text, True, c.TITLE_COLOR)
    text_rect = title.get_rect()
    text_rect.center = (c.TITLE_BASE_X, c.TITLE_BASE_Y)
    screen.blit(title, text_rect)
    
# BUTTON
def create_buttons(buttons, quantity, texts):
    for i in range(quantity):
        picture = pygame.image.load(c.button_path)
        picture = pygame.transform.scale(picture, (picture.get_width()*1.2, picture.get_height()))
        picture_rect = picture.get_rect(center=(c.BUTTON_BASE_X, c.BUTTON_BASE_Y + i*(picture.get_height() + 20)))
        
        font = pygame.font.Font(c.font_text_path, c.TEXT_SIZE)
        text = font.render(texts[i], True, c.TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.center = (c.BUTTON_BASE_X, c.BUTTON_BASE_Y + i*(picture.get_height() + 20) - 5)
        buttons.append([picture, picture_rect, text, text_rect])

def set_hover_button(buttons, hover):
    # đặt lại picture trong list button, sau đó set picture của button có vị trí index là hover thành hover_button.png
    for i in buttons:
        # i: [picture, picture_rect, text, text_rect]
        i[0] = pygame.image.load(c.button_path) 
        i[0] = pygame.transform.scale(i[0], (i[0].get_width()*1.2, i[0].get_height()))
        
    # hover == -1 -> hover is null    
    if hover != -1:
        buttons[hover][0] = pygame.image.load(c.hover_button_path)
        buttons[hover][0] = pygame.transform.scale(buttons[hover][0], (buttons[hover][0].get_width()*1.2, buttons[hover][0].get_height()))
       
def create_buttons_map(buttons, quantity, level):
    # create texts
    texts = []
    for i in range(quantity):
        texts.append(str(level*10 + i + 1))
        
    for row in range (quantity//5):
        for col in range(quantity//2):
            picture = pygame.image.load(c.map_path)
            picture = pygame.transform.scale(picture, (int(picture.get_width()*1.2),int(picture.get_height()*1.2)))
            picture_rect = picture.get_rect(topleft=(c.BUTTON_MAP_BASE_X + col*(c.BUTTON_MAP_MARGIN + c.BUTTON_MAP_SIZE), 
                                                     c.BUTTON_MAP_BASE_Y + row*(c.BUTTON_MAP_MARGIN + c.BUTTON_MAP_SIZE)))
            
            font = pygame.font.Font(c.font_text_path, c.TEXT_SIZE)
            text = font.render(texts[5*row + col], True, c.MAP_COLOR)
            text_rect = text.get_rect()
            text_rect.center = picture_rect.center
            text_rect.top = text_rect.top-15
            
            buttons.append([picture, picture_rect, text, text_rect, level*10+5*row + col]) # stage = level*10+5*row + col

def set_hover_button_map(buttons, hover):
    # đặt lại picture trong list button, sau đó set picture của button có vị trí index là hover thành hover_button.png
    for i in buttons:
        # i: [picture, picture_rect, text, text_rect]
        i[0] = pygame.image.load(c.button_map_path) 
        i[0] = pygame.transform.scale(i[0], (c.BUTTON_MAP_SIZE,c.BUTTON_MAP_SIZE))
        
    # hover == -1 -> hover is null    
    if hover != -1:
        buttons[hover][0] = pygame.image.load(c.hover_button_map_path)
        buttons[hover][0] = pygame.transform.scale(buttons[hover][0], (c.BUTTON_MAP_SIZE,c.BUTTON_MAP_SIZE))

# LOGIN: return 0: none, 1: quit, 2: success
def login(screen):
    active = None
    username = ""
    while True:
        draw_background(screen)
        draw_title(screen, 'LOGIN')
        
        # text
        font = pygame.font.Font(c.font_text_path, c.TEXT_SIZE)
        text = font.render('Enter username:', True, 'white')
        text_rect = text.get_rect(center=(c.SCREEN_WIDTH//2,300))
        screen.blit(text, text_rect)
        
        
        # textbox
        textbox_username = pygame.Rect(text_rect.left,text_rect.top+50,text.get_width(),text.get_height()+10)
        pygame.draw.rect(screen, c.TEXTBOX_COLOR, textbox_username, 2)
        
        # button
        button_login = pygame.image.load(c.button_path)
        button_login = pygame.transform.scale(button_login, (button_login.get_width()*1.2, button_login.get_height()))
        button_login_rect = button_login.get_rect(center=text_rect.center)
        button_login_rect.top += 140
        
        screen.blit(button_login, button_login_rect)
        
        login_text = font.render('OK', True, c.TEXT_COLOR)
        login_text_rect = login_text.get_rect(center=button_login_rect.center)
        screen.blit(login_text, login_text_rect)
        
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                return 1
            if event.type == MOUSEBUTTONDOWN:
                if textbox_username.collidepoint(event.pos):
                    active = textbox_username
                elif button_login_rect.collidepoint(event.pos):
                    return check_login(username)
                else:
                    active = None
            if event.type == pygame.KEYDOWN:
                if active is not None:
                    if event.key == pygame.K_RETURN:
                        return check_login(username)
                    elif event.key == pygame.K_BACKSPACE:
                        if active == textbox_username:
                            username = username[:-1]
                    else:
                        if active == textbox_username:
                            username += event.unicode

        if active == textbox_username:
            pygame.draw.rect(screen, c.TEXTBOX_COLOR_ACTIVE, textbox_username, 2)
        
        user_text = font.render(username, True, 'white')
        
        screen.blit(user_text, (textbox_username.x + 5, textbox_username.y + 5))
        # update
        pygame.display.update()

def check_login(user):
    if user == '':
        return 0
    list_user = []
    with open(c.login_path+"\\user.txt", 'r') as file:
        list_user = file.readlines()
    
    for i in list_user:
        if user == i[:-1]:
            return user
    
    list_user.append(user+"\n")
    
    with open(c.login_path+"\\user.txt", 'w') as file:
        file.writelines(list_user)
        return user
    
def quit():
    pygame.quit()
    sys.exit()

# SCREEN GAME
def game(screen, user):
    
    # danh sách 4 button, mỗi button chứa [picture, picture_rect, text, text_rect]
    buttons = []
    create_buttons(buttons, 4, ['PLAY', 'SCORE', 'OPTION', 'QUIT'])
    
    hover = -1
    while True:
        
        draw_background(screen)
        draw_title(screen, 'SOKOBAN')
        
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEMOTION:
                for i in range(4):
                    # buttons: list of [picture, picture_rect, text, text_rect]
                    if buttons[i][1].collidepoint(event.pos):
                        hover = i
                        break
                    hover = -1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:               
                if hover == 0:
                    play(screen)
                    hover = -1
                elif hover == 1:
                    print('score')
                    hover = -1
                elif hover == 2:
                    print('option')
                    hover = -1
                elif hover == 3:
                    quit()
               
        # do hover button và button thường khác nhau nên khi hover != null thì cần set lại     
        set_hover_button(buttons, hover)
        
        # draw button
        for i in buttons:
            screen.blit(i[0], i[1]) # blit button
            screen.blit(i[2], i[3]) # blit text
                
        pygame.display.update()

# SCREEN PLAY
def play(screen):
    # danh sách 4 button, mỗi button chứa [picture, picture_rect, text, text_rect]
    buttons = []
    create_buttons(buttons, 4, ['1 PLAYER', '2 PLAYER', 'AI', 'BACK'])
    
    hover = -1
    running = True
    while running:
        draw_background(screen)
        draw_title(screen, 'SOKOBAN')
        
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEMOTION:
                for i in range(4):
                    # buttons: list of [picture, picture_rect, text, text_rect]
                    if buttons[i][1].collidepoint(event.pos):
                        hover = i
                        break
                    hover = -1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:               
                if hover == 0:
                    player_1(screen)
                    hover = -1
                elif hover == 1:
                    player_2(screen)
                    hover = -1
                elif hover == 2:
                    AI(screen)
                    hover = -1
                elif hover == 3:
                    running = False
        
        # do hover button và button thường khác nhau nên khi hover != null thì cần set lại
        set_hover_button(buttons, hover)
        
        # draw button
        for i in buttons:
            screen.blit(i[0], i[1]) # blit button
            screen.blit(i[2], i[3]) # blit text
                
        pygame.display.update()

# SCREEN SCORE
def score(screen):
    print('score')
    
# SCREEN OPTION
def option(screen):
    print('option')


# SCREEN PLAYER
def player_1(screen):
    # danh sách 4 button, mỗi button chứa [picture, picture_rect, text, text_rect]
    buttons = []
    create_buttons(buttons, 4, ['EASY', 'MEDIUM', 'HARD', 'BACK'])
    
    hover = -1
    running = True
    while running:
        
        draw_background(screen)
        draw_title(screen, 'SOKOBAN')
        
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEMOTION:
                for i in range(4):
                    # buttons: list of [picture, picture_rect, text, text_rect]
                    if buttons[i][1].collidepoint(event.pos):
                        hover = i
                        break
                    hover = -1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:               
                if hover == 0:
                    map(screen, level=0)
                    hover = -1
                elif hover == 1:
                    map(screen, level=1)
                    hover = -1
                elif hover == 2:
                    map(screen, level=2)
                    hover = -1
                elif hover == 3:
                    running = False
        
        # do hover button và button thường khác nhau nên khi hover != null thì cần set lại
        set_hover_button(buttons, hover)
        
        # draw button
        for i in buttons:
            screen.blit(i[0], i[1]) # blit button
            screen.blit(i[2], i[3]) # blit text
        
        pygame.display.update()
    
def player_2(screen):
    # danh sách 4 button, mỗi button chứa [picture, picture_rect, text, text_rect]
    buttons = []
    create_buttons(buttons, 4, ['EASY', 'MEDIUM', 'HARD', 'BACK'])
    
    hover = -1
    running = True
    while running:
        
        draw_background(screen)
        draw_title(screen, 'SOKOBAN')
       
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEMOTION:
                for i in range(4):
                    # buttons: list of [picture, picture_rect, text, text_rect]
                    if buttons[i][1].collidepoint(event.pos):
                        hover = i
                        break
                    hover = -1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:               
                if hover == 0:
                    map(screen, level=0)
                    hover = -1
                elif hover == 1:
                    map(screen, level=1)
                    hover = -1
                elif hover == 2:
                    map(screen, level=2)
                    hover = -1
                elif hover == 3:
                    running = False
        
        # do hover button và button thường khác nhau nên khi hover != null thì cần set lại
        set_hover_button(buttons, hover)
        
        # draw button
        for i in buttons:
            screen.blit(i[0], i[1]) # blit button
            screen.blit(i[2], i[3]) # blit text
        
        pygame.display.update()
    
def AI(screen):
    # danh sách 4 button, mỗi button chứa [picture, picture_rect, text, text_rect]
    buttons = []
    create_buttons(buttons, 4, ['EASY', 'MEDIUM', 'HARD', 'BACK'])
    
    hover = -1
    running = True
    while running:
        
        draw_background(screen)
        draw_title(screen, 'SOKOBAN')
       
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEMOTION:
                for i in range(4):
                    # buttons: list of [picture, picture_rect, text, text_rect]
                    if buttons[i][1].collidepoint(event.pos):
                        hover = i
                        break
                    hover = -1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:               
                if hover == 0:
                    map(screen, level=0)
                    hover = -1
                elif hover == 1:
                    map(screen, level=1)
                    hover = -1
                elif hover == 2:
                    map(screen, level=2)
                    hover = -1
                elif hover == 3:
                    running = False
        
        # do hover button và button thường khác nhau nên khi hover != null thì cần set lại
        set_hover_button(buttons, hover)
        
        # draw button
        for i in buttons:
            screen.blit(i[0], i[1]) # blit button
            screen.blit(i[2], i[3]) # blit text
        
        pygame.display.update()

# SCREEN MAP
def map(screen, level):
    # danh sách 10 button, mỗi button chứa [picture, picture_rect, text, text_rect, stage]
    buttons = []
    quantity = 10 
    create_buttons_map(buttons, quantity, level)
    
    back = pygame.image.load(c.icon_path+"\\back.png")
    back_rect = back.get_rect(topleft=(10,c.SCREEN_HEIGHT-back.get_height()))
    running = True
    hover = -1
    while running:
        
        draw_background(screen)
        draw_title(screen, 'MAP')
        
        screen.blit(back, back_rect)
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEMOTION:
                for i in range(quantity):
                    # buttons: list of [picture, picture_rect, text, text_rect]
                    if buttons[i][1].collidepoint(event.pos):
                        hover = i
                        break
                    hover = -1

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:               
                if hover != -1:
                    sokoban(screen, buttons[hover][4])
                    hover = -1 # đặt lại hover mỗi lần load map
                if back_rect.collidepoint(event.pos):
                    running = False
        
        
        
        # draw button
        for i in buttons:
            screen.blit(i[0], i[1]) # blit button
            screen.blit(i[2], i[3]) # blit text
                
        pygame.display.update()