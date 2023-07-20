####### ##    # ####### ####### ####### ##### ####### #######
   #    # #   #    #    ##   ## ##    #   #       ##      ##
   #    #  #  #    #    ####### #######   #      #       #
   #    #   # #    #    ##      ####      #    ##      ##
   #    #    ##    #    ##      ##  ### ##### ####### #######
# These code should be only used by the approved team/person by TNTprizz
# All rights reserved and Legal rights reserved
# 07-20-2023, TNTprizz

def init_r():
    robot_ctrl.set_mode(rm_define.robot_mode_free)
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)
    vision_ctrl.set_marker_detection_distance(3)
    vision_ctrl.marker_detection_color_set(rm_define.marker_detection_color_red)
    gun_ctrl.set_fire_count(1)
    gimbal_ctrl.set_rotate_speed(540)
​
def init_b():
    robot_ctrl.set_mode(rm_define.robot_mode_free)
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)
    vision_ctrl.set_marker_detection_distance(3)
    vision_ctrl.marker_detection_color_set(rm_define.marker_detection_color_blue)
    gun_ctrl.set_fire_count(1)
    gimbal_ctrl.set_rotate_speed(540)
​
result_position = []

def get_marker_infos(num: int = -1):
    result = []
    retrive = {}
    markers = []
    while len(result) != (1 + num * 5):
        result = vision_ctrl.get_marker_detection_info()
        print("fail: only " + str(len(result)) + " tags detected")
    i = 0
    while i != num:
        retrive[result[1 + i * 5]] = [result[2 + i * 5], result[3 + i * 5], result[4 + i * 5], result[5 + i * 5]]
        markers.append(result[1 + i * 5])
        i= i + 1
    global result_position
    i = 0
    while i != num:
        i = i + 1
        cache_id = 0
        cache_value = 99
        for k in markers:
            if cache_value > retrive[k][0]:
                cache_id = k
                cache_value = retrive[k][0]
        result_position.append(cache_id)
        del markers[markers.index(cache_id)]
    return retrive
distance = 0
def shoot_energy(ID: int = -1):
    global result_position
    global distance
    yaw_angle = math.asin(18.7 / distance) / math.pi * 180
    pitch_angle = math.atan((9 * ID - 18) / math.sqrt(distance * distance - 660.49)) / math.pi * 180
    gimbal_ctrl.angle_ctrl(pitch_angle, yaw_angle)
    gun_ctrl.fire_once()
    time.sleep(0.1)
​
def start():
    init_r()
    global distance
    res = get_marker_infos(5)
    vision_ctrl.detect_marker_and_aim(result_position[2])
    distance = res[result_position[2]][2] * -110.7726 + 67.539
    gimbal_ctrl.angle_ctrl(0,0)
    """
    Here I am to explain how it works:
    [] [] [] [] []
    These are 5 tags, named 0(!), 1, 2, 3, 4 respectively, from left to right.
    For example to shoot tag 2, do this:
        shoot_energy(2) 
    and then [] [] [!] [] [] will occur.
    Btw the code above this message should not be edited. None of my business if you lose because of that.
    """
    shoot_energy(2)
    shoot_energy(3)
    shoot_energy(1)
    shoot_energy(4)
    shoot_energy(0)
    """
    These code will shoot the tags with the following sequence:
    [5] [3] [1] [2] [4]
    """