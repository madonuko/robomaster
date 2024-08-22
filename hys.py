# this assumes that we cannot use each num more than once


def enumerate(ls):
    arr = []
    i = 0
    for n in ls:
        arr.append((i, n))
        i += 1
    return arr


def try_find_except(n, nums, without):
    start = 0
    while True:
        single = nums.index(n, start)
        if single not in without:
            return single
        start = single + 1


def _add(nums):
    # try `1x + 1y`
    try:
        one1 = nums.index(1)
        one2 = nums.index(1, one1 + 1)
        remain = [0, 1, 2, 3]
        remain.remove(one1)
        remain.remove(one2)
        assert nums[remain[0]] + nums[remain[1]] == 4
        #       1         x              +  1         y
        return [one1 + 1, remain[0] + 1, 0, one2 + 1, remain[1] + 1]
    except (ValueError, AssertionError):
        pass
    # try `1x + y`
    try:
        one = nums.index(1)
        for i, n in enumerate(nums):
            if i == one:
                continue
            try:
                left = try_find_except(14 - n, nums, [i, one])
                #       1        x           +  y
                return [one + 1, left + 1, 0, i + 1]
            except ValueError:
                continue
    except ValueError:
        pass
    # try `2x + y`
    try:
        two = nums.index(2)
        for i, n in enumerate(nums):
            if i == two:
                continue
            try:
                left = try_find_except(4 - n, nums, [i, two])
                #       2        x           +  y
                return [two + 1, left + 1, 0, i + 1]
            except ValueError:
                continue
    except ValueError:
        pass
    print(f"add: {nums} don't contain 1/2 => impossible")
    return []


def _minus(nums):
    try:
        two = nums.index(2)
        for i, n in enumerate(nums):
            if i == two or n >= 6:
                continue
            try:
                left = try_find_except(n + 4, nums, [i, two])
                return [two + 1, left + 1, 0, i + 1]
            except ValueError:
                continue
    except ValueError:
        pass
    try:
        three = nums.index(3)
        for i, n in enumerate(nums):
            if i == three or n < 6:
                continue
            try:
                left = try_find_except(n - 6, nums, [i, three])
                return [three + 1, left + 1, 0, i + 1]
            except ValueError:
                continue
    except ValueError:
        pass
    try:
        for lefti1, leftn1 in enumerate(nums):
            try:
                lefti2 = nums.index(leftn1 + 2)
            except ValueError:
                continue
            remain = [0, 1, 2, 3]
            remain.remove(lefti1)
            remain.remove(lefti2)
            if nums[remain[0]] - nums[remain[1]] == 4:
                righti1 = remain[1]
                righti2 = remain[0]
            elif nums[remain[1]] - nums[remain[0]] == 4:
                righti1 = remain[0]
                righti2 = remain[1]
            else:
                continue
            return [lefti2 + 1, righti2 + 1, 0, lefti1 + 1, righti1 + 1]
    except ValueError:
        pass
    try:
        for lefti1, leftn1 in enumerate(nums):
            try:
                lefti2 = nums.index(leftn1 + 3)
            except ValueError:
                continue
            remain = [0, 1, 2, 3]
            remain.remove(lefti1)
            remain.remove(lefti2)
            if nums[remain[0]] - nums[remain[1]] == 6:
                righti1 = remain[0]
                righti2 = remain[1]
            elif nums[remain[1]] - nums[remain[0]] == 6:
                righti1 = remain[1]
                righti2 = remain[0]
            else:
                continue
            return [lefti2 + 1, righti2 + 1, 0, lefti1 + 1, righti1 + 1]
    except ValueError:
        pass
    print("minus: somehow impossible?")
    return []


def _mul(nums):
    counts = [[], [], [], [], [], [], [], [], [], []]
    for i, n in enumerate(nums):
        counts[n].append(i + 1)
    if any(counts[1]) and len(counts[2]) >= 2:
        return [counts[1][0], counts[2][0], 0, counts[2][1]]
    if any(counts[3]) and any(counts[8]):
        return [counts[8][0], 0, counts[3][0]]
    if any(counts[4]) and any(counts[6]):
        return [counts[6][0], 0, counts[4][0]]
    print(f"mul: {counts=} => impossible")
    return []


def _div(nums):
    DIV_TABLE = [
        [],
        [],
        [4, 8],
        [7, 2],
        [9, 6],
        [1, 2, 0],
        [1, 4, 4],
        [1, 6, 8],
        [1, 9, 2],
        [2, 1, 6],
    ]
    for i, n in enumerate(nums):
        if n < 2:
            continue
        arr = DIV_TABLE[n]
        try:
            first = nums.index(arr[0])
            second = nums.index(arr[1])
            if n > 5:
                third = nums.index(arr[2])
                return [first + 1, second + 1, third + 1, 0, i + 1]
            return [first + 1, second + 1, 0, i + 1]
        except ValueError:
            continue


def hys(op, nums):
    try:
        first = nums.index(2) + 1
        second = nums.index(4) + 1
        return [first, second]
    except ValueError:
        pass
    if op == "+":
        return _add(nums)
    elif op == "-":
        return _minus(nums)
    elif op == "*":
        return _mul(nums)
    else:
        return _div(nums)


op = "-"  # assume at position 0
nums = [9, 9, 7, 5]
ans = hys(op, nums)
_in = [op] + nums
print(f"{ans} => {[_in[x] for x in ans]}")
