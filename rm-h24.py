table = {
	11: rm_define.marker_number_one,
	12: rm_define.marker_number_two,
	13: rm_define.marker_number_three,
	14: rm_define.marker_number_four,
	15: rm_define.marker_number_five,
	16: rm_define.marker_number_six,
	17: rm_define.marker_number_seven,
	18: rm_define.marker_number_eight,
	19: rm_define.marker_number_nine,
	20: rm_define.IDK_MAYBE_ADD,
	21: rm_define.IDK_MAYBE_SUB,
	22: rm_define.IDK_MAYBE_MUL,
	23:	rm_deifne.IDK_MAYBE_DIV,
}

OP_MAP = {
	20: '+',
	21: '-',
	22: '*',
	23: '//'
}


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


def _h24(prevs, arr, ops):
	global found
	for i, op in enumerate(set(ops)):
		op = OP_MAP[op]
		for i, a in enumerate(arr):
			new = f'{prevs}{op}{a}'
			if eval(new) == 24:
				found = new
				return True
			if _h24(new, arr[:i] + arr[i+1:], ops[:i] + ops[i+1:]):
				return True
	for i, a in enumerate(arr):
		new = f'{prevs}{a}'
		if eval(new) == 24:
			found = new
			return True
		if _h24(new, arr[:i] + arr[i+1:], ops):
			return True
	return False


def sort_h24(detected):
	ops = [x for x in detected if x >= 20]
	nums = [x - 10 for x in detected if x != 20]
	for i, n in enumerate(nums):
		if _h24(str(n), nums[:i] + nums[i+1:], ops):
			break
	if not any(found):
		print("oops, no h24 found")
		exit()
	return found


def start():
	global table
	detected = getMarkerID()
	sortedData = sort_h24(detected)
	for d in sortedData:
		vision_ctrl.detect_marker_and_aim(table[d])
		gun_ctrl.fire_once()
