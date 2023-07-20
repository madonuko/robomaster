####### ##    # ####### ####### ####### ##### ####### #######
   #    # #   #    #    ##   ## ##    #   #       ##      ##
   #    #  #  #    #    ####### #######   #      #       #
   #    #   # #    #    ##      ####      #    ##      ##
   #    #    ##    #    ##      ##  ### ##### ####### #######
# These code should be only used by the approved team/person by TNTprizz
# All rights reserved and Legal rights reserved
# 23-08-2021, TNTprizz
markers = []
# Base function
class BaseFunc():
    def get_marker_infos(num: int = -1):
        result = []
        retrive = {}
        global markers
        while len(result) != (1 + num * 5):
            result = vision_ctrl.get_marker_detection_info()
        i = 0
        while i != num:
            retrive[result[1 + i * 5]] = [result[2 + i * 5], result[3 + i * 5]]
            markers.append(result[1 + i * 5])
            i = i + 1
        return retrive
    # Base function
    def getSmallest():
        global markers
        val = 99
        for L in markers:
            if L < val and L > 10 and L < 20:
                val = L
        del markers[markers.index(val)]
        return val
# Do these all at the first time
def init():
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)
    vision_ctrl.marker_detection_color_set(rm_define.marker_detection_color_blue)
    chassis_ctrl.enable_stick_overlay()
    gimbal_ctrl.enable_stick_overlay()
# Shoot according to X and Y value of markers
def shoot_using_XY(X, Y):
    if X > 1 and Y > 1 and X < 0 and Y < 0:
        return False
    gun_ctrl.set_fire_count(1)
    gimbal_ctrl.set_rotate_speed(540)
    gimbal_ctrl.angle_ctrl((X - 0.5) * 96, (0.5 - Y) * 60)
    gun_ctrl.fire_once()
    time.sleep(0.1)

def shoot_energy():
    gimbal_ctrl.recenter()
    res = BaseFunc.get_marker_infos(5)
    media_ctrl.play_sound(rm_define.media_sound_scanning)
    led_ctrl.gun_led_on()
    for t in res:
        sort = BaseFunc.getSmallest()
        shoot_using_XY(res[sort][0], res[sort][1])
    time.sleep(1)

# Do these on start
def start():
    global markers
    init()
    robot_ctrl.set_mode(rm_define.robot_mode_free)
    led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 255, 0, 0, rm_define.effect_flash)
    led_ctrl.set_top_led(rm_define.armor_top_all, 255, 0, 0, rm_define.effect_flash)
    #gimbal_ctrl.angle_ctrl(0, 20)
    shoot_energy()
    if not vision_ctrl.check_condition(rm_define.cond_recognized_marker_letter_A):
        shoot_energy()
    gimbal_ctrl.recenter()
    media_ctrl.play_sound(rm_define.media_sound_recognize_success)

    
    
