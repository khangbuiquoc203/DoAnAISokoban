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
        else:
            print("success!\nHello",check)
            game(screen, check)

def draw_background(screen):
    assets_path = os.getcwd() + "\\..\\Assets\\init_background.png"
    background = pygame.image.load(assets_path)
    background = pygame.transform.scale(background, (const.SCREEN_WIDTH,const.SCREEN_HEIGHT))
    screen.blit(background, (0,0))
    font_title = pygame.font.Font(None, 80)
    
    # control
    title = font_title.render('SOKOBAN', True, const.TEXT_COLOR)
    
    # draw
    text_rect = title.get_rect()
    text_rect.center = (const.SCREEN_WIDTH//2, 80)
    screen.blit(title, text_rect)

# LOGIN: 0: none, 1: quit, 2: success
def login(screen):
    active = None
    username = ""
    while True:
        assets_path = os.getcwd() + "\\..\\Assets\\init_background.png"
        background = pygame.image.load(assets_path)
        background = pygame.transform.scale(background, (const.SCREEN_WIDTH,const.SCREEN_HEIGHT))
        screen.blit(background, (0,0))
        # title
        font_title = pygame.font.Font(None, 80)
        title = font_title.render("LOGIN", True, const.TEXT_COLOR)
        text_rect = title.get_rect()
        text_rect.center = (300, 60)
        screen.blit(title, text_rect)
        
        # label
        font_text = pygame.font.Font(None, 40)
        label_username = font_text.render("Enter username", True, const.TEXT_COLOR)
        screen.blit(label_username, (140, 120))
        
        # textbox
        textbox_username = pygame.Rect(140,150,320,40)
        pygame.draw.rect(screen, const.TEXTBOX_COLOR, textbox_username, 2)
        
        # button
        button_login = pygame.image.load(const.asset_button_path + "\\login.png")
        button_quit = pygame.image.load(const.asset_button_path + "\\login_quit.png")
        
        screen.blit(button_login, (160,200))
        screen.blit(button_quit, (330,200))
        
        button_login_rect = button_login.get_rect(topleft=(160,200))
        button_quit_rect = button_quit.get_rect(topleft=(330,200))
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                return 1
            if event.type == MOUSEBUTTONDOWN:
                if textbox_username.collidepoint(event.pos):
                    active = textbox_username
                elif button_login_rect.collidepoint(event.pos):
                    return check_login(username)
                elif button_quit_rect.collidepoint(event.pos):
                    return 1
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
            pygame.draw.rect(screen, const.TEXTBOX_COLOR_ACTIVE, textbox_username, 2)
        
        user_text = font_text.render(username, True, 'white')
        
        screen.blit(user_text, (textbox_username.x + 5, textbox_username.y + 5))
        # update
        pygame.display.update()

def check_login(user):
    list_user = []
    with open(const.asset_button_path+"\\user.txt", 'r') as file:
        list_user = file.readlines()
    
    for i in list_user:
        if user == i:
            return user
    
    list_user.append(user+"\n")
    
    with open(const.asset_button_path+"\\user.txt", 'w') as file:
        file.writelines(list_user)
        return user
    
    
# GAME
def game(screen, user):
    while True:
        draw_background(screen)
        
        image_name = ["\\play.png","\\score.png","\\option.png","\\quit.png"]
        image = []
        image_rect = []
        image_location = []
        for i in range(4):
            image.append(pygame.image.load(const.asset_button_path + image_name[i]))
            image_location.append((const.BUTTON_BASE_X, const.BUTTON_BASE_Y + i*(const.BUTTON_HEIGHT + 10)))
            image_rect.append(image[i].get_rect(topleft=image_location[i]))
            screen.blit(image[i], image_location[i])
            
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                if image_rect[0].collidepoint(event.pos):
                    play(screen)
                elif image_rect[1].collidepoint(event.pos):
                    score(screen)
                elif image_rect[2].collidepoint(event.pos):
                    option(screen)
                elif image_rect[3].collidepoint(event.pos):
                    quit()
                
            
        pygame.display.update()

def quit():
    pygame.quit()
    sys.exit()
    
def play(screen):
    running = True
    while running:
        draw_background(screen)
        
        image_name = ["\\1_player.png","\\2_player.png","\\machine.png","\\back.png"]
        image = []
        image_rect = []
        image_location = []
        for i in range(4):
            image.append(pygame.image.load(const.asset_button_path + image_name[i]))
            image_location.append((const.BUTTON_BASE_X, const.BUTTON_BASE_Y + i*(const.BUTTON_HEIGHT + 10)))
            image_rect.append(image[i].get_rect(topleft=image_location[i]))
            screen.blit(image[i], image_location[i])
        
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                if image_rect[0].collidepoint(event.pos):
                    player_1(screen)
                elif image_rect[1].collidepoint(event.pos):
                    player_2(screen)
                elif image_rect[2].collidepoint(event.pos):
                    machine(screen)
                elif image_rect[3].collidepoint(event.pos):
                    running=False
            
        pygame.display.update()
    
def score(screen):
    print('score')
    
def option(screen):
    print('option')
    
def player_1(screen):
    running = True
    while running:
        draw_background(screen)
        
        image_name = ["\\easy.png","\\medium.png","\\hard.png","\\back.png"]
        image = []
        image_rect = []
        image_location = []
        for i in range(4):
            image.append(pygame.image.load(const.asset_button_path + image_name[i]))
            image_location.append((const.BUTTON_BASE_X, const.BUTTON_BASE_Y + i*(const.BUTTON_HEIGHT + 10)))
            image_rect.append(image[i].get_rect(topleft=image_location[i]))
            screen.blit(image[i], image_location[i])
            
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                if image_rect[0].collidepoint(event.pos):
                    easy(screen)
                elif image_rect[1].collidepoint(event.pos):
                    medium(screen)
                elif image_rect[2].collidepoint(event.pos):
                    hard(screen)
                elif image_rect[3].collidepoint(event.pos):
                    running=False
            
        pygame.display.update()
    
def player_2(screen):
    running = True
    while running:
        draw_background(screen)
        
        image_name = ["\\easy.png","\\medium.png","\\hard.png","\\back.png"]
        image = []
        image_rect = []
        image_location = []
        for i in range(4):
            image.append(pygame.image.load(const.asset_button_path + image_name[i]))
            image_location.append((const.BUTTON_BASE_X, const.BUTTON_BASE_Y + i*(const.BUTTON_HEIGHT + 10)))
            image_rect.append(image[i].get_rect(topleft=image_location[i]))
            screen.blit(image[i], image_location[i])
            
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                if image_rect[0].collidepoint(event.pos):
                    easy(screen)
                elif image_rect[1].collidepoint(event.pos):
                    medium(screen)
                elif image_rect[2].collidepoint(event.pos):
                    hard(screen)
                elif image_rect[3].collidepoint(event.pos):
                    running=False
            
        pygame.display.update()
    
def machine(screen):
    running = True
    while running:
        draw_background(screen)
        
        image_name = ["\\easy.png","\\medium.png","\\hard.png","\\back.png"]
        image = []
        image_rect = []
        image_location = []
        for i in range(4):
            image.append(pygame.image.load(const.asset_button_path + image_name[i]))
            image_location.append((const.BUTTON_BASE_X, const.BUTTON_BASE_Y + i*(const.BUTTON_HEIGHT + 10)))
            image_rect.append(image[i].get_rect(topleft=image_location[i]))
            screen.blit(image[i], image_location[i])
            
        # event
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                if image_rect[0].collidepoint(event.pos):
                    easy(screen)
                elif image_rect[1].collidepoint(event.pos):
                    medium(screen)
                elif image_rect[2].collidepoint(event.pos):
                    hard(screen)
                elif image_rect[3].collidepoint(event.pos):
                    running=False
            
        pygame.display.update()

def easy(screen):
    hover = active = None
    running = True
    while running:
        list_control = [] # text, button, centerX, centerY
        running = draw_listmap(screen, list_control, hover, active) 
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
        running = draw_listmap(screen, list_control, hover, active) 
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
        running = draw_listmap(screen, list_control, hover, active) 
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

def draw_listmap(screen, list_control, hover, active):
    assets_path = os.getcwd() + "\\..\\Assets\\init_background.png"
    background = pygame.image.load(assets_path)
    background = pygame.transform.scale(background, (const.SCREEN_WIDTH,const.SCREEN_HEIGHT))
    screen.blit(background, (0,0))
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