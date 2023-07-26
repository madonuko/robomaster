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
​
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
