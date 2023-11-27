import const as c
class user:
    def __init__(self, username, level, score):
        self.username = username
        self.level = level
        self.score = score
        
def is_exist(username):
    # 0: error, 1: not exist, 2: exist
    if username == '':
        return 0
    
    list_user = []
    with open(c.login_path+'\\user.txt', 'r') as file:
        list_user = file.readlines()
    for i in list_user:
        if username == i[:-1]:
            return 2
        
    return 1
    
def create(username):               
    with open(c.login_path+'user.txt', 'a') as file:
        file.writelines(username+'\n')

    with open(c.login_path+'detail.txt', 'a') as file:
        file.write(username+';')
        file.write(str(0)+',0;')
        for i in range(1,30):
            file.write(str(i)+',-1;')
        file.write('\n')
    
def get_user(username):
    if is_exist(username) == 0:
        return None
    elif is_exist(username) == 1:
        create(username)
        
    users_list = []
    with open(c.login_path+'detail.txt', 'r') as file:
        user_data = file.read().split('\n')  # mỗi người dùng được ngăn cách bởi dòng trắng
        for data in user_data:
            if data == '':
                continue
            user_info = data.split(';')  # Tách thông tin người dùng
            name = user_info[0]
            level = []
            score = []
            for i in range(1, 31):
                temp = user_info[i].split(',')
                level.append(temp[0])
                score.append(temp[1])
            users_list.append(user(name, level, score))
    for i in users_list:
        if i.username == username:
            return i
    return None

def update_user(user):
    return None