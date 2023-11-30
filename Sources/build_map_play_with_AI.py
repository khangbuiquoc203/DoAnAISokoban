import pygame
import controls
import const as c
from enum import Enum
import os
import Algorithms as agr
import support_func as spf
import build_map
import sys
import User
import login
import threading

path_board = os.getcwd() + '\\..\\Testcases'
path_checkpoint = os.getcwd() + '\\..\\Checkpoints'
wall = pygame.image.load(os.getcwd() + '\\..\\Assets\\wall.png')
box = pygame.image.load(os.getcwd() + '\\..\\Assets\\box.png')
point = pygame.image.load(os.getcwd() + '\\..\\Assets\\point.png')
space = pygame.image.load(os.getcwd() + '\\..\\Assets\\space.png')
algorithm_list = ["BFS", "DFS", "ASTAR", "UCS", "GREEDY", "IDFS", "HILL", "BEAM", "LDFS"]
algorithm = algorithm_list[0]
list_board = []
algorithm_number = 0

class enum_of_control_game(Enum):
    PLAY = 0
    PAUSE = 1
    REPLAY = 2
    SOUND = 3
    HOME = 4
    ALGORITHM = 5
    
def sokoban_play_with_AI(screen, stage_list, is_play_music):
    stage_list[0] = 0
    player1 = pygame.image.load(os.getcwd() + '\\..\\Assets\\playerleft.png')
    player2 = pygame.image.load(os.getcwd() + '\\..\\Assets\\playerleft.png')
    control_game = [] #0: Play, 1: Pause, 2: Replay, 3: Sound, 4: Home, 5: Select algorithm
    create_control(control_game)
    running = True 
    is_pause = True
    global list_board
    global num_states_visited
    global algorithm_number
    global algorithm
    pygame.font.init()
    clock = pygame.time.Clock()
    moved_player1 = False
    moved_player2 = False
    
    new_board_player1 = []
    new_board_player2 = []
    player1_stage = 0
    player2_stage = 0
    
    maps = build_map.get_boards()  
    list_check_points = build_map.get_check_points()
    
    # Thiết lập thời gian ban đầu (tính theo mili giây)
    start_time = pygame.time.get_ticks()
    current_time = pygame.time.get_ticks()
    play_time = 0
    timer = 1000*60*5 # thời gian chơi
    while running:        
        login.draw_background(screen)
        if is_pause == False:
            # Handle time
            current_time = pygame.time.get_ticks()
            
            if control_game[enum_of_control_game.PAUSE.value].is_clicked():
                pygame.mixer.Sound(c.click_sound_path).play()
                is_pause = True
                play_time += (current_time-start_time)
                start_time = current_time
        
        for i in control_game:
            i.draw(screen)
        
        # draw timer, start_time + 1000 để time draw đúng 05:00
        controls.Label(c.font_title_path, "Time: "+convert_time_to_str(timer, current_time, start_time+1000, play_time), 
                                    size=45, color=c.TITLE_COLOR, location_topleft=(420,40)).draw(screen)
        controls.Label(c.font_title_path, "Map clear: "+str(player1_stage), size=30, color=c.TITLE_COLOR, location_topleft=(60,150)).draw(screen)
        controls.Label(c.font_title_path, "Map clear: "+str(player2_stage), size=30, color=c.TITLE_COLOR, location_topleft=(660,150)).draw(screen)
        
        if control_game[enum_of_control_game.PLAY.value].is_clicked():
            pygame.mixer.Sound(c.click_sound_path).play()
            if is_pause:
                is_pause = False
                start_time = pygame.time.get_ticks()
                print('SOLVE')
                if algorithm == "BFS": 
                    list_board = agr.BFS(maps[player1_stage], list_check_points[player1_stage])
                    num_states_visited = agr.number_states_visited()
                if algorithm == "ASTAR":
                    list_board = agr.ASTAR(maps[player1_stage], list_check_points[player1_stage])
                    num_states_visited = agr.number_states_visited()
                if algorithm == "GREEDY":
                    list_board = agr.GREEDY(maps[player1_stage], list_check_points[player1_stage])
                    num_states_visited = agr.number_states_visited()
                if algorithm == "UCS":
                    list_board = agr.UCS(maps[player1_stage], list_check_points[player1_stage])
                    num_states_visited = agr.number_states_visited()
                if algorithm == "IDFS": 
                    list_board = agr.IDFS(maps[player1_stage], list_check_points[player1_stage])
                    num_states_visited = agr.number_states_visited()
                if algorithm == "DFS": 
                    list_board = agr.DFS(maps[player1_stage], list_check_points[player1_stage])
                    num_states_visited = agr.number_states_visited()
                if algorithm == "LDFS": 
                    list_board = agr.LDFS(maps[player1_stage], list_check_points[player1_stage])
                    num_states_visited = agr.number_states_visited()
                if algorithm == "BEAM": 
                    list_board = agr.BEAM(maps[player1_stage], list_check_points[player1_stage], 1)
                    num_states_visited = agr.number_states_visited()
                if algorithm == "HILL": 
                    list_board = agr.HILL(maps[player1_stage], list_check_points[player1_stage])
                    num_states_visited = agr.number_states_visited()
                
                stateLenght = len(list_board[0]) if list_board != [] else 0
                
                AI_solving= True
                currentState = 0
                # Handle time
                current_time = pygame.time.get_ticks()
                listdirect = []
            
        if control_game[enum_of_control_game.REPLAY.value].is_clicked():
            pygame.mixer.Sound(c.click_sound_path).play()
            drawBoard(screen, maps[stage_list[player1_stage]], 1, player1)
            drawBoard(screen, maps[stage_list[player2_stage]], 2, player2)
            new_board_player1 = maps[stage_list[player1_stage]]
            new_board_player2 = maps[stage_list[player2_stage]]
            moved_player1 = False
            moved_player2 = False
            player1_stage = 0
            player2_stage = 0
            start_time = pygame.time.get_ticks()
            play_time = 0
            is_pause = False
            
        if control_game[enum_of_control_game.SOUND.value].is_clicked():
            pygame.mixer.Sound(c.click_sound_path).play()
            if is_play_music:
                is_play_music = False
                pygame.mixer.music.stop()
                control_game[enum_of_control_game.SOUND.value].text = pygame.image.load(c.icon_path+'SoundOff.png')
            else:
                is_play_music = True
                pygame.mixer.music.play(-1)
                control_game[enum_of_control_game.SOUND.value].text = pygame.image.load(c.icon_path+'SoundOn.png')
            
        if control_game[enum_of_control_game.HOME.value].is_clicked():
            pygame.mixer.Sound(c.click_sound_path).play()
            running = False
            
        if control_game[enum_of_control_game.ALGORITHM.value].is_clicked():
            pygame.mixer.Sound(c.click_sound_path).play()
            algorithm_number +=1
            if algorithm_number == (len(algorithm_list)):
                algorithm_number = 0
            algorithm = algorithm_list[algorithm_number]
            
            # Thay đổi text của button algorithm
            font = pygame.font.Font(c.font_text_path, c.TEXT_SIZE-3)
            control_game[5].text = font.render(str(algorithm), True, 'black')
            rect=control_game[5].text.get_rect(center=control_game[5].image_rect.center)
            rect.top-=5
            control_game[5].text_rect = rect
            
        
        if len(list_board) > 0 and AI_solving == True:
            clock.tick(5)
            new_list_board = list_board[0][1:]
            if currentState < len(new_list_board):
                nowpos = spf.find_position_player(new_board_player1)
                nextpos = spf.find_position_player(new_list_board[currentState])
                direct = spf.check_movement_direction(nowpos,nextpos)
                listdirect.append(direct)
                new_board_player1 = new_list_board[currentState]
                if direct == 'w':
                    player1 = pygame.image.load(c.assets_path + '\\playerup.png')
                if direct == 's':
                    player1 = pygame.image.load(c.assets_path + '\\playerdown.png')
                if direct == 'a':
                    player1 = pygame.image.load(c.assets_path + '\\playerleft.png')
                if direct == 'd':
                    player1 = pygame.image.load(c.assets_path + '\\playerright.png')
                pygame.mixer.Sound(c.assets_path + '\\movesound.wav').play()
                currentState = currentState + 1
                moved_player1 = True
            else:
                print("CLOCKTICK RESET")
                list_board=[]
                AI_solving == False
                clock.tick(120)
            
            
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and is_pause == False:
                if event.key == pygame.K_w:
                    temp_board = spf.move_in_1_direction(new_board_player1, 'U', list_check_points[stage_list[player1_stage]])  
                    if new_board_player1 != temp_board:
                        new_board_player1 = temp_board
                        moved_player1 = True
                    player1 = pygame.image.load(c.assets_path + 'playerup.png')
                    pygame.mixer.Sound(c.assets_path + 'movesound.wav').play()
                if event.key == pygame.K_a:
                    temp_board = spf.move_in_1_direction(new_board_player1, 'L', list_check_points[stage_list[player1_stage]])  
                    if new_board_player1 != temp_board:
                        new_board_player1 = temp_board
                        moved_player1 = True
                    player1 = pygame.image.load(c.assets_path + 'playerleft.png')
                    pygame.mixer.Sound(c.assets_path + 'movesound.wav').play()
                if event.key == pygame.K_s:
                    temp_board = spf.move_in_1_direction(new_board_player1, 'D', list_check_points[stage_list[player1_stage]])  
                    if new_board_player1 != temp_board:
                        new_board_player1 = temp_board
                        moved_player1 = True
                    player1 = pygame.image.load(c.assets_path + 'playerdown.png')
                    pygame.mixer.Sound(c.assets_path + 'movesound.wav').play()
                if event.key == pygame.K_d:
                    temp_board = spf.move_in_1_direction(new_board_player1, 'R', list_check_points[stage_list[player1_stage]])  
                    if new_board_player1 != temp_board:
                        new_board_player1 = temp_board
                        moved_player1 = True
                    player1 = pygame.image.load(c.assets_path + 'playerright.png')
                    pygame.mixer.Sound(c.assets_path + 'movesound.wav').play()
                    
                if event.key == pygame.K_UP:
                    temp_board = spf.move_in_1_direction(new_board_player2, 'U', list_check_points[stage_list[player2_stage]])  
                    if new_board_player2 != temp_board:
                        new_board_player2 = temp_board
                        moved_player2 = True
                    player2 = pygame.image.load(c.assets_path + 'playerup.png')
                    pygame.mixer.Sound(c.assets_path + 'movesound.wav').play()
                if event.key == pygame.K_LEFT:
                    temp_board = spf.move_in_1_direction(new_board_player2, 'L', list_check_points[stage_list[player2_stage]])  
                    if new_board_player2 != temp_board:
                        new_board_player2 = temp_board
                        moved_player2 = True
                    player2 = pygame.image.load(c.assets_path + 'playerleft.png')
                    pygame.mixer.Sound(c.assets_path + 'movesound.wav').play()
                if event.key == pygame.K_DOWN:
                    temp_board = spf.move_in_1_direction(new_board_player2, 'D', list_check_points[stage_list[player2_stage]])  
                    if new_board_player2 != temp_board:
                        new_board_player2 = temp_board
                        moved_player2 = True
                    player2 = pygame.image.load(c.assets_path + 'playerdown.png')
                    pygame.mixer.Sound(c.assets_path + 'movesound.wav').play()
                if event.key == pygame.K_RIGHT:
                    temp_board = spf.move_in_1_direction(new_board_player2, 'R', list_check_points[stage_list[player2_stage]])  
                    if new_board_player2 != temp_board:
                        new_board_player2 = temp_board
                        moved_player2 = True
                    player2 = pygame.image.load(c.assets_path + 'playerright.png')
                    pygame.mixer.Sound(c.assets_path + 'movesound.wav').play()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        if moved_player1 or moved_player2:
            drawBoard(screen, new_board_player1, 1, player1)
            drawBoard(screen, new_board_player2, 2, player2)
        else:
            drawBoard(screen, maps[stage_list[player1_stage]], 1, player1)
            drawBoard(screen, maps[stage_list[player2_stage]], 2, player2)
            new_board_player1 = maps[stage_list[player1_stage]]
            new_board_player2 = maps[stage_list[player2_stage]]
            
        pygame.display.update()
        
        if spf.check_win(new_board_player1, list_check_points[stage_list[player1_stage]]):
            player1_stage+=1
            drawBoard(screen, maps[stage_list[player1_stage]], 1, player1)
            drawBoard(screen, maps[stage_list[player2_stage]], 2, player2)
            new_board_player1 = maps[stage_list[player1_stage]]
            new_board_player2 = maps[stage_list[player2_stage]]
        elif spf.check_win(new_board_player2, list_check_points[stage_list[player2_stage]]):
            player2_stage+=1
            drawBoard(screen, maps[stage_list[player1_stage]], 1, player1)
            drawBoard(screen, maps[stage_list[player2_stage]], 2, player2)
            new_board_player1 = maps[stage_list[player1_stage]]
            new_board_player2 = maps[stage_list[player2_stage]]
            
        # handle endgame
        if (timer - (current_time-start_time-1000) - play_time)//1000 == 0:
            if player1_stage>player2_stage:
                menu(screen,'player 1', player1_stage)
            elif player1_stage<player2_stage:
                menu(screen,'player 2', player2_stage)
            else:
                menu(screen,'Draw', player2_stage)
            pygame.mixer.Sound(c.click_sound_path).play()
            drawBoard(screen, maps[player1_stage], 1, player1)
            drawBoard(screen, maps[player2_stage], 2, player2)
            new_board_player1 = maps[player1_stage]
            new_board_player2 = maps[player2_stage]
            moved_player1 = False
            moved_player2 = False
            start_time = current_time-1000
            play_time = 0
            is_pause = True
        
def drawBoard(screen, board, role, player):
    try:
        width = len(board[0])  
        height = len(board)   
        # kích thước cố định của board là 600px, lấy size này chia cho số box sẽ ra size của mỗi box
        base_location = 60 if role==1 else 660
        tile_size = c.BOARD_SIZE*0.8//width 

        # resize image
        resize_space = pygame.transform.scale(space, (tile_size, tile_size))
        resize_wall = pygame.transform.scale(wall, (tile_size, tile_size))
        resize_box = pygame.transform.scale(box, (tile_size, tile_size))
        resize_point = pygame.transform.scale(point, (tile_size, tile_size))
        resize_player = pygame.transform.scale(player, (tile_size, tile_size))

        # draw board
        for i in range(height):
            for j in range(width):
                screen.blit(resize_space, (j * tile_size + base_location, i * tile_size + 200))
                if board[i][j] == '#':
                    screen.blit(resize_wall, (j * tile_size + base_location, i * tile_size + 200))
                if board[i][j] == '$':
                    screen.blit(resize_box, (j * tile_size + base_location, i * tile_size + 200))
                if board[i][j] == '%':
                    screen.blit(resize_point, (j * tile_size + base_location, i * tile_size + 200))
                if board[i][j] == '@':
                    screen.blit(resize_player, (j * tile_size + base_location, i * tile_size + 200))
    except:
        return
    
def menu(screen, player_win, map_clear):
    pygame.mixer.Sound(c.assets_path + '\\winsound.mp3').play()
    menu = pygame.image.load(c.assets_path+'\\png\\menu.png')
    rect = menu.get_rect(center=(c.SCREEN_WIDTH//2,c.SCREEN_HEIGHT//2))
    
    # button
    btn_mark = pygame.image.load(c.icon_path+'Mark.png')
    rect_mark = btn_mark.get_rect(centerx=rect.centerx, centery=rect.centery+120)
    
    screen.blit(menu, rect)
    screen.blit(btn_mark, rect_mark)
    
    # label
    label1 = controls.Label(c.font_text_path, "Winner:", size=30, color=c.TITLE_COLOR, location_topleft=(rect.centerx-50,rect.centery-120))
    label1.text_rect.centerx = rect.centerx
    label1.draw(screen)

    label = controls.Label(c.font_text_path, player_win, size=45, color='white', location_topleft=(rect.centerx-100,rect.centery-50))
    label.text_rect.centerx = rect.centerx
    label.draw(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:     
                if rect_mark.collidepoint(event.pos):
                    running = False
        pygame.display.update()
    
def convert_time_to_str(timer, current_time, start_time, play_time):
    result = ''
    elapse_time = timer - (current_time-start_time) - play_time
    second = elapse_time//1000 
    minute = second//60
    second %= 60
    if minute<10:
        result+='0'+str(minute)+':'
    else:
        result+=str(minute)+':'
    
    if second<10:
        result+='0'+str(second)
    else:
        result+=str(second)
    return result
        
def create_control(control_game):
    icons = ['Play.png', 'Pause.png', 'Replay.png', 'SoundOn.png', 'Home.png']
    for i in range(5):
        image = pygame.image.load(c.png_path + "square.png")
        image_hover = pygame.image.load(c.png_path + 'hover_' + "square.png")
        image_rect = image.get_rect(center=(c.SCREEN_WIDTH//2, 200 + (image.get_height()+10)*i + 42))
        
        icon = pygame.image.load(c.icon_path + icons[i])
        icon_rect = icon.get_rect(center=image_rect.center)
        icon_rect.top -= 5
        
        control_game.append(controls.Button(image=image, image_rect=image_rect, text=icon, text_rect=icon_rect, image_hover=image_hover))
        
    image = pygame.image.load(c.png_path + "button.png")
    image = pygame.transform.scale(image, (image.get_width()*0.8, image.get_height()*0.8))
    image_hover = pygame.image.load(c.png_path + 'hover_' + "button.png")
    image_rect = image.get_rect(topleft=(60, 685))
    
    font = pygame.font.Font(c.font_text_path, c.TEXT_SIZE-3)
    text = font.render("BFS", True, 'black')
    text_rect = text.get_rect(center=image_rect.center)
    text_rect.top -= 5
    
    control_game.append(controls.Button(image=image, image_rect=image_rect, text=text, text_rect=text_rect, image_hover=image_hover))