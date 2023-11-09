import numpy as np
import os
import pygame
import re
'''
//========================//
//    GET SOME ASSETS     //
//========================//
'''
assets_path = os.getcwd() + "\\..\\Assets"
os.chdir(assets_path)
player = pygame.image.load(os.getcwd() + '\\player.png')
wall = pygame.image.load(os.getcwd() + '\\wall.png')
box = pygame.image.load(os.getcwd() + '\\box.png')
point = pygame.image.load(os.getcwd() + '\\point.png')
space = pygame.image.load(os.getcwd() + '\\space.png')
init_background = pygame.image.load(os.getcwd() + '\\init_background.png')


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


'''
//============================//
//     GET THE TESTCASES      //
//    AND CHECKPOINTS PATH    //
//           FOLDERS          //
//============================//
'''
path_board = os.getcwd() + '\\..\\Testcases'
path_checkpoint = os.getcwd() + '\\..\\Checkpoints'


def get_number (file): 
    match = re.search ('(\d+)', file) 
    if match:
        return int (match.group(1)) 
    else: 
        return 0

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


''' 
//===========================//
//      SOKOBAN FUNCTION     //
//===========================//
'''
def sokoban(stage):
    running = True 
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1200, 760))
    pygame.display.set_caption('Sokoban Game')
    BACKGROUND = (0, 0, 0) #BLACK
    WHITE = (255, 255, 255)
    while running:     
        screen.blit(init_background, (0, 0))
        initGame(maps[stage])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            pygame.display.flip()

    pygame.quit()

    
'''
//==================//
//      DISPLAY     //
//    INITIALIZE    //
//      SCENE       //
//==================//
'''
def initGame(map):
	renderMap(map)


'''
//========================//
//      DECLARE AND       //
//  INITIALIZE MAPS AND   //
//      CHECK POINTS      //
//========================//
'''
maps = get_boards()
                
# def main():
#     sokoban()

# if __name__ == "__main__":
# 	main()



