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



import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):
    

    def best_seam(self, dp=True):
        seam = []
        if dp == True:
            dp = self.dp_seam()
            seam.append((dp[0], self.width - 1))
            for i in range(self.width - 1, 0, -1):
                if dp[i] == dp[i - 1] + 1:
                    seam.append((dp[i] - 1, i - 1))
                elif dp[i] == dp[i - 1]:
                    seam.append((dp[i], i - 1))
                else:
                    seam.append((dp[i] + 1, i - 1))
        else:
            seam = self.naive_seam()
        return seam

    def dp_seam(self):
        dp = [0] * self.width
        for i in range(1, self.height):
            for j in range(self.width):
                if j == 0:
                    dp[j] = min(dp[j], dp[j + 1]) + self.energy(j, i)
                elif j == self.width - 1:
                    dp[j] = min(dp[j], dp[j - 1]) + self.energy(j, i)
                else:
                    dp[j] = min(dp[j], dp[j - 1], dp[j + 1]) + self.energy(j, i)
        return dp

    def naive_seam(self):
        seam = []
        for i in range(self.height):
            min_energy = float('inf')
            min_index = 0
            for j in range(self.width):
                if self.energy(j, i) < min_energy:
                    min_energy = self.energy(j, i)
                    min_index = j
            seam.append((min_index, i))
        return seam


    def remove_best_seam(self):
        self.remove_seam(self.best_seam())