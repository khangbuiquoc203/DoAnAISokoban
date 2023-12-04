import User
import build_map_2player
# import build_map_play_with_AI

import pygame
from pygame.locals import *
import sys
import const as c
from build_map import *
import random
import setting as s
is_play_music = True

def init():
    pygame.init()
    screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT)) 
    pygame.display.set_caption('Sokoban')
    pygame.display.set_icon(pygame.image.load(c.assets_path + '\\icon_image.png'))
    
    pygame.mixer.init()
    pygame.mixer.music.load(c.assets_path+'music.mp3')  # Đặt đường dẫn đến file nhạc của bạn
    pygame.mixer.music.set_volume(0.3)  # Đặt âm lượng (từ 0.0 đến 1.0)
    
    # Bắt đầu phát nhạc
    pygame.mixer.music.play(-1)  # -1 để lặp vô hạn, 0 để chơi một lần
    
    run = True
    while run:
        screen.fill('white')
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        global user
        user = login(screen)
        if user == None:
            continue
        else:
            game(screen)

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

def draw_welcome(screen, text):
    font_title = pygame.font.Font(c.font_title_path, 40)
    title = font_title.render(text, True, '#f4c12a')
    text_rect = title.get_rect()
    text_rect.center = (c.TITLE_BASE_X, c.TITLE_BASE_Y+90)
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
       
def create_buttons_map(buttons, quantity, level, user_score):
    texts = []
    i = 0
    while i<quantity:
        if int(user_score[level*10 + i]) != -1:
            font = pygame.font.Font(c.font_text_path, c.TEXT_SIZE)
            text = font.render(str(level*10 + i + 1), True, c.MAP_COLOR)
            texts.append(text)
        else:
            texts.append(pygame.image.load(c.icon_path+'Locker.png'))
        i += 1
    
    for row in range (quantity//5):
        for col in range(quantity//2):
            picture = pygame.image.load(c.map_path)
            picture = pygame.transform.scale(picture, (int(picture.get_width()*1.2),int(picture.get_height()*1.2)))
            picture_rect = picture.get_rect(topleft=(c.BUTTON_MAP_BASE_X + col*(c.BUTTON_MAP_MARGIN + c.BUTTON_MAP_SIZE), 
                                                     c.BUTTON_MAP_BASE_Y + row*(c.BUTTON_MAP_MARGIN + c.BUTTON_MAP_SIZE)))
            
            text_rect = texts[row*5+col].get_rect()
            text_rect.center = picture_rect.center
            text_rect.top = text_rect.top-15
            
            buttons.append([picture, picture_rect, texts[row*5+col], text_rect, level*10+5*row + col]) # stage = level*10+5*row + col

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
    buttons = []
    create_buttons(buttons, 1, ['OK'])
    hover = -1
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
        buttons[0][1].center = text_rect.center
        buttons[0][1].top += 140
        buttons[0][3].center = buttons[0][1].center
        buttons[0][3].top -= 5
        screen.blit(buttons[0][0], buttons[0][1])
        screen.blit(buttons[0][2], buttons[0][3])
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEMOTION:
                if buttons[0][1].collidepoint(event.pos):
                    hover = 0
                else:
                    hover = -1
            if event.type == MOUSEBUTTONDOWN:
                if textbox_username.collidepoint(event.pos):
                    active = textbox_username
                elif buttons[0][1].collidepoint(event.pos):
                    pygame.mixer.Sound(c.click_sound_path).play()
                    if User.get_user(username) == None:
                        continue
                    else:
                        return User.get_user(username)
                else:
                    active = None
            if event.type == pygame.KEYDOWN:
                if active is not None:
                    if event.key == pygame.K_RETURN:
                        if User.get_user(username) == None:
                            continue
                        else:
                            return User.get_user(username)
                    elif event.key == pygame.K_BACKSPACE:
                        if active == textbox_username:
                            username = username[:-1]
                    else:
                        if active == textbox_username:
                            username += event.unicode

        set_hover_button(buttons, hover)
        if active == textbox_username:
            pygame.draw.rect(screen, c.TEXTBOX_COLOR_ACTIVE, textbox_username, 2)
        
        user_text = font.render(username, True, 'white')
        
        screen.blit(user_text, (textbox_username.x + 5, textbox_username.y + 5))
        # update
        pygame.display.update()
    
def quit():
    pygame.quit()
    sys.exit()

# SCREEN GAME
def game(screen):
    # danh sách 4 button, mỗi button chứa [picture, picture_rect, text, text_rect]
    buttons = []
    create_buttons(buttons, 4, ['PLAY', 'SCORE', 'SETTING', 'QUIT'])
    
    hover = -1
    while True:
        draw_background(screen)
        draw_title(screen, 'SOKOBAN')
        draw_welcome(screen, 'WELCOME '+user.username)
        
        # do hover button và button thường khác nhau nên khi hover != null thì cần set lại     
        set_hover_button(buttons, hover)
        
        # draw button
        for i in buttons:
            screen.blit(i[0], i[1]) # blit button
            screen.blit(i[2], i[3]) # blit text
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
                    pygame.mixer.Sound(c.click_sound_path).play()           
                    play(screen)
                    hover = -1 
                elif hover == 1:
                    pygame.mixer.Sound(c.click_sound_path).play()           
                    score(screen)
                    hover = -1
                elif hover == 2:
                    pygame.mixer.Sound(c.click_sound_path).play()           
                    setting(screen)
                    hover = -1
                elif hover == 3:
                    pygame.mixer.Sound(c.click_sound_path).play()           
                    quit()
               
                
        pygame.display.update()

# SCREEN PLAY
def play(screen):
    # danh sách 4 button, mỗi button chứa [picture, picture_rect, text, text_rect]
    buttons = []
    create_buttons(buttons, 3, ['1 PLAYER', '2 PLAYER', 'BACK'])
    
    hover = -1
    running = True
    while running:
        draw_background(screen)
        draw_title(screen, 'SOKOBAN')
        draw_welcome(screen, 'WELCOME '+user.username)
        
        # do hover button và button thường khác nhau nên khi hover != null thì cần set lại
        set_hover_button(buttons, hover)
        
        # draw button
        for i in buttons:
            screen.blit(i[0], i[1]) # blit button
            screen.blit(i[2], i[3]) # blit text
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEMOTION:
                for i in range(3):
                    # buttons: list of [picture, picture_rect, text, text_rect]
                    if buttons[i][1].collidepoint(event.pos):
                        hover = i
                        break
                    hover = -1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:        
                if hover == 0:
                    pygame.mixer.Sound(c.click_sound_path).play()           
                    player_1(screen)
                    hover = -1
                elif hover == 1:
                    pygame.mixer.Sound(c.click_sound_path).play()           
                    player_2(screen)
                    hover = -1
                elif hover == 2:
                    pygame.mixer.Sound(c.click_sound_path).play()           
                    running = False
        
                
        pygame.display.update()

# SCREEN SCORE
def score(screen):
    back = pygame.image.load(c.icon_path+'back.png')
    back_rect = back.get_rect(topleft=(10,c.SCREEN_HEIGHT-back.get_height()))
    running = True
    while running:
        draw_background(screen)
        draw_title(screen, 'SOKOBAN')
        draw_welcome(screen, 'HIGHEST SCORE')
        screen.blit(back, back_rect)
        highest_score_users = User.get_top10_highest_score()
        for i in range(len(highest_score_users)):
            controls.Label(c.font_title_path, str(i+1), size=30, color=c.TITLE_COLOR, 
                                   location_topleft=(c.SCREEN_WIDTH//2-250,250+i*50)).draw(screen)
            
            controls.Label(c.font_title_path, str(highest_score_users[i][0]), size=30, color=c.TITLE_COLOR, 
                                   location_topleft=(c.SCREEN_WIDTH//2-70,250+i*50)).draw(screen)
            
            controls.Label(c.font_title_path, str(highest_score_users[i][1]), size=30, color=c.TITLE_COLOR, 
                                   location_topleft=(c.SCREEN_WIDTH//2+150,250+i*50)).draw(screen)
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:     
                if back_rect.collidepoint(event.pos):
                    pygame.mixer.Sound(c.click_sound_path).play()           
                    running = False
        pygame.display.update()
    
# SCREEN OPTION
def setting(screen):
    back = pygame.image.load(c.icon_path+'back.png')
    back_rect = back.get_rect(topleft=(10,c.SCREEN_HEIGHT-back.get_height()))
    running = True
    active = None
    while running:
        draw_background(screen)
        draw_title(screen, 'SOKOBAN')
        draw_welcome(screen, 'SETTING')
        screen.blit(back, back_rect)
        setting_player1 = [s.up_player1, s.down_player1, s.left_player1, s.right_player1, s.undo_player1]
        setting_player2 = [s.up_player2, s.down_player2, s.left_player2, s.right_player2, s.undo_player2]
        # draw text player 1
        controls.Label(c.font_title_path, 'Player 1', size=25, color='white', 
                            location_topleft=(c.SCREEN_WIDTH//2-250,250)).draw(screen)
        texts = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'UNDO']
        for i in range(5):
            controls.Label(c.font_title_path, texts[i], size=20, color=c.TITLE_COLOR, 
                            location_topleft=(c.SCREEN_WIDTH//2-250+(i%2)*300,300+(i//2)*50)).draw(screen)
        # draw text player 2
        controls.Label(c.font_title_path, 'Player 2', size=25, color='white', 
                            location_topleft=(c.SCREEN_WIDTH//2-250,450)).draw(screen)
        for i in range(5):
            controls.Label(c.font_title_path, texts[i], size=20, color=c.TITLE_COLOR, 
                            location_topleft=(c.SCREEN_WIDTH//2-250+(i%2)*300,500+(i//2)*50)).draw(screen)
        
        controls.Label(c.font_title_path, 'Others', size=25, color='white', 
                            location_topleft=(c.SCREEN_WIDTH//2-250,650)).draw(screen)
        # draw text reset
        controls.Label(c.font_title_path, "Reset", size=20, color=c.TITLE_COLOR, 
                        location_topleft=(c.SCREEN_WIDTH//2-250,700)).draw(screen)
        # textbox player 1 
        textboxs_player1 = []
        for i in range(5):
            textbox = pygame.Rect(c.SCREEN_WIDTH//2-150+(i%2)*300,295+(i//2)*50,180,25+10)
            textboxs_player1.append(textbox)
        
        for i in range(len(textboxs_player1)):
            pygame.draw.rect(screen, c.TEXTBOX_COLOR, textboxs_player1[i], 2)
            
            controls.Label(c.font_title_path, pygame.key.name(setting_player1[i]), size=20, color='red', 
                            location_topleft=(textboxs_player1[i].x+10,textboxs_player1[i].y+5)).draw(screen)
            
        # textbox player 2
        textboxs_player2 = []
        for i in range(5):
            textbox = pygame.Rect(c.SCREEN_WIDTH//2-150+(i%2)*300,495+(i//2)*50,180,25+10)
            textboxs_player2.append(textbox)
        # textbox reset
        for i in range(len(textboxs_player2)):
            pygame.draw.rect(screen, c.TEXTBOX_COLOR, textboxs_player2[i], 2)  
            
            controls.Label(c.font_title_path, pygame.key.name(setting_player2[i]), size=20, color='red', 
                            location_topleft=(textboxs_player2[i].x+10,textboxs_player2[i].y+5)).draw(screen)
        
        reset_textbox = pygame.Rect(c.SCREEN_WIDTH//2-150,695,100,25+10)
        pygame.draw.rect(screen, c.TEXTBOX_COLOR, reset_textbox, 2)  
        
        controls.Label(c.font_title_path, pygame.key.name(s.reset), size=20, color='red', 
                        location_topleft=(reset_textbox.x+10,reset_textbox.y+5)).draw(screen)
        
        pygame.display.update()# event
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:   
                for i in textboxs_player1:
                    if i.collidepoint(event.pos):
                        active = i
                for i in textboxs_player2:
                    if i.collidepoint(event.pos):
                        active = i 
                if reset_textbox.collidepoint(event.pos):
                    active = reset_textbox
                if back_rect.collidepoint(event.pos):
                    pygame.mixer.Sound(c.click_sound_path).play()           
                    running = False
                    
            if event.type == pygame.KEYDOWN:
                if active == textboxs_player1[0]:
                    s.up_player1 = event.key
                    
                if active == textboxs_player1[1]:
                    s.down_player1 = event.key
                    
                if active == textboxs_player1[2]:
                    s.left_player1 = event.key
                    
                if active == textboxs_player1[3]:
                    s.right_player1 = event.key
                    
                if active == textboxs_player1[4]:
                    s.undo_player1 = event.key
                    
                if active == textboxs_player2[0]:
                    s.up_player2 = event.key
                    
                if active == textboxs_player2[1]:
                    s.down_player2 = event.key
                    
                if active == textboxs_player2[2]:
                    s.left_player2 = event.key
                    
                if active == textboxs_player2[3]:
                    s.right_player2 = event.key
                    
                if active == textboxs_player2[4]:
                    s.undo_player1 = event.key
                    
                if active == reset_textbox:
                    s.reset = event.key
                    
        for i in textboxs_player1:
            if active == i:
                pygame.draw.rect(screen, c.TEXTBOX_COLOR_ACTIVE, i, 2)         
        for i in textboxs_player2:
            if active == i:
                pygame.draw.rect(screen, c.TEXTBOX_COLOR_ACTIVE, i, 2)                
        if active == reset_textbox:
            pygame.draw.rect(screen, c.TEXTBOX_COLOR_ACTIVE, reset_textbox, 2)                
    
        pygame.display.update()
        
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
        draw_welcome(screen, 'WELCOME '+user.username)
        
        # do hover button và button thường khác nhau nên khi hover != null thì cần set lại
        set_hover_button(buttons, hover)
        
        # draw button
        for i in buttons:
            screen.blit(i[0], i[1]) # blit button
            screen.blit(i[2], i[3]) # blit text
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
                    pygame.mixer.Sound(c.click_sound_path).play()           
                    map(screen, level=0)
                    hover = -1
                elif hover == 1:
                    pygame.mixer.Sound(c.click_sound_path).play()           
                    map(screen, level=1)
                    hover = -1
                elif hover == 2:
                    pygame.mixer.Sound(c.click_sound_path).play()           
                    map(screen, level=2)
                    hover = -1
                elif hover == 3:
                    pygame.mixer.Sound(c.click_sound_path).play()           
                    running = False
        
        
        pygame.display.update()
    
def player_2(screen):
    stage_list  = list(range(30))
    random.shuffle(stage_list)

    build_map_2player.sokoban_2_player(screen, stage_list, is_play_music)
    
def AI(screen):
    
    stage_list  = list(range(30))
    random.shuffle(stage_list)

    #build_map_play_with_AI.sokoban_play_with_AI(screen, stage_list, is_play_music)

# SCREEN MAP
def map(screen, level):
    # danh sách 10 button, mỗi button chứa [picture, picture_rect, text, text_rect, stage]
    buttons = []
    quantity = 10 
    create_buttons_map(buttons, quantity, level, user.score)
    
    back = pygame.image.load(c.icon_path+'back.png')
    back_rect = back.get_rect(topleft=(10,c.SCREEN_HEIGHT-back.get_height()))
    running = True
    hover = -1
    while running:
        draw_background(screen)
        draw_title(screen, 'MAP')
        create_buttons_map(buttons, quantity, level, user.score)
        # draw button
        for i in buttons:
            screen.blit(i[0], i[1]) # blit button
            screen.blit(i[2], i[3]) # blit text
        
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
                if hover != -1 and int(user.score[level*10 + hover]) != -1:
                    pygame.mixer.Sound(c.click_sound_path).play()           
                    sokoban(screen, buttons[hover][4], user, is_play_music)
                    hover = -1 # đặt lại hover mỗi lần load map
                if back_rect.collidepoint(event.pos):
                    pygame.mixer.Sound(c.click_sound_path).play()           
                    running = False
      
        pygame.display.update()
