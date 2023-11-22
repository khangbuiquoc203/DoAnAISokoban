import support_func as spf 
import time
from queue import PriorityQueue

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
    while not heuristic_queue.empty():
        now_state = heuristic_queue.get()
        cur_pos = spf.find_position_player(now_state.board)

        list_can_move = spf.get_next_pos(now_state.board, cur_pos)
        for next_pos in list_can_move:
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
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
    while not heuristic_queue.empty():
        now_state = heuristic_queue.get()
        cur_pos = spf.find_position_player(now_state.board)
    
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)
        for next_pos in list_can_move:
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
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
    
    cost_queue = PriorityQueue()
    cost_queue.put(start_state)
    while not cost_queue.empty():
        now_state = cost_queue.get()
        cur_pos = spf.find_position_player(now_state.board)
    
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)
        for next_pos in list_can_move:
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
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
        
    print("Not Found")
    return []
