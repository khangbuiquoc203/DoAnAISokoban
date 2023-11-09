import pygame
from pygame.locals import *
import sys
import const 
from build_map import *

def init():
    pygame.init()
    screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT)) 
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
        elif check == 2:
            print("success!")
            game(screen)


# LOGIN: 0: none, 1: quit, 2: success
def login(screen):
    active = None
    hover = None
    username = "phong"
    password = "123"
    while True:
        screen.fill('white')
        # control
        font_title = pygame.font.Font(None, 80)
        font_text = pygame.font.Font(None, 40)
        title = font_title.render("LOGIN", True, const.TEXT_COLOR)
        label_username = font_text.render("Enter username", True, const.TEXT_COLOR)
        label_password = font_text.render("Enter password", True, const.TEXT_COLOR)
        textbox_username = pygame.Rect(140,150,320,40)
        textbox_password = pygame.Rect(140,230,320,40)
        button_login = pygame.Rect(140, 280, 150, 40)
        button_exit = pygame.Rect(310, 280, 150, 40)
        text_login = font_text.render("Login", True, const.TEXT_COLOR)
        text_exit = font_text.render("Exit", True, const.TEXT_COLOR)
        
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                return 1
            if event.type == MOUSEBUTTONDOWN:
                if textbox_username.collidepoint(event.pos):
                    active = textbox_username
                elif textbox_password.collidepoint(event.pos):
                    active = textbox_password
                elif button_login.collidepoint(event.pos):
                    active = button_login
                elif button_exit.collidepoint(event.pos):
                    active = button_exit
                else:
                    active = None
            if event.type == MOUSEMOTION:
                if button_exit.collidepoint(event.pos):
                    hover = button_exit
                elif button_login.collidepoint(event.pos):
                    hover = button_login
                else:
                    hover = None
            if event.type == pygame.KEYDOWN:
                if active is not None:
                    if event.key == pygame.K_RETURN:
                        return check_login(username, password)
                    elif event.key == pygame.K_BACKSPACE:
                        if active == textbox_username:
                            username = username[:-1]
                        elif active == textbox_password:
                            password = password[:-1]
                    else:
                        if active == textbox_username:
                            username += event.unicode
                        elif active == textbox_password:
                            password += event.unicode

        # draw
        text_rect = title.get_rect()
        text_rect.center = (300, 60)
        screen.blit(title, text_rect)
        
        screen.blit(label_username, (140, 120))
        pygame.draw.rect(screen, const.TEXTBOX_COLOR, textbox_username, 2)
        
        screen.blit(label_password, (140, 200))
        pygame.draw.rect(screen, const.TEXTBOX_COLOR, textbox_password, 2)
        
        if active == textbox_username:
            pygame.draw.rect(screen, const.TEXTBOX_COLOR_ACTIVE, textbox_username, 2)
        elif active == textbox_password:
            pygame.draw.rect(screen, const.TEXTBOX_COLOR_ACTIVE, textbox_password, 2)
        elif active == button_login:
            return check_login(username, password)
        elif active == button_exit:
            return 1
        
        if hover == button_exit:
            pygame.draw.rect(screen, const.BUTTON_LOGIN_COLOR, button_login)
            pygame.draw.rect(screen, const.BUTTON_EXIT_COLOR_HOVER, button_exit)
        elif hover == button_login:
            pygame.draw.rect(screen, const.BUTTON_LOGIN_COLOR_HOVER, button_login)
            pygame.draw.rect(screen, const.BUTTON_EXIT_COLOR, button_exit)  
        else:      
            pygame.draw.rect(screen, const.BUTTON_LOGIN_COLOR, button_login)
            pygame.draw.rect(screen, const.BUTTON_EXIT_COLOR, button_exit)     
            
        text_rect = text_exit.get_rect()
        text_rect.center = button_exit.center
        screen.blit(text_exit, text_rect)

        text_rect = text_login.get_rect()
        text_rect.center = button_login.center
        screen.blit(text_login, text_rect)    
        
        user_text = font_text.render(username, True, 'black')
        pass_text = font_text.render(password, True, 'black')
        
        screen.blit(user_text, (textbox_username.x + 5, textbox_username.y + 5))
        screen.blit(pass_text, (textbox_password.x + 5, textbox_password.y + 5))  
        # update
        pygame.display.update()

def check_login(user, password):
    if user == "phong" and password == "123":
        return 2
    else:
        return 0
    
# GAME
def game(screen):
    hover = active = None
    while True:
        screen.fill('white')
        font_title = pygame.font.Font(None, 80)
        font_text = pygame.font.Font(None, 40)
        
        # control
        title = font_title.render('SOKOBAN', True, const.TEXT_COLOR)
        
        list_text = ["PLAY", "SCORE", "OPTION", "QUIT"]
        list_text_control = []
        for i in range(4):
            text = font_text.render(list_text[i], True, const.TEXT_COLOR)
            list_text_control.append(text)
        
        list_button_control = []
        for i in range(4):
            button = pygame.Rect(const.BUTTON_BASE_X, const.BUTTON_BASE_Y + i*(const.BUTTON_HEIGHT + 10), const.BUTTON_WIDTH, const.BUTTON_HEIGHT)
            list_button_control.append(button)
        
        # draw
        text_rect = title.get_rect()
        text_rect.center = (const.SCREEN_WIDTH//2, 80)
        screen.blit(title, text_rect)
        
        for i in range(4):
            pygame.draw.rect(screen, const.BUTTON_COLOR, list_button_control[i])
        
        if hover == list_button_control[0]:
            pygame.draw.rect(screen, const.BUTTON_COLOR_HOVER, list_button_control[0])
        elif hover == list_button_control[1]:
            pygame.draw.rect(screen, const.BUTTON_COLOR_HOVER, list_button_control[1])
        elif hover == list_button_control[2]:
            pygame.draw.rect(screen, const.BUTTON_COLOR_HOVER, list_button_control[2])
        elif hover == list_button_control[3]:
            pygame.draw.rect(screen, const.BUTTON_COLOR_HOVER, list_button_control[3])
        
        for i in range(4):
            text = list_text_control[i]
            text_rect = text.get_rect()
            text_rect.center = list_button_control[i].center
            screen.blit(text, text_rect)
        
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEMOTION:
                if list_button_control[0].collidepoint(event.pos):
                    hover = list_button_control[0]
                elif list_button_control[1].collidepoint(event.pos):
                    hover = list_button_control[1]
                elif list_button_control[2].collidepoint(event.pos):
                    hover = list_button_control[2]
                elif list_button_control[3].collidepoint(event.pos):
                    hover = list_button_control[3]
                else:
                    hover = None
            if event.type == MOUSEBUTTONDOWN:
                active = hover
                
        if active == list_button_control[0]:
            play(screen)
            active = None
        elif active == list_button_control[1]:
            score(screen)
            active = None
        elif active == list_button_control[2]:
            option(screen)
            active = None
        elif active == list_button_control[3]:
            quit()
            
        pygame.display.update()

def quit():
    pygame.quit()
    sys.exit()
    
def play(screen):
    hover = active = None
    running = True
    while running:
        screen.fill('white')
        font_title = pygame.font.Font(None, 80)
        font_text = pygame.font.Font(None, 40)
        
        # control
        title = font_title.render('SOKOBAN', True, const.TEXT_COLOR)
        
        list_text = ["1 PLAYER", "2 PLAYER", "MACHINE", "BACK"]
        list_text_control = []
        for i in range(4):
            text = font_text.render(list_text[i], True, const.TEXT_COLOR)
            list_text_control.append(text)
        
        list_button_control = []
        for i in range(4):
            button = pygame.Rect(const.BUTTON_BASE_X, const.BUTTON_BASE_Y + i*(const.BUTTON_HEIGHT + 10), const.BUTTON_WIDTH, const.BUTTON_HEIGHT)
            list_button_control.append(button)
        
        # draw
        text_rect = title.get_rect()
        text_rect.center = (const.SCREEN_WIDTH//2, 80)
        screen.blit(title, text_rect)
        
        for i in range(4):
            pygame.draw.rect(screen, const.BUTTON_COLOR, list_button_control[i])
        
        if hover == list_button_control[0]:
            pygame.draw.rect(screen, const.BUTTON_COLOR_HOVER, list_button_control[0])
        elif hover == list_button_control[1]:
            pygame.draw.rect(screen, const.BUTTON_COLOR_HOVER, list_button_control[1])
        elif hover == list_button_control[2]:
            pygame.draw.rect(screen, const.BUTTON_COLOR_HOVER, list_button_control[2])
        elif hover == list_button_control[3]:
            pygame.draw.rect(screen, const.BUTTON_COLOR_HOVER, list_button_control[3])
        
        for i in range(4):
            text = list_text_control[i]
            text_rect = text.get_rect()
            text_rect.center = list_button_control[i].center
            screen.blit(text, text_rect)
        
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEMOTION:
                if list_button_control[0].collidepoint(event.pos):
                    hover = list_button_control[0]
                elif list_button_control[1].collidepoint(event.pos):
                    hover = list_button_control[1]
                elif list_button_control[2].collidepoint(event.pos):
                    hover = list_button_control[2]
                elif list_button_control[3].collidepoint(event.pos):
                    hover = list_button_control[3]
                else:
                    hover = None
            if event.type == MOUSEBUTTONDOWN:
                active = hover
                
        if active == list_button_control[0]:
            player_1(screen)
            active=None
        elif active == list_button_control[1]:
            player_2(screen)
            active=None
        elif active == list_button_control[2]:
            machine(screen)
            active=None
        elif active == list_button_control[3]:
            running = False
            
        pygame.display.update()
    
def score(screen):
    print('score')
    
def option(screen):
    print('option')
    
def player_1(screen):
    hover = active = None
    running = True
    while running:
        list_text = ["EASY", "MEDIUM", "HARD", "BACK"]
        list_button_control = []
        draw1(screen, list_text, list_button_control, hover, active)
        
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEMOTION:
                if list_button_control[0].collidepoint(event.pos):
                    hover = list_button_control[0]
                elif list_button_control[1].collidepoint(event.pos):
                    hover = list_button_control[1]
                elif list_button_control[2].collidepoint(event.pos):
                    hover = list_button_control[2]
                elif list_button_control[3].collidepoint(event.pos):
                    hover = list_button_control[3]
                else:
                    hover = None
            if event.type == MOUSEBUTTONDOWN:
                active = hover
        
        if active == list_button_control[0]:
            easy(screen)
            active = None
        elif active == list_button_control[1]:
            medium(screen)
            active = None
        elif active == list_button_control[2]:
            hard(screen)
            active = None
        elif active == list_button_control[3]:
            running = False
        
        pygame.display.update()
    
def player_2(screen):
    hover = active = None
    running = True
    while running:
        list_text = ["EASY", "MEDIUM", "HARD", "BACK"]
        list_button_control = []
        draw1(screen, list_text, list_button_control, hover, active)
        
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEMOTION:
                if list_button_control[0].collidepoint(event.pos):
                    hover = list_button_control[0]
                elif list_button_control[1].collidepoint(event.pos):
                    hover = list_button_control[1]
                elif list_button_control[2].collidepoint(event.pos):
                    hover = list_button_control[2]
                elif list_button_control[3].collidepoint(event.pos):
                    hover = list_button_control[3]
                else:
                    hover = None
            if event.type == MOUSEBUTTONDOWN:
                active = hover
        
        if active == list_button_control[0]:
            easy(screen)
            active = None
        elif active == list_button_control[1]:
            medium(screen)
            active = None
        elif active == list_button_control[2]:
            hard(screen)
            active = None
        elif active == list_button_control[3]:
            running = False
        
        pygame.display.update()
    
def machine(screen):
    hover = active = None
    running = True
    while running:
        list_text = ["EASY", "MEDIUM", "HARD", "BACK"]
        list_button_control = []
        draw1(screen, list_text, list_button_control, hover, active)
        
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEMOTION:
                if list_button_control[0].collidepoint(event.pos):
                    hover = list_button_control[0]
                elif list_button_control[1].collidepoint(event.pos):
                    hover = list_button_control[1]
                elif list_button_control[2].collidepoint(event.pos):
                    hover = list_button_control[2]
                elif list_button_control[3].collidepoint(event.pos):
                    hover = list_button_control[3]
                else:
                    hover = None
            if event.type == MOUSEBUTTONDOWN:
                active = hover
        
        if active == list_button_control[0]:
            easy(screen)
            active = None
        elif active == list_button_control[1]:
            medium(screen)
            active = None
        elif active == list_button_control[2]:
            hard(screen)
            active = None
        elif active == list_button_control[3]:
            running = False
        
        pygame.display.update()

def draw1(screen, list_text, list_button_control, hover, active):
    screen.fill('white')
    font_title = pygame.font.Font(None, 80)
    font_text = pygame.font.Font(None, 40)
    # control
    title = font_title.render('SOKOBAN', True, const.TEXT_COLOR)
    list_text_control = []
    for i in range(4):
        text = font_text.render(list_text[i], True, const.TEXT_COLOR)
        list_text_control.append(text)
    for i in range(4):
        button = pygame.Rect(const.BUTTON_BASE_X, const.BUTTON_BASE_Y + i*(const.BUTTON_HEIGHT + 10), const.BUTTON_WIDTH, const.BUTTON_HEIGHT)
        list_button_control.append(button)
    # draw
    text_rect = title.get_rect()
    text_rect.center = (const.SCREEN_WIDTH//2, 80)
    screen.blit(title, text_rect)
    for i in range(4):
        pygame.draw.rect(screen, const.BUTTON_COLOR, list_button_control[i])
        
    if hover == list_button_control[0]:
        pygame.draw.rect(screen, const.BUTTON_COLOR_HOVER, list_button_control[0])
    elif hover == list_button_control[1]:
        pygame.draw.rect(screen, const.BUTTON_COLOR_HOVER, list_button_control[1])
    elif hover == list_button_control[2]:
        pygame.draw.rect(screen, const.BUTTON_COLOR_HOVER, list_button_control[2])
    elif hover == list_button_control[3]:
        pygame.draw.rect(screen, const.BUTTON_COLOR_HOVER, list_button_control[3])
    
    for i in range(4):
        text = list_text_control[i]
        text_rect = text.get_rect()
        text_rect.center = list_button_control[i].center
        screen.blit(text, text_rect)
            
def easy(screen):
    hover = active = None
    running = True
    while running:
        list_control = [] # text, button, centerX, centerY
        running = draw2(screen, list_control, hover, active) 
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEMOTION:
                is_None = True
                for i in list_control:
                    if i[1].collidepoint(event.pos):
                        hover = i
                        is_None = False
                if is_None:
                    hover = None
            if event.type == MOUSEBUTTONDOWN:
                if hover != None:
                    active = hover
                    if(active[3]==75):
                        stage = (active[2]//100)-1
                        sokoban(stage)
                    if(active[3]==175):
                        stage = (active[2]//100)+5-1
                        sokoban(stage)
                    

        
        # active
        if active != None:
            if active[1] == list_control[-1][1]:
                running = False
        pygame.display.update()

def medium(screen):
    hover = active = None
    running = True
    while running:
        list_control = [] # text, button, centerX, centerY
        running = draw2(screen, list_control, hover, active) 
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEMOTION:
                is_None = True
                for i in list_control:
                    if i[1].collidepoint(event.pos):
                        hover = i
                        is_None = False
                if is_None:
                    hover = None
            if event.type == MOUSEBUTTONDOWN:
                if hover != None:
                    active = hover
                if(active[3]==75):
                    stage = (active[2]//100)+10-1
                    sokoban(stage)
                if(active[3]==175):
                    stage = (active[2]//100)+15-1
                    sokoban(stage)
        
        # active
        if active != None:
            if active[1] == list_control[-1][1]:
                running = False
        pygame.display.update()
        
def hard(screen):
    hover = active = None
    running = True
    while running:
        list_control = [] # text, button, centerX, centerY
        running = draw2(screen, list_control, hover, active) 
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEMOTION:
                is_None = True
                for i in list_control:
                    if i[1].collidepoint(event.pos):
                        hover = i
                        is_None = False
                if is_None:
                    hover = None
            if event.type == MOUSEBUTTONDOWN:
                if hover != None:
                    active = hover
                if(active[3]==75):
                    stage = (active[2]//100)+20-1
                    sokoban(stage)
                if(active[3]==175):
                    stage = (active[2]//100)+25-1
                    sokoban(stage)
        
        # active
        if active != None:
            if active[1] == list_control[-1][1]:
                running = False
        pygame.display.update()

def draw2(screen, list_control, hover, active):
    screen.fill('white')
    font_text = pygame.font.Font(None, 40)
    font_text2 = pygame.font.Font(None, 30)
    
    i = 1
    for row in range(2):
        for col in range(5):
            button = pygame.Rect(const.BUTTON_MAP_X+(col*100), const.BUTTON_MAP_Y+(row*100), const.BUTTON_MAP_SIZE, const.BUTTON_MAP_SIZE)
            pygame.draw.rect(screen, const.BUTTON_COLOR, button)
            
            text = font_text.render(str(i), True, const.TEXT_COLOR)
            text_rect = text.get_rect()
            text_rect.center = (const.BUTTON_MAP_X+(col*100)+45, const.BUTTON_MAP_Y+(row*100)+45)
            screen.blit(text, text_rect)
            i += 1
            
            data = [text, button, const.BUTTON_MAP_X+(col*100)+45, const.BUTTON_MAP_Y+(row*100)+45]
            list_control.append(data)
    
    # button back
    button_back = pygame.Rect(10, 350, 80, 40)
    pygame.draw.rect(screen, const.BUTTON_COLOR, button_back)
    text_back = font_text2.render('BACK', True, const.TEXT_COLOR)
    text_rect = text_back.get_rect()
    text_rect.center = button_back.center
    screen.blit(text_back, text_rect)
    list_control.append([text_back, button_back, 10 + 80/2, 350 + 40/2])

    # hover
    if hover != None:
        pygame.draw.rect(screen, const.BUTTON_COLOR_HOVER, hover[1])
        text_rect = hover[0].get_rect()
        text_rect.center = (hover[2], hover[3])
        screen.blit(hover[0], text_rect)
    
    return True