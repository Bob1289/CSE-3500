# Similar to edit distance, we define a cost for removing a pixel to be energy(i, j) which
# corresponds to the energy of the pixel, or, the level of image disruption that would occur
# by removing pixel B[i, j]. Informally, the higher the energy, the more dissimilar the pixel is
# to its neighbors. The total cost is Ts =
# P
# (i,j)∈s
# energy(i, j) where s is the seam. The DP
# subproblem is, for each pixel (i, j), what is the lowest-energy seam that starts at the top row
# of the image, but ends at (i, j)?
# Let dp[i, j] be the solution to subproblem (i, j). Then, for a vertical seam, dp[i, j] =
# min(dp[i − 1, j − 1], dp[i, j − 1], dp[i + 1, j − 1]) + energy(i, j)

# The provided code assumes you are using Python3. In resizable image.py, implement a
# function best seam(self, dp=True) that returns a list of coordinates corresponding to the
# lowest-energy vertical seam to remove, e.g. [(5, 0), (5, 1), (4, 2), (5, 3), (6, 4)].
# The class ResizeableImage inherits from ImageMatrix. You should use the following components of ImageMatrix in your program:
# • self.energy(i,j) returns the energy of a pixel. This takes O(1) time, but the constant
# factor is large. If you call energy more than once on the same pixel, you should cache
# the result. You should still cache the energy for a pixel even if dp == False.
# • ‘self.width‘ and ‘self.height‘ are the width and height of the image.
# Your implementation may be either bottom-up or top-down. But either way, it must respect
# the argument dp, which indicates whether or not dynamic programming should be used. If
# dp == True, then you should either use memoization or store the subproblem values in a
# table for re-use. If dp == False, then you should naively recompute those subproblems
# test your code using test resizable image.py



import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self, dp=True):
        if dp == True:
            return self.dp_seam()
        else:
            return self.naive_seam()

    def dp_seam(self):
        coord = []
        dp = [[0 for i in range(self.width)] for j in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                if i == 0:
                    dp[i][j] = self.energy(j, i)
                else:
                    if j == 0:
                        dp[i][j] = min(dp[i-1][j], dp[i-1][j+1]) + self.energy(j, i)
                    elif j == self.width - 1:
                        dp[i][j] = min(dp[i-1][j-1], dp[i-1][j]) + self.energy(j, i)
                    else:
                        dp[i][j] = min(dp[i-1][j-1], dp[i-1][j], dp[i-1][j+1]) + self.energy(j, i)
        min_val = min(dp[self.height-1])
        min_index = dp[self.height-1].index(min_val)
        coord.append((min_index, self.height-1))
        for i in range(self.height-2, -1, -1):
            if min_index == 0:
                if dp[i][min_index] < dp[i][min_index+1]:
                    coord.append((min_index, i))
                else:
                    min_index += 1
                    coord.append((min_index, i))
            elif min_index == self.width - 1:
                if dp[i][min_index] < dp[i][min_index-1]:
                    coord.append((min_index, i))
                else:
                    min_index -= 1
                    coord.append((min_index, i))
            else:
                if dp[i][min_index] < dp[i][min_index-1] and dp[i][min_index] < dp[i][min_index+1]:
                    coord.append((min_index, i))
                elif dp[i][min_index-1] < dp[i][min_index+1]:
                    min_index -= 1
                    coord.append((min_index, i))
                else:
                    min_index += 1
                    coord.append((min_index, i))
        return coord

    def naive_seam(self):
        coord = []
        min_val = float('inf')
        for i in range(self.width):
            val = self.energy(i, 0)
            if val < min_val:
                min_val = val
                min_index = i
        coord.append((min_index, 0))
        for i in range(1, self.height):
            if min_index == 0:
                if self.energy(min_index, i) < self.energy(min_index+1, i):
                    coord.append((min_index, i))
                else:
                    min_index += 1
                    coord.append((min_index, i))
            elif min_index == self.width - 1:
                if self.energy(min_index, i) < self.energy(min_index-1, i):
                    coord.append((min_index, i))
                else:
                    min_index -= 1
                    coord.append((min_index, i))
            else:
                if self.energy(min_index, i) < self.energy(min_index-1, i) and self.energy(min_index, i) < self.energy(min_index+1, i):
                    coord.append((min_index, i))
                elif self.energy(min_index-1, i) < self.energy(min_index+1, i):
                    min_index -= 1
                    coord.append((min_index, i))
                else:
                    min_index += 1
                    coord.append((min_index, i))
        return coord



    
    def remove_best_seam(self):
        self.remove_seam(self.best_seam())