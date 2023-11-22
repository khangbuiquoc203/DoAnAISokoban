from copy import deepcopy
import numpy as np

TIME_OUT = 1800
'''
//========================//
//        SUPPORTING      //
//        FUNCTIONS       //
//========================//
'''
'''
DATA CONTAINER TO STORE THE STATE FOR EACH STEP
'''
class state:
    def __init__(self, board, state_parent, cost, list_check_point, algorithm):
        self.board = board
        self.state_parent = state_parent
        self.cost = cost
        self.heuristic = 0
        self.algorithm = algorithm
        self.check_points = deepcopy(list_check_point)
        
    ''' FUNCTION TO BACKTRACK TO THE FIRST IF THE CURRENT STATE IS GOAL '''
    def get_line(self):    
        path = []
        current_state = self
        while current_state is not None:
            path.append(current_state.board)
            current_state = current_state.state_parent
        path.reverse()
        return path
            
            
    
    ''' COMPUTE HEURISTIC FUNCTION USED FOR GREEDY, A* ALGORITHM
    def h(self):
        list_boxes = find_boxes_position(self.board)
        if self.heuristic == 0:
            self.heuristic = abs(sum(list_boxes[i][0] + list_boxes[i][1] - self.check_points[i][0] - self.check_points[i][1] for i in range(len(list_boxes))))
        return self.heuristic
    '''
    
    def h(self):
        list_boxes = find_boxes_position(self.board) 
        if self.heuristic == 0: # Convert the lists to numpy arrays 
            array_boxes = np.array(list_boxes) 
            array_check_points = np.array(self.check_points) # Calculate the absolute sum of the differences 
            self.heuristic = np.sum(np.abs(array_boxes - array_check_points)) 
        return self.heuristic
    
    def depth(self):
        return self.depth
    
    def g(self):
        return self.cost 
      
    def __gt__(self, other):
        if self.algorithm == "ASTAR": 
            return (self.h() + self.g()) > (other.h() + other.g()) 
        elif self.algorithm == "GREEDY": 
            return (self.h()) > (other.h()) 
        elif self.algorithm == "UCS": 
            return (self.g()) > (other.g()) 
        else: return False

''' FIND THE PLAYER'S CURRENT POSITION IN A BOARD '''
def find_position_player(board):
    array = np.array(board) 
    x, y = np.where(array == '@')
    if len(x) > 0 and len(y) > 0:
      return (x[0], y[0])
    else: 
      return (-1, -1) # error board


''' COMPARE 2 BOARDS '''
def compare_matrix(board_A, board_B):
    array_A = np.array(board_A) 
    array_B = np.array(board_B)
    return np.array_equal(array_A, array_B)


''' CHECK WHETHER THE BOARD IS GOAL OR NOT '''
def check_win(board, list_check_point):
    return all(board[p[0]][p[1]] == '$' for p in list_check_point)


''' CHECK WHETHER A SINGLE BOX IS ON A CHECKPOINT '''
def is_box_on_check_point(box, list_check_point):
    return box in list_check_point


''' CHECK WHETHER A SIGNLE BOX IS STUCK IN THE CORNER '''
def check_in_corner(board, x, y, list_check_point):
    '''return true if board[x][y] in corner'''

    if (
        (board[x-1][y-1] == '#' and board[x-1][y] == '#' and board[x][y-1] == '#') or
        (board[x+1][y-1] == '#' and board[x+1][y] == '#' and board[x][y-1] == '#') or
        (board[x-1][y+1] == '#' and board[x-1][y] == '#' and board[x][y+1] == '#') or
        (board[x+1][y+1] == '#' and board[x+1][y] == '#' and board[x][y+1] == '#')
    ) and not is_box_on_check_point((x, y), list_check_point):
        return True
    return False


''' CHECK WHETHER THE BOARD ALREADY EXISTED IN THE TRAVERSED LIST'''
def is_board_exist(board, list_state):
    '''return true if has same board in list'''
    for state in list_state:
        if compare_matrix(state.board, board):
            return True
    return False


''' CHECK WHETHER ALL BOXES ARE STUCK '''
def is_all_boxes_stuck(board, list_check_point):
    box_positions = find_boxes_position(board)
    result = True
    for box_position in box_positions:
        if is_box_on_check_point(box_position, list_check_point):
            return False
        if is_box_can_be_moved(board, box_position):
            result = False
    return result

''' CHECK WHETHER AT LEAST ONE BOX IS STUCK IN THE CORNER'''
def is_board_can_not_win(board, list_check_point):
    '''return true if box in corner of wall -> can't win'''
    array = np.array(board)
    x, y = np.where(array == '$')
    
    for i in range(len(x)):
        if check_in_corner(board, x[i], y[i], list_check_point):
            return True
    return False


''' FIND ALL BOXES' POSITIONS '''
def find_boxes_position(board):
    array = np.array(board)
    x, y = np.where(array == '$')
    xy = np.transpose([x, y])
    result = xy.tolist()
    return result


''' CHECK WHETHER A SINGLE BOX CAN BE MOVED IN AT LEAST 1 DIRECTION'''
def is_box_can_be_moved(board, box_position):
    left_move = (box_position[0], box_position[1] - 1) 
    right_move = (box_position[0], box_position[1] + 1)
    up_move = (box_position[0] - 1, box_position[1])
    down_move = (box_position[0] + 1, box_position[1])
    if (board[left_move[0]][left_move[1]] == ' ' or board[left_move[0]][left_move[1]] == '%' or board[left_move[0]][left_move[1]] == '@') and board[right_move[0]][right_move[1]] != '#' and board[right_move[0]][right_move[1]] != '$':
        return True
    if (board[right_move[0]][right_move[1]] == ' ' or board[right_move[0]][right_move[1]] == '%' or board[right_move[0]][right_move[1]] == '@') and board[left_move[0]][left_move[1]] != '#' and board[left_move[0]][left_move[1]] != '$':
        return True
    if (board[up_move[0]][up_move[1]] == ' ' or board[up_move[0]][up_move[1]] == '%' or board[up_move[0]][up_move[1]] == '@') and board[down_move[0]][down_move[1]] != '#' and board[down_move[0]][down_move[1]] != '$':
        return True
    if (board[down_move[0]][down_move[1]] == ' ' or board[down_move[0]][down_move[1]] == '%' or board[down_move[0]][down_move[1]] == '@') and board[up_move[0]][up_move[1]] != '#' and board[up_move[0]][up_move[1]] != '$':
        return True
    return False


''' GET THE NEXT POSSIBLE MOVE '''
def get_next_pos(board, cur_pos):
    '''return list of positions that player can move to from current position'''
    x,y = cur_pos[0], cur_pos[1]
    list_can_move = []
    # MOVE UP (x - 1, y)
    if 0 <= x - 1 < len(board):
        value = board[x - 1][y]
        if value == ' ' or value == '%':
            list_can_move.append((x - 1, y))
        elif value == '$' and 0 <= x - 2 < len(board):
            next_pos_box = board[x - 2][y]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x - 1, y))
    # MOVE DOWN (x + 1, y)
    if 0 <= x + 1 < len(board):
        value = board[x + 1][y]
        if value == ' ' or value == '%':
            list_can_move.append((x + 1, y))
        elif value == '$' and 0 <= x + 2 < len(board):
            next_pos_box = board[x + 2][y]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x + 1, y))
    # MOVE LEFT (x, y - 1)
    if 0 <= y - 1 < len(board[0]):
        value = board[x][y - 1]
        if value == ' ' or value == '%':
            list_can_move.append((x, y - 1))
        elif value == '$' and 0 <= y - 2 < len(board[0]):
            next_pos_box = board[x][y - 2]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x, y - 1))
    # MOVE RIGHT (x, y + 1)
    if 0 <= y + 1 < len(board[0]):
        value = board[x][y + 1]
        if value == ' ' or value == '%':
            list_can_move.append((x, y + 1))
        elif value == '$' and 0 <= y + 2 < len(board[0]):
            next_pos_box = board[x][y + 2]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x, y + 1))
    return list_can_move


''' MOVE THE BOARD IN CERTAIN DIRECTIONS '''
def move(board, next_pos, cur_pos, list_check_point):
    '''return a new board after move'''
    new_board = deepcopy(board) 
    # FIND NEXT POSITION IF MOVE TO BOX
    if new_board[next_pos[0]][next_pos[1]] == '$':
        x = 2*next_pos[0] - cur_pos[0]
        y = 2*next_pos[1] - cur_pos[1]
        new_board[x][y] = '$'
    # MOVE PLAYER TO NEW POSITION
    new_board[next_pos[0]][next_pos[1]] = '@'
    new_board[cur_pos[0]][cur_pos[1]] = ' '
    # CHECK IF AT CHECK POINT'S POSITION DON'T HAVE ANYTHING THEN UPDATE % LIKE CHECK POINT
    for p in list_check_point:
        if new_board[p[0]][p[1]] == ' ':
            new_board[p[0]][p[1]] = '%'
    return new_board


''' FIND ALL CHECKPOINTS ON THE BOARD '''
def find_list_check_point(board):
    '''return list check point form the board
        if don't have any check point, return empty list
        it will check num of box, if num of box < num of check point
            return list [(-1,-1)]'''
    #list_check_point = []
    num_of_box = 0
    array = np.array(board)
    num_of_box = np.count_nonzero(array=='$')
    num_of_check_point = np.count_nonzero(array == '%')
    if num_of_box < num_of_check_point:
        return [(-1, -1)]
    
    x, y = np.where(array == '%')
    xy = np.transpose([x, y])
    result = xy.tolist()
    return result

    ''' CHECK THE ENTIRE BOARD TO FIND CHECK POINT AND NUM OF BOX
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == '$':
                num_of_box += 1
            elif board[x][y] == '%':
                list_check_point.append((x,y))
    if num_of_box < len(list_check_point):
        return [(-1,-1)]
    return list_check_point
    '''
    
'''FUNCTION RETURN NEW BOARD AFTER MOVE IN 1 DIRECTION'''
def move_in_1_direction(board, direct, list_check_point):
    # MAKE NEW BOARD AS SAME AS CURRENT BOARD
    new_board = deepcopy(board)
    
    # GET POSITION OF PLAYER ON CURRENT BOARD AND SET VALUE TO 2 VARIABLES
    cur_pos = find_position_player(board)
    list_can_move = get_next_pos(board, cur_pos)
    flag = False
    x, y = cur_pos[0], cur_pos[1]

    # GET NEW POSITION AFTER MOVING
    if direct == 'U':
        x -= 1
    if direct == 'D':
        x += 1
    if direct == 'L':
        y -= 1
    if direct == 'R':
        y += 1
        
    for next_pos in list_can_move:
        if x == next_pos[0] and y == next_pos[1]:
            flag = True
            
    if flag == True:
        # COLLID WITH THE WALL
        if new_board[x][y] == '$':
            z = 2 * x - cur_pos[0]
            t = 2 * y - cur_pos[1]
            # MOVE PLAYER TO NEW POSITION
            new_board[z][t] = '$'
        new_board[x][y] = '@'
        new_board[cur_pos[0]][cur_pos[1]] = ' '
            
        # CHECK IF AT CHECK POINT'S POSITION DON'T HAVE ANYTHING THEN UPDATE % LIKE CHECK POINT
        for p in list_check_point:
            if new_board[p[0]][p[1]] == ' ':
                new_board[p[0]][p[1]] = '%'
        return new_board 
    return board

def check_movement_direction(previous_position, current_position):
    prev_row, prev_col = previous_position
    curr_row, curr_col = current_position
    if curr_row < prev_row:
        return 'w'
    elif curr_row > prev_row:
        return 's'
    elif curr_col < prev_col:
        return 'a'
    elif curr_col > prev_col:
        return 'd'
    else:
        return 'no_movement'
