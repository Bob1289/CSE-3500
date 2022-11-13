# Given a n x n matrix that has different values in each square
# find the path has the largest sum from the top left to the bottom right.
# You can only move down, left, or right
# Do this in O(n^2) time

if __name__ == '__main__':
    matrix = [
        [1,2,3],
        [-100,5,6],
        [7,8,9]
        ]

    def find_path(grid):
        for i in range(len(grid)):
            for j in range(len(grid)):
                if j == 0:
                    grid[i][j] += max(grid[i-1][j], grid[i][j+1])
                    print(grid[i][j],i,j)
                elif j == len(grid)-1:
                    grid[i][j] += max(grid[i-1][j], grid[i][j-1])
                    print(grid[i][j],i,j)
                else:
                    grid[i][j] += max(grid[i-1][j], grid[i][j-1], grid[i][j+1])
                    print(grid[i][j],i,j)
        return grid[-1][-1]

    print(find_path(matrix))

    

