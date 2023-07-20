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
OP_REV_MAP = {
	'1': rm_define.marker_number_one,
	'2': rm_define.marker_number_two,
	'3': rm_define.marker_number_three,
	'4': rm_define.marker_number_four,
	'5': rm_define.marker_number_five,
	'6': rm_define.marker_number_six,
	'7': rm_define.marker_number_seven,
	'8': rm_define.marker_number_eight,
	'9': rm_define.marker_number_nine,
	'+': rm_define.IDK_MAYBE_ADD,
	'-': rm_define.IDK_MAYBE_SUB,
	'*': rm_define.IDK_MAYBE_MUL,
	'/': rm_define.IDK_MAYBE_DIV,
}

OP_MAP = {
	20: '+',
	21: '-',
	22: '*',
	23: '/'
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


def eval(tokens):
	if len(tokens) == 1:
		return int(tokens[0])
	i = 0
	for token in tokens:
		if token == '*':
			return eval(tokens[:i-1] + [tokens[i-1]*tokens[i+1]] + tokens[i+2:])
		if token == '/':
			return eval(tokens[:i-1] + [tokens[i-1]//tokens[i+1]] + tokens[i+2:])
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
	i = 0
	for x in a:
		if a.index(x) == i:
			new.append(x)
		i += 1
	return new

def _h24(prevs, arr, ops):
	global found
	x = 0
	for op in set(ops):
		op = OP_MAP[op]

		i = 0
		for a in arr:
			new = prevs + [op, a]
			if eval(new) == 24:
				found = new
				return True
			if _h24(new, arr[:i] + arr[i+1:], ops[:i] + ops[i+1:]):
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
		if _h24(new, arr[:i] + arr[i+1:], ops):
			return True
		i += 1
	return False


def sort_h24(detected):
	ops = [x for x in detected if x >= 20]
	nums = [x - 10 for x in detected if x <= 20]
	i = 0
	for n in nums:
		if _h24([n], nums[:i] + nums[i+1:], ops):
			break
		i += 1
	if not any(found):
		print("oops, no h24 found")
		exit()
	res = ""
	for token in found:
		res += str(token)
	return res


def start():
	global found
	global table
	found = []
	detected = getMarkerID()
	sortedData = sort_h24(detected)
	for d in sortedData:
		vision_ctrl.detect_marker_and_aim(OP_REV_MAP[d])
		gun_ctrl.fire_once()
