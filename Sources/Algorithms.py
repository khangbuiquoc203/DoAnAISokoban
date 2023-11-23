import support_func as spf
import time
import random
import heapq
'''
//========================//
//           BFS          //
//        ALGORITHM       //
//     IMPLEMENTATION     //
//========================//
'''
def BFS_search(board, list_check_point):
    start_time = time.time()
    ''' BFS SEARCH SOLUTION '''
    ''' IF START BOARD IS GOAL OR DON'T HAVE CHECK POINT '''
    if spf.check_win(board,list_check_point):
        print("Found win")
        return [board]
    ''' INITIALIZE START STATE '''
    start_state = spf.state(board, None, list_check_point)
    ''' INITIALIZE 2 LISTS USED FOR BFS SEARCH '''
    list_state = [start_state]
    list_visit = [start_state]
    
    global num_states_visited
    num_states_visited = 0
    ''' LOOP THROUGH VISITED LIST '''
    while len(list_visit) != 0:
        num_states_visited +=1
        ''' GET NOW STATE TO SEARCH '''
        now_state = list_visit.pop(0)
        ''' GET THE PLAYER'S CURRENT POSITION '''
        cur_pos = spf.find_position_player(now_state.board)
        ''' 
        THIS WILL PRINT THE STEP-BY-STEP IMPLEMENTATION OF HOW THE ALGORITHM WORKS, 
        UNCOMMENT TO USE IF NECCESSARY 
        '''
        '''
        time.sleep(1)
        clear = lambda: os.system('cls')
        clear()
        print_matrix(now_state.board)
        print("State visited : {}".format(len(list_state)))
        print("State in queue : {}".format(len(list_visit)))
        '''

        ''' GET LIST POSITION THAT PLAYER CAN MOVE TO '''
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)
        num_shuffles = 23

        for _ in range(num_shuffles):
            random.shuffle(list_can_move)
        ''' MAKE NEW STATES FROM LIST CAN MOVE '''
        for next_pos in list_can_move:
            ''' MAKE NEW BOARD '''
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
            ''' IF THIS BOARD DON'T HAVE IN LIST BEFORE --> SKIP THE STATE '''
            if spf.is_board_exist(new_board, list_state):
                continue
            ''' IF ONE OR MORE BOXES ARE STUCK IN THE CORNER --> SKIP THE STATE '''
            if spf.is_board_can_not_win(new_board, list_check_point):
                continue
            ''' IF ALL BOXES ARE STUCK --> SKIP THE STATE '''
            if spf.is_all_boxes_stuck(new_board, list_check_point):
                continue

            ''' MAKE NEW STATE '''
            new_state = spf.state(new_board, now_state, list_check_point)
            ''' CHECK WHETHER THE NEW STATE IS GOAL OR NOT '''
            if spf.check_win(new_board, list_check_point):
                print("Found win")
                return (new_state.get_line(), len(list_state))
            
            ''' APPEND NEW STATE TO VISITED LIST AND TRAVERSED LIST '''
            list_state.append(new_state)
            list_visit.append(new_state)

            ''' COMPUTE THE TIMEOUT '''
            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return []
    ''' SOLUTION NOT FOUND '''
    print("Not Found")
    return []

def DFS_search(board, list_check_point):
    start_time = time.time()
    ''' BFS SEARCH SOLUTION '''
    ''' IF START BOARD IS GOAL OR DON'T HAVE CHECK POINT '''
    if spf.check_win(board,list_check_point):
        print("Found win")
        return [board]
    ''' INITIALIZE START STATE '''
    start_state = spf.state(board, None, list_check_point)
    ''' INITIALIZE 2 LISTS USED FOR BFS SEARCH '''
    list_state = [start_state]
    list_visit = [start_state]
    ''' LOOP THROUGH VISITED LIST '''
    global num_states_visited
    num_states_visited = 0
    while len(list_visit) != 0:
        num_states_visited+=1
        ''' GET NOW STATE TO SEARCH '''
        now_state = list_visit.pop()
        ''' GET THE PLAYER'S CURRENT POSITION '''
        cur_pos = spf.find_position_player(now_state.board)
        ''' 
        THIS WILL PRINT THE STEP-BY-STEP IMPLEMENTATION OF HOW THE ALGORITHM WORKS, 
        UNCOMMENT TO USE IF NECCESSARY 
        '''
        '''
        time.sleep(1)
        clear = lambda: os.system('cls')
        clear()
        print_matrix(now_state.board)
        print("State visited : {}".format(len(list_state)))
        print("State in queue : {}".format(len(list_visit)))
        '''

        ''' GET LIST POSITION THAT PLAYER CAN MOVE TO '''
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)
        print(list_can_move)
        num_shuffles = 23

        for _ in range(num_shuffles):
            random.shuffle(list_can_move)
        ''' MAKE NEW STATES FROM LIST CAN MOVE '''
        for next_pos in list_can_move:
            ''' MAKE NEW BOARD '''
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
            ''' IF THIS BOARD DON'T HAVE IN LIST BEFORE --> SKIP THE STATE '''
            if spf.is_board_exist(new_board, list_state):
                continue
            ''' IF ONE OR MORE BOXES ARE STUCK IN THE CORNER --> SKIP THE STATE '''
            if spf.is_board_can_not_win(new_board, list_check_point):
                continue
            ''' IF ALL BOXES ARE STUCK --> SKIP THE STATE '''
            if spf.is_all_boxes_stuck(new_board, list_check_point):
                continue

            ''' MAKE NEW STATE '''
            new_state = spf.state(new_board, now_state, list_check_point)
            ''' CHECK WHETHER THE NEW STATE IS GOAL OR NOT '''
            if spf.check_win(new_board, list_check_point):
                print("Found win")
                return (new_state.get_line(), len(list_state))
            
            ''' APPEND NEW STATE TO VISITED LIST AND TRAVERSED LIST '''
            list_state.append(new_state)
            list_visit.append(new_state)

            ''' COMPUTE THE TIMEOUT '''
            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return []
    ''' SOLUTION NOT FOUND '''
    print("Not Found")
    return []

def ID_search(board, list_check_point):
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
    ''' DFS SEARCH SOLUTION WITH DEPTH LIMIT '''
    ''' IF START BOARD IS GOAL OR DON'T HAVE CHECK POINT '''
    if spf.check_win(board, list_check_point):
        print("Found win")
        return [board]
    
    ''' INITIALIZE START STATE '''
    start_state = spf.state(board, None, list_check_point)
    ''' INITIALIZE 2 LISTS USED FOR DFS SEARCH '''
    list_state = [start_state]
    list_visit = [start_state]
    ''' LOOP THROUGH VISITED LIST '''
    global num_states_visited
    num_states_visited = 0
    
    while len(list_visit) != 0:
        num_states_visited += 1
        ''' GET NOW STATE TO SEARCH '''
        now_state = list_visit.pop()
        ''' GET THE PLAYER'S CURRENT POSITION '''
        cur_pos = spf.find_position_player(now_state.board)
        ''' GET LIST POSITION THAT PLAYER CAN MOVE TO '''
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)
        print(list_can_move)
        num_shuffles = 23

        for _ in range(num_shuffles):
            random.shuffle(list_can_move)
        
        ''' MAKE NEW STATES FROM LIST CAN MOVE '''
        for next_pos in list_can_move:
            ''' MAKE NEW BOARD '''
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
            ''' IF THIS BOARD DON'T HAVE IN LIST BEFORE --> SKIP THE STATE '''
            if spf.is_board_exist(new_board, list_state):
                continue
            ''' IF ONE OR MORE BOXES ARE STUCK IN THE CORNER --> SKIP THE STATE '''
            if spf.is_board_can_not_win(new_board, list_check_point):
                continue
            ''' IF ALL BOXES ARE STUCK --> SKIP THE STATE '''
            if spf.is_all_boxes_stuck(new_board, list_check_point):
                continue

            ''' MAKE NEW STATE '''
            new_state = spf.state(new_board, now_state, list_check_point)
            ''' CHECK WHETHER THE NEW STATE IS GOAL OR NOT '''
            if spf.check_win(new_board, list_check_point):
                print("Found win")
                return (new_state.get_line(), len(list_state))

            ''' APPEND NEW STATE TO VISITED LIST AND TRAVERSED LIST '''
            list_state.append(new_state)
            list_visit.append(new_state)

            ''' COMPUTE THE TIMEOUT '''
            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []
        
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return []
        
        ''' Check if depth limit is reached '''
        if now_state.depth < max_depth:
            continue
    
    ''' SOLUTION NOT FOUND '''
    print("Not Found")
    return []

def Dijkstra_search(board, list_check_point):
    start_time = time.time()

    if spf.check_win(board, list_check_point):
        print("Found win")
        return [board]

    start_state = spf.state(board, None, list_check_point)
    priority_queue = [(0, start_state)]  # (cost, state)
    visited_states = set()
    global num_states_visited
    num_states_visited = 0

    while priority_queue:
        num_states_visited += 1
        cost, now_state = heapq.heappop(priority_queue)
        cur_pos = spf.find_position_player(now_state.board)


        list_can_move = spf.get_next_pos(now_state.board, cur_pos)
        random.shuffle(list_can_move)

        for next_pos in list_can_move:
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
        
            if spf.is_board_exist(new_board, visited_states):
                continue
        
            if spf.is_board_can_not_win(new_board, list_check_point) or spf.is_all_boxes_stuck(new_board, list_check_point):
                continue
        
            new_state = spf.state(new_board, now_state, list_check_point)
        
            if spf.check_win(new_board, list_check_point):
                print("Found win")
                return (new_state.get_line(), len(visited_states))
        
            visited_states.add(new_state)
            heapq.heappush(priority_queue, (cost + 1, new_state))
        
            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []

    print("Not Found")
    return []

def number_states_visited():
    return num_states_visited   
