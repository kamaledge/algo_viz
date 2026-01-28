
from algo_viz.decorators import visualize


@visualize()
def two_sum(nums, target):
    l, r = 0, len(nums) - 1
    while l < r:
        s = nums[l] + nums[r]
        if s == target:
            return l, r
        elif s < target:
            l += 1
        else:
            r -= 1
nums = [1,2,5,6,7,9,13]
target = 11

two_sum(nums, target)