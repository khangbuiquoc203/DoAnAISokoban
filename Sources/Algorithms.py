import support_func as spf 
import time
from queue import PriorityQueue
import random

'''
//========================//
//          ASTAR         //
//        ALGORITHM       //
//========================//
'''
def ASTAR(board, list_check_point):
    start_time = time.time()

    start_state = spf.state(board, None, 0, list_check_point, "ASTAR")
    list_state = [start_state]
    
    heuristic_queue = PriorityQueue()
    heuristic_queue.put(start_state)
    global num_states_visited
    num_states_visited = 0
    while not heuristic_queue.empty():
        now_state = heuristic_queue.get()
        cur_pos = spf.find_position_player(now_state.board)

        list_can_move = spf.get_next_pos(now_state.board, cur_pos)
        num_shuffles = 23

        for _ in range(num_shuffles):
            random.shuffle(list_can_move)
        for next_pos in list_can_move:
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
            num_states_visited+=1
            if spf.is_board_exist(new_board, list_state):
                continue
            if spf.is_board_can_not_win(new_board, list_check_point):
                continue
            if spf.is_all_boxes_stuck(new_board, list_check_point):
                continue

            new_state = spf.state(new_board, now_state, now_state.cost, list_check_point, "ASTAR")
            
            if spf.check_win(new_board, list_check_point):
                print("Found win")
                return (new_state.get_line(), len(list_state))

            new_state.cost += 1
            list_state.append(new_state)
            heuristic_queue.put(new_state)
            
            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return []
        
    print("Not Found")
    return []

'''
//========================//
//          GREEDY        //
//        ALGORITHM       //
//========================//
'''
def GREEDY(board, list_check_point): 
    start_time = time.time()
    start_state = spf.state(board, None, 0, list_check_point, "GREEDY")
    list_state = [start_state]
    
    heuristic_queue = PriorityQueue()
    heuristic_queue.put(start_state)
    
    global num_states_visited
    num_states_visited = 0
    
    while not heuristic_queue.empty():
        now_state = heuristic_queue.get()
        cur_pos = spf.find_position_player(now_state.board)
    
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)
        num_shuffles = 23

        for _ in range(num_shuffles):
            random.shuffle(list_can_move)
        for next_pos in list_can_move:
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
            num_states_visited += 1
            if spf.is_board_exist(new_board, list_state):
                continue
            if spf.is_board_can_not_win(new_board, list_check_point):
                continue
            if spf.is_all_boxes_stuck(new_board, list_check_point):
                continue
    
            new_state = spf.state(new_board, now_state, now_state.cost, list_check_point, "GREEDY")
            
            if spf.check_win(new_board, list_check_point):
                print("Found win")
                return (new_state.get_line(), len(list_state))
    
            list_state.append(new_state)
            heuristic_queue.put(new_state)
    
            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return []
        
    print("Not Found")
    return []

'''
//========================//
//           UCS          //
//        ALGORITHM       //
//========================//
'''
def UCS(board, list_check_point): 
    start_time = time.time()
    start_state = spf.state(board, None, 0, list_check_point, "UCS")
    list_state = [start_state]
    
    global num_states_visited
    num_states_visited = 0
    
    cost_queue = PriorityQueue()
    cost_queue.put(start_state)
    while not cost_queue.empty():
        now_state = cost_queue.get()
        cur_pos = spf.find_position_player(now_state.board)
    
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)
        num_shuffles = 23

        for _ in range(num_shuffles):
            random.shuffle(list_can_move)
        for next_pos in list_can_move:
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
            num_states_visited += 1
            if spf.is_board_exist(new_board, list_state):
                continue
            if spf.is_board_can_not_win(new_board, list_check_point):
                continue
            if spf.is_all_boxes_stuck(new_board, list_check_point):
                continue
    
            new_state = spf.state(new_board, now_state, now_state.cost, list_check_point, "UCS")
            
            if spf.check_win(new_board, list_check_point):
                print("Found win")
                return (new_state.get_line(), len(list_state))
    
            new_state.cost += 1
            list_state.append(new_state)
            cost_queue.put(new_state)
            
            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []    
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return []
        
    print("Not Found")
    return []


'''
//========================//
//           BFS          //
//        ALGORITHM       //
//========================//
'''
def BFS(board, list_check_point):
    start_time = time.time()
    start_state = spf.state(board, None, 0, list_check_point, "BFS")
    
    list_state = [start_state]
    list_visit = [start_state]
    
    global num_states_visited
    num_states_visited = 0
    
    while len(list_visit) != 0:
        
        now_state = list_visit.pop(0)
        cur_pos = spf.find_position_player(now_state.board)

        list_can_move = spf.get_next_pos(now_state.board, cur_pos)
        num_shuffles = 23

        for _ in range(num_shuffles):
            random.shuffle(list_can_move)

        for next_pos in list_can_move:
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
            num_states_visited+=1
            if spf.is_board_exist(new_board, list_state):
                continue           
            if spf.is_board_can_not_win(new_board, list_check_point) or spf.is_all_boxes_stuck(new_board, list_check_point):
                continue
            new_state = spf.state(new_board, now_state, 0, list_check_point, "BFS")
            
            if spf.check_win(new_board, list_check_point):
                print("Found win")
                return (new_state.get_line(), len(list_state))
            
            list_state.append(new_state)
            list_visit.append(new_state)

            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return []
        
    print("Not Found")
    return []

'''
//========================//
//           DFS          //
//        ALGORITHM       //
//========================//
'''
def DFS(board, list_check_point):
    start_time = time.time()

    start_state = spf.state(board, None, 0, list_check_point, "DFS")

    list_state = [start_state]
    list_visit = [start_state]
    
    global num_states_visited
    num_states_visited = 0
    
    while len(list_visit) != 0:
        now_state = list_visit.pop()
        cur_pos = spf.find_position_player(now_state.board)
        
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)
        num_shuffles = 23

        for _ in range(num_shuffles):
            random.shuffle(list_can_move)

        for next_pos in list_can_move:
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
            num_states_visited+=1
            if spf.is_board_exist(new_board, list_state):
                continue
            if spf.is_board_can_not_win(new_board, list_check_point) or spf.is_all_boxes_stuck(new_board, list_check_point):
                continue

            new_state = spf.state(new_board, now_state, 0, list_check_point, "DFS")

            if spf.check_win(new_board, list_check_point):
                print("Found win")
                return (new_state.get_line(), len(list_state))
            
            list_state.append(new_state)
            list_visit.append(new_state)

            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return []
    print("Not Found")
    return []

def LDFS(board, list_check_point):
    start_time = time.time()
    max_depth=50
    start_state = spf.state(board, None, 0, list_check_point, "LDFS")

    stack = [(start_state, 0)]  # Dùng stack để theo dõi trạng thái và độ sâu
    list_state = [start_state]

    global num_states_visited
    num_states_visited = 0

    while stack:
        now_state, current_depth = stack.pop()
        cur_pos = spf.find_position_player(now_state.board)

        list_can_move = spf.get_next_pos(now_state.board, cur_pos)
        num_shuffles = 23

        for _ in range(num_shuffles):
            random.shuffle(list_can_move)

        for next_pos in list_can_move:
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
            num_states_visited += 1

            if spf.is_board_exist(new_board, list_state) or current_depth >= max_depth:
                continue

            if spf.is_board_can_not_win(new_board, list_check_point) or spf.is_all_boxes_stuck(new_board, list_check_point):
                continue

            new_state = spf.state(new_board, now_state, current_depth + 1, list_check_point, "LDFS")

            if spf.check_win(new_board, list_check_point):
                print("Found win")
                return (new_state.get_line(), len(list_state))

            list_state.append(new_state)
            stack.append((new_state, current_depth + 1))

        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return []

    print("Not Found")
    return []

def IDFS(board, list_check_point):
    start_time = time.time()
    max_depth = 1  # Initial depth limit
    
    while True:
        result = depth_limited_DFS(board, list_check_point, max_depth)
        if result:
            return result
        max_depth += 1

        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            print("Time limit exceeded")
            return []
        
def depth_limited_DFS(board, list_check_point, max_depth):
    start_time = time.time()
    start_state = spf.state(board, None, 0, list_check_point, "IDFS")

    list_state = [start_state]
    list_visit = [start_state]
    
    global num_states_visited
    num_states_visited = 0
    
    while len(list_visit) != 0:
        now_state = list_visit.pop()
        cur_pos = spf.find_position_player(now_state.board)
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)
        num_shuffles = 23

        for _ in range(num_shuffles):
            random.shuffle(list_can_move)

        for next_pos in list_can_move:
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
            num_states_visited += 1
            if spf.is_board_exist(new_board, list_state):
                continue
            
            if spf.is_board_can_not_win(new_board, list_check_point) or spf.is_all_boxes_stuck(new_board, list_check_point):
                continue

            new_state = spf.state(new_board, now_state, now_state.cost, list_check_point, "IDFS")

            if spf.check_win(new_board, list_check_point):
                print("Found win")
                return (new_state.get_line(), len(list_state))

            new_state.cost += 1
            list_state.append(new_state)
            list_visit.append(new_state)

            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []
        
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return []
        
        ''' Check if depth limit is reached '''
        if now_state.depth < max_depth:
            continue
        
    print("Not Found")
    return []
  
def BEAM(board, list_check_point, beam_width): 
    start_time = time.time() 
    start_state = spf.state(board, None, 0, list_check_point, "BEAM") 
    list_state = [start_state]
    
    heuristic_queue = PriorityQueue()
    heuristic_queue.put(start_state)
    
    global num_states_visited
    num_states_visited = 0
    
    while not heuristic_queue.empty():
        # Get the top beam_width states from the queue
        beam_states = []
        for _ in range(beam_width):
            if heuristic_queue.empty():
                break
            beam_states.append(heuristic_queue.get())
        
        # Expand each state in the beam and add the successors to the queue
        for now_state in beam_states:
            cur_pos = spf.find_position_player(now_state.board)
    
            list_can_move = spf.get_next_pos(now_state.board, cur_pos)
            num_shuffles = 23
    
            for _ in range(num_shuffles):
                random.shuffle(list_can_move)
            for next_pos in list_can_move:
                new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
                num_states_visited += 1
                if spf.is_board_exist(new_board, list_state):
                    continue
                if spf.is_board_can_not_win(new_board, list_check_point):
                    continue
                if spf.is_all_boxes_stuck(new_board, list_check_point):
                    continue
    
                new_state = spf.state(new_board, now_state, now_state.cost, list_check_point, "BEAM")
            
                if spf.check_win(new_board, list_check_point):
                    print("Found win")
                    return (new_state.get_line(), len(list_state))
    
                list_state.append(new_state)
                heuristic_queue.put(new_state)
    
                end_time = time.time()
                if end_time - start_time > spf.TIME_OUT:
                    return []
            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []
    
    print("Not Found")
    return []    

def HILL(board, list_check_point): 
    start_time = time.time()
    start_state = spf.state(board, None, 0, list_check_point, "HILL")
    list_state = [start_state]
    
    global num_states_visited
    num_states_visited = 0
    
    while True:
        now_state = list_state[-1]
        cur_pos = spf.find_position_player(now_state.board)
    
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)
        num_shuffles = 23

        for _ in range(num_shuffles):
            random.shuffle(list_can_move)
        best_heuristic_value = float('-inf')
        best_next_state = None
        
        for next_pos in list_can_move:
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
            
            if spf.is_board_exist(new_board, list_state):
                continue
            if spf.is_board_can_not_win(new_board, list_check_point):
                continue
            if spf.is_all_boxes_stuck(new_board, list_check_point):
                continue
    
            new_state = spf.state(new_board, now_state, now_state.cost, list_check_point, "HILL")
            heuristic_value = new_state.h()
            
            if heuristic_value > best_heuristic_value:
                best_heuristic_value = heuristic_value
                best_next_state = new_state
        
        if best_next_state is None:
            print("Not Found")
            return []
        
        if spf.check_win(best_next_state.board, list_check_point):
            print("Found win")
            return (best_next_state.get_line(), len(list_state))
    
        list_state.append(best_next_state)
        num_states_visited += 1
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return []

def number_states_visited():
    return num_states_visited  
