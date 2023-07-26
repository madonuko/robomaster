def init_r():
    robot_ctrl.set_mode(rm_define.robot_mode_free)
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)
    vision_ctrl.set_marker_detection_distance(3)
    vision_ctrl.marker_detection_color_set(rm_define.marker_detection_color_red)
    gun_ctrl.set_fire_count(1)
    gimbal_ctrl.set_rotate_speed(540)

def init_b():
    robot_ctrl.set_mode(rm_define.robot_mode_free)
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)
    vision_ctrl.set_marker_detection_distance(3)
    vision_ctrl.marker_detection_color_set(rm_define.marker_detection_color_blue)
    gun_ctrl.set_fire_count(1)
    gimbal_ctrl.set_rotate_speed(540)

result_position = []

OP_MAP = {
    50: '+',
    52: '/',
    43: '*',
    51: '-'
}

OP_REV_MAP = {
    '1': 11,
    '2': 12,
    '3': 13,
    '4': 14,
    '5': 15,
    '6': 16,
    '7': 17,
    '8': 18,
    '9': 19,
    '0': 10,
    '+': 50,
    '/': 52,
    '*': 43,
    '-': 51,
}


def eval(tokens):
    if len(tokens) == 1:
        return int(tokens[0])
    i = 0
    for token in tokens:
        if token == '*':
            return eval(tokens[:i-1] + [tokens[i-1]*tokens[i+1]] + tokens[i+2:])
        if token == '/':
            if tokens[i-1] % tokens[i+1] == 0:
                return eval(tokens[:i-1] + [tokens[i-1]//tokens[i+1]] + tokens[i+2:])
            return 0
        i += 1
    i = 0
    for token in tokens:
        if token == '+':
            return eval(tokens[:i-1] + [tokens[i-1]+tokens[i+1]] + tokens[i+2:])
        if token == '-':
            return eval(tokens[:i-1] + [tokens[i-1]-tokens[i+1]] + tokens[i+2:])
        i += 1


def set(a):
    new = []
    for x in a:
        if x not in new:
            new.append(x)
    return new

def _h24(prevs, arr):
    global ops
    global found
    x = 0
    for op in ops:
        i = 0
        for a in arr:
            new = prevs + [op, a]
            if eval(new) == 24:
                found = new
                return True
            if _h24(new, arr[:i] + arr[i+1:]):
                return True
            i += 1
        x += 1
    i = 0
    for a in arr:
        new = prevs[:]
        new[-1] = prevs[-1]*10+a
        if eval(new) == 24:
            found = new
            return True
        if _h24(new, arr[:i] + arr[i+1:]):
            return True
        i += 1
    return False


def sort_h24(detected):
    global ops
    global found
    ops = [OP_MAP[x] for x in detected if x >= 20]
    nums = [x - 10 for x in detected if x <= 20]
    i = 0
    for n in nums:
        if _h24([n], nums[:i] + nums[i+1:]):
            break
        i += 1
    if found != []:
        return [str(token) for token in found]
    print("oops, no h24 found")
    return sort_h24(get_marker_infos(5))


def get_marker_infos(num: int = -1):
    result = []
    retrive = {}
    markers = []
    while True:
        result = vision_ctrl.get_marker_detection_info()
        if len(result) == (1 + num * 5):
            break
        print("fail: only " + str((len(result) - 1)/5) + " tags detected")
    i = 0
    markers = []
    while i != num:
        retrive[result[1 + i * 5]] = [result[2 + i * 5], result[3 + i * 5], result[4 + i * 5], result[5 + i * 5]]
        markers.append(result[1 + i * 5])
        i= i + 1
    global result_position
    i = 0
    result_position = []
    while i != num:
        i = i + 1
        cache_id = 0
        cache_value = 0
        for k in markers:
            if cache_value < retrive[k][0]:
                cache_id = k
                cache_value = retrive[k][0]
        result_position.append(cache_id)
        del markers[markers.index(cache_id)]
    return retrive

def getMarkerID():
    list_Cache = []
    list_Maker_ID_Data = []
    variable_Sequence = 0
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)
    vision_ctrl.marker_detection_color_set(rm_define.marker_detection_color_red)
    while not len(list_Cache) == 26:
        list_Cache = RmList(vision_ctrl.get_marker_detection_info())
    variable_Sequence = 2
    while not variable_Sequence > 22:
        list_Maker_ID_Data.append(list_Cache[variable_Sequence])
        variable_Sequence = variable_Sequence + 5
    return list_Maker_ID_Data
    
distance = 0
def shoot_energy(ID: int = -1):
    global result_position
    global distance
    print(distance)
    yaw_angle = math.asin(24 / distance) / math.pi * 180 + 3
    pitch_angle = (math.atan((-9 * ID + 18) / math.sqrt(distance * distance - 625)) / math.pi * 180) 
    print(pitch_angle)
    print(yaw_angle)
    gimbal_ctrl.angle_ctrl(pitch_angle, yaw_angle)
    time.sleep(0.1)
    gun_ctrl.fire_once()
    time.sleep(0.1)

def start():
    print("point -z")
    init_r()
    print("x")
    global distance
    global found
    global table
    found = []
    res = get_marker_infos(5)
    print("1")
    vision_ctrl.detect_marker_and_aim(result_position[2])
    print("2")
    res = get_marker_infos(5)
    print(res)
    print(result_position)
    distance = res[result_position[2]][2] * -110.7726 + 67.539
    print("4")
    gimbal_ctrl.angle_ctrl(0,0)
    res = get_marker_infos(5)
    seq = sort_h24(res)
    #res = get_marker_infos(5)
    #print("point a")
    #a = sort_h24(res)
    print("a")
    if not seq:
        res = get_marker_infos(5)
        seq = sort_h24(res)
    #print("point b")
    #vision_ctrl.detect_marker_and_aim(result_position[2])
    #print("point c")
    #distance = res[result_position[2]][2] * -110.7726 + 67.539
    #gimbal_ctrl.angle_ctrl(0,0)
    for i in seq:
        print(i)
        shoot_energy(result_position.index(OP_REV_MAP[i]))
    print(seq)
    print(get_marker_infos(5))
