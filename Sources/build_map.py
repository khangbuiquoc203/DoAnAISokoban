import numpy as np
import os
import pygame
import re
import button
import support_func as spf
import ctypes
import const as c
import sys
import algo
import keyboard
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
stage = 29
clock = pygame.time.Clock()
#text_font=pygame.font.Font("Arial",30)
list_board = []
algorithm_number = 0
algorithm_list = ["BFS", "DFS", "A Star", "UCS", "Greedy", "ID", "Hill Climbing", "Beam", "Dijkstra"]
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

text_font=pygame.font.Font(os.getcwd() + '\\game.ttf',45)
textsmall_font=pygame.font.Font(os.getcwd() + '\\game.ttf',30)

''' DRAW BUTTON'''
start_img = pygame.image.load(os.getcwd()+'\\start_btn.png').convert_alpha()
solve_img = pygame.image.load(os.getcwd()+'\\solve_btn.png').convert_alpha()
reset_img = pygame.image.load(os.getcwd()+'\\reset_btn.png').convert_alpha()
algos_img = pygame.image.load(os.getcwd()+'\\algos_btn.png').convert_alpha()
player_img = pygame.image.load(os.getcwd()+'\\player_name.png').convert_alpha()
level_img = pygame.image.load(os.getcwd()+'\\level.png').convert_alpha()


player_button = button.Button(780, 200, player_img, 1)
level_button = button.Button(780, 260, level_img, 1)
start_button = button.Button(780, 320, start_img, 1)
solve_button = button.Button(780, 380, solve_img, 1)
reset_button = button.Button(780, 440, reset_img, 1)
algos_button = button.Button(780, 500, algos_img, 1)


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
    return result

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
//===========================//
//      A BRICK OR A BOX     //
//     MEASURING 32X32       //
//===========================//
'''
def renderMap(board):
    width = len(board[0])  
    height = len(board)  

    screen_width = 1200  
    screen_height = 760  

    tile_size = 32  

    map_width_pixels = width * tile_size  
    map_height_pixels = height * tile_size  

    
    map_offset_x = (screen_width - map_width_pixels) // 10
    map_offset_y = (screen_height - map_height_pixels) // 2

    for i in range(height):
        for j in range(width):
            screen.blit(space, (j * tile_size + map_offset_x, i * tile_size + map_offset_y))
            if board[i][j] == '#':
                screen.blit(wall, (j * tile_size + map_offset_x, i * tile_size + map_offset_y))
            if board[i][j] == '$':
                screen.blit(box, (j * tile_size + map_offset_x, i * tile_size + map_offset_y))
            if board[i][j] == '%':
                screen.blit(point, (j * tile_size + map_offset_x, i * tile_size + map_offset_y))
            if board[i][j] == '@':
                screen.blit(player, (j * tile_size + map_offset_x, i * tile_size + map_offset_y))

''' VARIABLE '''
algorithm = algorithm_list[0]
''' 
//===========================//
//      SOKOBAN FUNCTION     //
//===========================//
'''
def sokoban(screen, stage):
    running = True 
    global algorithm
    global player
    global list_board
    global algorithm_number
    global num_states_visited
    pygame.font.init()
    BACKGROUND = (0, 0, 0) #BLACK
    WHITE = (255, 255, 255)
    moved = False
    new_board = []
    backward_matrix = []
    playsound = False
    stateLenght = 0
    AI_solving = False
    currentState = 0
    # back button
    back = pygame.image.load(c.icon_path)
    back_rect = back.get_rect(topleft=(10,c.SCREEN_HEIGHT-back.get_height()))
    while running:     
        screen.blit(init_background, (0, 0))
        
        # back button
        screen.blit(back, back_rect)
        
        if moved == False:
            initGame(maps[stage])
            new_board = maps[stage]
        else:
            initGame(new_board)
        display(stage)
        
        if solve_button.draw(screen):
            move_step = []
            check_points = get_check_points()
            list_check_point = check_points[stage]
            if algorithm == "BFS":
                list_board = algo.BFS_search(maps[stage], list_check_point)
                num_states_visited = algo.number_states_visited()
                print(num_states_visited)
            if algorithm == "DFS":
                list_board = algo.DFS_search(maps[stage], list_check_point)
                num_states_visited = algo.number_states_visited()
                print(num_states_visited)
            if algorithm == "ID":
                list_board = algo.ID_search(maps[stage], list_check_point)
                num_states_visited = algo.number_states_visited()
                print(num_states_visited)
            if algorithm == "Dijkstra":
                list_board = algo.Dijkstra_search(maps[stage], list_check_point)
                num_states_visited = algo.number_states_visited()
                print(num_states_visited)  
            stateLenght = len(list_board[0])
            AI_solving= True
            currentState = 0
                
        if reset_button.draw(screen):
            print('RESET')
            initGame(maps[stage])
            new_board = maps[stage]
            playsound = False
            moved == False
        if player_button.draw(screen):
            print('RESET')
        if level_button.draw(screen):
            print('RESET')
        if algos_button.draw(screen):
            algorithm_number +=1
            if algorithm_number == (len(algorithm_list)):
                algorithm_number = 0
            algorithm = algorithm_list[algorithm_number]
            
        if start_button.draw(screen):
            print('RESET')
            
            
            
        if len(list_board) > 0 and AI_solving == True:
            clock.tick(3)
            new_board = list_board[0][currentState]
            sound = pygame.mixer.Sound(assets_path + '\\movesound.wav')
            sound.play()
            currentState = currentState + 1
            moved = True
            if currentState == stateLenght:
                AI_solving = False
        
        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_rect.collidepoint(event.pos):
                    running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    new_board = load_matrix_from_txt(backward_path + '\\backward.txt')
                    moved = True
                if event.key == pygame.K_SPACE:
                    initGame(maps[stage])
                    new_board = maps[stage]
                    playsound = False
                    moved == False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    backward_matrix = new_board
                    new_board = spf.move_in_1_direction(new_board, 'U', list_check_points[stage]) 
                    sound = pygame.mixer.Sound(assets_path + '\\movesound.wav')
                    sound.play()
                    moved = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    backward_matrix = new_board
                    new_board = spf.move_in_1_direction(new_board, 'D', list_check_points[stage])
                    sound = pygame.mixer.Sound(assets_path + '\\movesound.wav')
                    sound.play()
                    moved = True
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    backward_matrix = new_board
                    new_board = spf.move_in_1_direction(new_board, 'L', list_check_points[stage])
                    player = pygame.image.load(assets_path + '\\playerleft.png')
                    sound = pygame.mixer.Sound(assets_path + '\\movesound.wav')
                    sound.play()
                    moved = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    backward_matrix = new_board
                    new_board = spf.move_in_1_direction(new_board, 'R', list_check_points[stage])
                    player = pygame.image.load(assets_path + '\\playerright.png')
                    sound = pygame.mixer.Sound(assets_path + '\\movesound.wav')
                    sound.play()
                    moved = True
                if event.key == pygame.K_RETURN and spf.check_win(new_board, list_check_points[stage]):
                    initGame(maps[stage+1])
                    new_board = maps[stage+1]
                    stage+=1
                    playsound = False
                    moved = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if spf.check_win(new_board, list_check_points[stage]):
            draw_text("Press enter to continue!", textsmall_font, (255, 255, 255), 150, 350)
            draw_text("State visited: " + str(num_states_visited), textsmall_font, (255, 255, 255), 700, 15)
            if playsound == False:
                sound = pygame.mixer.Sound(assets_path + '\\winsound.mp3')
                sound.play()
                playsound = True
        pygame.display.update()
        save_matrix_to_txt(backward_matrix,backward_path + '\\backward.txt')
        
        
    
        
            
            
    #pygame.quit()


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
'''
//==================//
//      DISPLAY     //
//    INITIALIZE    //
//      SCENE       //
//==================//
'''
def initGame(map):
	renderMap(map)

def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxW(0, text, title, style)

def display(stage):
    # Vẽ các text border
    pygame.draw.rect(screen, (255, 255, 255), (930,200,150,40), width=3, border_bottom_left_radius=5, border_bottom_right_radius=5, border_top_left_radius=5, border_top_right_radius=5)
    pygame.draw.rect(screen, (255, 255, 255), (930,500,200,40), width=3, border_bottom_left_radius=5, border_bottom_right_radius=5, border_top_left_radius=5, border_top_right_radius=5)
    draw_text("Sokoban Game", text_font, (255, 255, 255), 800, 80)
    draw_text("Score: ", textsmall_font, (255, 255, 255), 100, 15)
    draw_text("Time: ", textsmall_font, (255, 255, 255), 400, 15)
    

    mapText = textsmall_font.render("Lv. " + str(stage+1), True, WHITE)
    mapRect = mapText.get_rect(center=(955, 280))
    screen.blit(mapText, mapRect)

 
    algorithmText = textsmall_font.render(str(algorithm), True, WHITE)
    algorithmRect = algorithmText.get_rect(center=(1025, 520))
    screen.blit(algorithmText, algorithmRect)

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



