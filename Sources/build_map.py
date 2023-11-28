import numpy as np
import User
import os
import pygame
import re
import controls
import support_func as spf
import ctypes
import const as c
import sys
import Algorithms as agr
import keyboard
from enum import Enum
'''
//========================//
//         PYGAME         //
//     INITIALIZATIONS    //
//========================//
'''
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1200, 760))
pygame.display.set_caption('Sokoban Game')
BACKGROUND = (0, 0, 0) #BLACK
WHITE = (255, 255, 255)
#text_font=pygame.font.Font("Arial",30)
list_board = []
algorithm_number = 0
algorithm_list = ["BFS", "DFS", "ASTAR", "UCS", "GREEDY", "IDFS", "Hill", "BEAM", "LDFS"]
num_states_visited = 0
'''
//========================//
//    GET SOME ASSETS     //
//========================//
'''
backward_path = os.getcwd() + "\\..\\Backward"
assets_path = os.getcwd() + "\\..\\Assets"
os.chdir(assets_path)
player = pygame.image.load(os.getcwd() + '\\playerleft.png')
wall = pygame.image.load(os.getcwd() + '\\wall.png')
box = pygame.image.load(os.getcwd() + '\\box.png')
point = pygame.image.load(os.getcwd() + '\\point.png')
space = pygame.image.load(os.getcwd() + '\\space.png')
init_background = pygame.image.load(os.getcwd() + '\\init_background.png')
icon_image  = pygame.image.load(os.getcwd() + '\\icon_image.png')

text_font=pygame.font.Font(os.getcwd() + '\\game.ttf',45)
textsmall_font=pygame.font.Font(os.getcwd() + '\\game.ttf',30)



'''
//============================//
//     GET THE TESTCASES      //
//    AND CHECKPOINTS PATH    //
//           FOLDERS          //
//============================//
'''
path_board = os.getcwd() + '\\..\\Testcases'
path_checkpoint = os.getcwd() + '\\..\\Checkpoints'


''' 
//==========================================//
//     READ A SINGLE CHECKPOINT TXT FILE    //
//==========================================//
'''
def get_pair(path):
    result = np.loadtxt(f"{path}", dtype=int, delimiter=',')
    return result

'''
//==========================================//
//          TRAVERSE CHECKPOINT FILES       //
//      AND RETURN A SET OF CHECKPOINT      //
//==========================================//
'''
def get_check_points():
    os.chdir(path_checkpoint)
    list_check_point = []
    for file in sorted(os.listdir(), key=get_number):
        if file.endswith(".txt"):
            file_path = f"{path_checkpoint}\{file}"
            check_point = get_pair(file_path)
            list_check_point.append(check_point)
    return list_check_point


def get_number (file): 
    match = re.search ('(\d+)', file) 
    if match:
        return int (match.group(1)) 
    else: 
        return 0
    
'''
//============================//
//         DRAW TEXT          //
//============================//
'''
def draw_text(text, font, text_col, x, y):
    img=font.render(text, True, text_col)
    screen.blit(img, (x,y))

''' 
//==============================//
//    TRAVERSE TESTCASE FILES   //
//   AND RETURN A SET OF BOARD  //
//==============================//
'''
def get_boards():
    os.chdir(path_board)
    list_boards = []
    for file in sorted(os.listdir(), key=get_number):
        if file.endswith(".txt"):
            file_path = f"{path_board}\{file}"
            board = get_board(file_path)
            list_boards.append(board)
    return list_boards

'''
//==========================================//
//      READ A SINGLE TESTCASE TXT FILE     //
//==========================================//
'''
def get_board(path):
    result = np.loadtxt(f"{path}", dtype=str, delimiter=',')
    for row in result:
        format_row(row)
    return result.tolist()

'''
//===========================//
//      FORMAT THE INPUT     //
//    TESTCASESE TXT FILE    //
//===========================//
'''
def format_row(row):
    for i in range(len(row)):
        if row[i] == '1':
            row[i] = '#'
        elif row[i] == 'p':
            row[i] = '@'
        elif row[i] == 'b':
            row[i] = '$'
        elif row[i] == 'c':
            row[i] = '%'


'''
Vẽ board ra màn hình
Kích thước width cố định của board là 600px, từ đó suy ra kích thước 1 box
Height phụ thuộc vào box đã đc tính
'''
# Draw board
def drawBoard(board):
    try:
        width = len(board[0])  
        height = len(board)   
        # kích thước cố định của board là 600px, lấy size này chia cho số box sẽ ra size của mỗi box
        tile_size = c.BOARD_SIZE//width 

        # resize image
        resize_space = pygame.transform.scale(space, (tile_size, tile_size))
        resize_wall = pygame.transform.scale(wall, (tile_size, tile_size))
        resize_box = pygame.transform.scale(box, (tile_size, tile_size))
        resize_point = pygame.transform.scale(point, (tile_size, tile_size))
        resize_player = pygame.transform.scale(player, (tile_size, tile_size))

        # draw board
        for i in range(height):
            for j in range(width):
                screen.blit(resize_space, (j * tile_size + c.BOARD_LOCATION_X, i * tile_size + c.BOARD_LOCATION_Y))
                if board[i][j] == '#':
                    screen.blit(resize_wall, (j * tile_size + c.BOARD_LOCATION_X, i * tile_size + c.BOARD_LOCATION_Y))
                if board[i][j] == '$':
                    screen.blit(resize_box, (j * tile_size + c.BOARD_LOCATION_X, i * tile_size + c.BOARD_LOCATION_Y))
                if board[i][j] == '%':
                    screen.blit(resize_point, (j * tile_size + c.BOARD_LOCATION_X, i * tile_size + c.BOARD_LOCATION_Y))
                if board[i][j] == '@':
                    screen.blit(resize_player, (j * tile_size + c.BOARD_LOCATION_X, i * tile_size + c.BOARD_LOCATION_Y))
    except:
        return

''' VARIABLE '''
algorithm = algorithm_list[0]

''' Controls '''
def create_control_game(control_game, control_info):
    imgs = ["button.png", "square.png", "square.png", "square.png", "square.png", "square.png", "square.png" ]

    texts = []
    font = pygame.font.Font(c.font_text_path, c.TEXT_SIZE-3)
    texts.append(font.render("BFS", True, 'black'))
    icon_play = pygame.image.load(c.icon_path + 'Play.png')
    icon_pause = pygame.image.load(c.icon_path + 'Pause.png')
    texts.append(icon_play)
    texts.append(icon_pause)

    for i in range(3):    
        image = pygame.image.load(c.png_path + imgs[i])
        image_hover = pygame.image.load(c.png_path + 'hover_' + imgs[i])
        if len(control_game) != 0:
            location_x = control_game[i-1].image.get_width() + control_game[i-1].image_rect.left + 20
        else:
            location_x = 60
        image_rect = image.get_rect(topleft=(location_x, 120))
        text_rect = texts[i].get_rect(center=image_rect.center)
        text_rect.top -= 5
        
        control_game.append(controls.Button(image=image, image_rect=image_rect, text=texts[i], text_rect=text_rect, image_hover=image_hover))
    icons = [ "Home.png", "Replay.png", "Undo.png", "SoundOn.png"]
    for i in range(4):
        image = pygame.image.load(c.png_path + imgs[i+3])
        image_hover = pygame.image.load(c.png_path + 'hover_' + imgs[i+3])
        
        image_rect = image.get_rect(topleft=(60 + (22+image.get_width())*i, c.SCREEN_HEIGHT - image.get_height() - 40))
        
        icon = pygame.image.load(c.icon_path + icons[i])
        icon_rect = icon.get_rect(center=image_rect.center)
        icon_rect.top -= 5
        
        control_game.append(controls.Button(image=image, image_rect=image_rect, text=icon, text_rect=icon_rect, image_hover=image_hover))
    
    # Infomation    
    control_info.append(controls.Label(c.font_title_path, "Lv: 0", size=38, color=c.TITLE_COLOR, location_topleft=(60,20)))
    control_info.append(controls.Label(c.font_title_path, "Move: 0", size=38, color=c.TITLE_COLOR, location_topleft=(540,20)))
    control_info.append(controls.Label(c.font_title_path, "Time: 0", size=38, color=c.TITLE_COLOR, location_topleft=(850,20)))

class enum_of_control_game(Enum):
    ALGORITHM = 0
    PLAY = 1
    PAUSE = 2
    HOME = 3
    REPLAY = 4
    UNDO = 5
    SOUND =6

''' 
//===========================//
//      SOKOBAN FUNCTION     //
//===========================//
'''
def sokoban(screen, stage, user):
    control_game = [] #0: algorithm, 1: play, 2: pause, 3: home, 4: replay, 5: undo, 6: sound
    control_info = [] #0: lv, 1: move, 2: time
    create_control_game(control_game, control_info)
    
    running = True 
    global algorithm
    global player
    global list_board
    global algorithm_number
    global num_states_visited
    pygame.font.init()
    clock = pygame.time.Clock()
    moved = False
    new_board = []
    backward_matrix = []
    stateLenght = 0
    AI_solving = False
    currentState = 0
    
    # Thiết lập thời gian ban đầu (tính theo mili giây)
    start_time = pygame.time.get_ticks()
    elapsed_time = 0
    # Move
    move_count = 0
    while running:     
        # Draw stage
        control_info[0] = controls.Label(c.font_title_path, "Lv: "+str(stage+1), size=38, color=c.TITLE_COLOR, location_topleft=(60,20))
        # Handle time
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        seconds = elapsed_time // 1000
        control_info[2] = controls.Label(c.font_title_path, "Time: "+str(seconds//60)+":"+str(seconds%60), size=38, color=c.TITLE_COLOR, location_topleft=(850,20))
        screen.blit(init_background, (0, 0))
        pygame.display.set_icon(icon_image)
        # Handle move
        control_info[1] = controls.Label(c.font_title_path, "Move: "+str(move_count), size=38, color=c.TITLE_COLOR, location_topleft=(540,20))
        
        # draw control
        for i in control_info:
            i.draw(screen)
            
        for i in control_game:
            i.draw(screen)
        pygame.draw.rect(screen, 'white', pygame.Rect(60, 220, 400, 360))
        
        #display(stage)
        #draw_text("State visited: " + str(num_states_visited), textsmall_font, (255, 255, 255), 700, 15)
        #draw_text("Solve step: " + str(stateLenght), textsmall_font, (255, 255, 255), 700, 50)
        if control_game[1].is_clicked():
            pygame.mixer.Sound(c.click_sound_path).play()
            start_time = pygame.time.get_ticks()
            print('SOLVE')
            if algorithm == "BFS": 
                list_board = agr.BFS(maps[stage], list_check_points[stage])
                num_states_visited = agr.number_states_visited()
            if algorithm == "ASTAR":
                list_board = agr.ASTAR(maps[stage], list_check_points[stage])
                num_states_visited = agr.number_states_visited()
            if algorithm == "GREEDY":
                list_board = agr.GREEDY(maps[stage], list_check_points[stage])
                num_states_visited = agr.number_states_visited()
            if algorithm == "UCS":
                list_board = agr.UCS(maps[stage], list_check_points[stage])
                num_states_visited = agr.number_states_visited()
            if algorithm == "IDFS": 
                list_board = agr.IDFS(maps[stage], list_check_points[stage])
                num_states_visited = agr.number_states_visited()
            if algorithm == "DFS": 
                list_board = agr.DFS(maps[stage], list_check_points[stage])
                num_states_visited = agr.number_states_visited()
            if algorithm == "LDFS": 
                list_board = agr.LDFS(maps[stage], list_check_points[stage])
                num_states_visited = agr.number_states_visited()
            if algorithm == "BEAM": 
                list_board = agr.BEAM(maps[stage], list_check_points[stage], 1)
                num_states_visited = agr.number_states_visited()
                stateLenght = len(list_board[0]) if list_board != [] else 0
            AI_solving= True
            currentState = 0
            # Handle time
            current_time = pygame.time.get_ticks()
            print("Thời gian AI xử lí: "+str(current_time-start_time))
            start_time = pygame.time.get_ticks()
     
        if len(list_board) > 0 and AI_solving == True:
            clock.tick(5)
            new_list_board = list_board[0][1:]
            if currentState < len(new_list_board):
                nowpos = spf.find_position_player(new_board)
                nextpos = spf.find_position_player(new_list_board[currentState])
                direct = spf.check_movement_direction(nowpos,nextpos)
                print(direct)
                new_board = new_list_board[currentState]
                if direct == 'w':
                    player = pygame.image.load(assets_path + '\\playerup.png')
                if direct == 's':
                    player = pygame.image.load(assets_path + '\\playerdown.png')
                if direct == 'a':
                    player = pygame.image.load(assets_path + '\\playerleft.png')
                if direct == 'd':
                    player = pygame.image.load(assets_path + '\\playerright.png')
                pygame.mixer.Sound(assets_path + '\\movesound.wav').play()
                move_count += 1
                currentState = currentState + 1
                moved = True
        
        if control_game[enum_of_control_game.ALGORITHM.value].is_clicked():
            pygame.mixer.Sound(c.click_sound_path).play()
            algorithm_number +=1
            if algorithm_number == (len(algorithm_list)):
                algorithm_number = 0
            algorithm = algorithm_list[algorithm_number]
            
            # Thay đổi text của button algorithm
            font = pygame.font.Font(c.font_text_path, c.TEXT_SIZE-3)
            control_game[0].text = font.render(str(algorithm), True, 'black')
            rect=control_game[0].text.get_rect(center=control_game[0].image_rect.center)
            rect.top-=5
            control_game[0].text_rect = rect
            
        if control_game[enum_of_control_game.HOME.value].is_clicked():
            pygame.mixer.Sound(c.click_sound_path).play()
            running = False 
            
        if control_game[enum_of_control_game.REPLAY.value].is_clicked():
            pygame.mixer.Sound(c.click_sound_path).play()
            drawBoard(maps[stage])
            new_board = maps[stage]
            moved == False
            move_count = 0
             
        if control_game[enum_of_control_game.UNDO.value].is_clicked():
            pygame.mixer.Sound(c.click_sound_path).play()
            temp_board = load_matrix_from_txt(backward_path + '\\backward.txt')
            if move_count > 0 and new_board != temp_board:
                new_board = temp_board
                moved = True
                move_count -= 1
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    pygame.mixer.Sound(c.click_sound_path).play()
                    temp_board = load_matrix_from_txt(backward_path + '\\backward.txt')
                    if move_count > 0 and new_board != temp_board:
                        new_board = temp_board
                        moved = True
                        move_count -= 1
                if event.key == pygame.K_SPACE:
                    pygame.mixer.Sound(c.click_sound_path).play()
                    drawBoard(maps[stage])
                    new_board = maps[stage]
                    moved == False
                    move_count = 0
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    backward_matrix = new_board
                    temp_board = spf.move_in_1_direction(new_board, 'U', list_check_points[stage])  
                    if new_board != temp_board:
                        new_board = temp_board
                        moved = True
                        move_count += 1  
                    player = pygame.image.load(assets_path + '\\playerup.png')
                    pygame.mixer.Sound(assets_path + '\\movesound.wav').play()

                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    backward_matrix = new_board
                    temp_board = spf.move_in_1_direction(new_board, 'D', list_check_points[stage])  
                    if new_board != temp_board:
                        new_board = temp_board
                        moved = True
                        move_count += 1  
                    player = pygame.image.load(assets_path + '\\playerdown.png')
                    pygame.mixer.Sound(assets_path + '\\movesound.wav').play()
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    backward_matrix = new_board
                    temp_board = spf.move_in_1_direction(new_board, 'L', list_check_points[stage])  
                    if new_board != temp_board:
                        new_board = temp_board
                        moved = True
                        move_count += 1  
                    player = pygame.image.load(assets_path + '\\playerleft.png')
                    pygame.mixer.Sound(assets_path + '\\movesound.wav').play()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    backward_matrix = new_board
                    temp_board = spf.move_in_1_direction(new_board, 'R', list_check_points[stage])  
                    if new_board != temp_board:
                        new_board = temp_board
                        moved = True
                        move_count += 1  
                    player = pygame.image.load(assets_path + '\\playerright.png')
                    pygame.mixer.Sound(assets_path + '\\movesound.wav').play()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        if moved == False:
            drawBoard(maps[stage])
            new_board = maps[stage]
        else:
            drawBoard(new_board)
        pygame.display.update()
        save_matrix_to_txt(backward_matrix,backward_path + '\\backward.txt')
        
        if spf.check_win(new_board, list_check_points[stage]):
            select_in_menu = menu(screen, user, stage, 1000-move_count*seconds, seconds, move_count)
            start_time = pygame.time.get_ticks()
            move_count = 0
            if select_in_menu == 0:
                running = False
            elif select_in_menu == 1:
                pygame.mixer.Sound(c.click_sound_path).play()
                drawBoard(maps[stage])
                new_board = maps[stage]
                moved == False
            elif select_in_menu == 2:
                if stage == 29:
                    drawBoard(maps[stage])
                    new_board = maps[stage]
                    moved == False
                drawBoard(maps[stage+1])
                new_board = maps[stage+1]
                stage+=1
                moved = False
        


def menu(screen, user, stage, score, time, move):
    pygame.mixer.Sound(assets_path + '\\winsound.mp3').play()
    user.score[stage] = score
    if stage != 29:
        user.score[stage+1] = 0
    User.update_user(user)
    result = -1
    menu = pygame.image.load(assets_path+'\\png\\menu.png')
    rect = menu.get_rect(center=(c.SCREEN_WIDTH//2,c.SCREEN_HEIGHT//2))
    # button
    btn_home = pygame.image.load(c.icon_path+'Home.png')
    rect_home = btn_home.get_rect(centerx=rect.centerx-80, centery=rect.centery+120)
    btn_replay = pygame.image.load(c.icon_path+'Replay.png')
    rect_replay = btn_replay.get_rect(centerx=rect.centerx, centery=rect.centery+120)
    btn_next = pygame.image.load(c.icon_path+'Play.png')
    rect_next = btn_next.get_rect(centerx=rect.centerx+80, centery=rect.centery+120)
    screen.blit(menu, rect)
    screen.blit(btn_home, rect_home)
    screen.blit(btn_replay, rect_replay)
    screen.blit(btn_next, rect_next)
    # label
    label1 = controls.Label(c.font_text_path, "Score:", size=20, color=c.TITLE_COLOR, location_topleft=(rect.centerx-50,rect.centery-140))
    label1.text_rect.centerx = rect.centerx
    label1.draw(screen)

    label = controls.Label(c.font_text_path, str(score), size=50, color='white', location_topleft=(rect.centerx-100,rect.centery-100))
    label.text_rect.centerx = rect.centerx
    label.draw(screen)
    controls.Label(c.font_title_path, "Move: "+str(move), size=25, color=c.TITLE_COLOR, location_topleft=(rect.centerx-100,rect.centery-20)).draw(screen)
    controls.Label(c.font_title_path, "Time: "+str(time//60)+":"+str(time%60), size=25, color=c.TITLE_COLOR, location_topleft=(rect.centerx-100,rect.centery+40)).draw(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:     
                if rect_home.collidepoint(event.pos):
                    result = 0 # back to home (select map)
                if rect_replay.collidepoint(event.pos):
                    result = 1 # replay
                if rect_next.collidepoint(event.pos):
                    result = 2 # next
        if result >= 0:
            return result   
        pygame.display.update()
        
    

def move_event(direct):
    keyboard.press(direct)
    pygame.time.wait(300)
    keyboard.release(direct)


'''
//==================//
//      BACKWARD    //
//==================//
'''
def save_matrix_to_txt(matrix, file_path):   
    with open(file_path, 'w') as file:
        for row in matrix:
            line = ', '.join(row)
            file.write(line + '\n')

def load_matrix_from_txt(file_path):
    read_matrix = []

    with open(file_path, 'r') as file:
        for line in file:
            row = line.strip().split(', ')
            read_matrix.append(row) 
    return read_matrix

def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxW(0, text, title, style)


'''
//========================//
//      DECLARE AND       //
//  INITIALIZE MAPS AND   //
//      CHECK POINTS      //
//========================//
'''
maps = get_boards()      
list_check_points = get_check_points()
def main():
    sokoban()

if __name__ == "__main__":
	main()


