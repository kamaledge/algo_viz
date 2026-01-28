from algo_viz.decorators import visualize

@visualize()
def climb_stairs(n):
    dp = [0] * (n + 1)
    dp[0], dp[1] = 1, 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]

n = 10
print(climb_stairs(n))