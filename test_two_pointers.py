from algo_viz import visualize

@visualize()
def two_sum_test(nums, target):
    l, r = 0, len(nums) - 1
    while l < r:
        s = nums[l] + nums[r]
        if s == target:
            return l, r
        elif s < target:
            l += 1
        else:
            r -= 1
    return None

result = two_sum_test([1, 2, 3, 4, 5, 6, 7, 8, 9], 13)  # 4 + 9 = 13, but need to explore
print(f'Result: {result}')



