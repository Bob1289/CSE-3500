def maxProfit(profits, k):
  n = len(profits)
  dp = [0] * n
  day = [0] * n

  # Initialize the maximum profit and chosen day for the first day
  dp[0] = profits[0]
  day[0] = 0

  for i in range(1, n):
    # Find the maximum profit up to day i, considering the restriction of waiting k days between profits
    maxProfit = profits[i]
    chosenDay = i
    for j in range(i-k, -1, -1):
      if profits[i] + dp[j] > maxProfit:
        maxProfit = profits[i] + dp[j]
        chosenDay = j
    dp[i] = max(dp[i-1], maxProfit)
    day[i] = chosenDay

  # dp[n-1] contains the maximum profit for the entire list of days
  # day[n-1] contains the chosen day for the last day
  return dp[n-1], day

profits = [9,3,-2,1,2,3,1,10]
k = 2

maxProfit, chosenDays = maxProfit(profits, k)
print(maxProfit)
print(chosenDays)