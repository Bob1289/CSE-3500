import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self, dp=False): 
        if dp == True: # if we are using dynamic programming
            return self.dp_seam()
        else: # if we are not using dynamic programming
            return self.naive_seam_recursion()

    def dp_seam(self):
        coord = [] # initialize the list of coordinates
        dp = [[0 for i in range(self.width)] for j in range(self.height)] # create a 2D array of 0s

        for i in range(self.height): # iterate through the height
            for j in range(self.width): # iterate through the width
                if i == 0: # if we are at the top row
                    dp[i][j] = self.energy(j, i) # set the value of the 2D array to the energy of the pixel
                else: # if we are not at the top row
                    if j == 0: # if we are at the leftmost column
                        dp[i][j] = min(dp[i-1][j], dp[i-1][j+1]) # set the value of the 2D array to the minimum of the two pixels above it
                    elif j == self.width - 1: # if we are at the rightmost column
                        dp[i][j] = min(dp[i-1][j-1], dp[i-1][j]) # set the value of the 2D array to the minimum of the two pixels above it
                    else: # if we are in the middle
                        dp[i][j] = min(dp[i-1][j-1], dp[i-1][j], dp[i-1][j+1]) # set the value of the 2D array to the minimum of the three pixels above it
                    dp[i][j] += self.energy(j, i) # add the energy of the pixel to the value of the 2D array
                        
        start_index = dp[self.height-1].index(min(dp[self.height-1])) # find the index of the minimum value in the bottom row
        coord.append((start_index, self.height-1)) # add the coordinates of the minimum value to the list of coordinates

        while coord[-1][1] != 0: # while we are not at the top row
            i = coord[-1][1] # set i to the y coordinate of the last pixel in the list of coordinates
            j = coord[-1][0] # set j to the x coordinate of the last pixel in the list of coordinates
            
            if j == 0: # if we are at the leftmost column
                if dp[i-1][j] < dp[i-1][j+1]: # if the pixel above is less than the pixel to the right
                    coord.append((j, i-1)) # add the coordinates of the pixel above to the list of coordinates
                else: # if the pixel to the right is less than the pixel above
                    coord.append((j+1, i-1)) # add the coordinates of the pixel to the right to the list of coordinates
            elif j == self.width - 1: # if we are at the rightmost column
                if dp[i-1][j-1] < dp[i-1][j]: # if the pixel to the left is less than the pixel above
                    coord.append((j-1, i-1)) # add the coordinates of the pixel to the left to the list of coordinates
                else: # if the pixel above is less than the pixel to the left
                    coord.append((j, i-1)) # add the coordinates of the pixel above to the list of coordinates
            else: # if we are in the middle
                if dp[i-1][j-1] < dp[i-1][j] and dp[i-1][j-1] < dp[i-1][j+1]: # if the pixel to the left is less than the pixels above
                    coord.append((j-1, i-1)) # add the coordinates of the pixel to the left to the list of coordinates
                elif dp[i-1][j] < dp[i-1][j+1]: # if the pixel above is less than the pixel to the right
                    coord.append((j, i-1)) # add the coordinates of the pixel above to the list of coordinates
                else: # if the pixel to the right is less than the pixels above
                    coord.append((j+1, i-1)) # add the coordinates of the pixel to the right to the list of coordinates
        return coord[::-1] # return the list of coordinates in reverse order
        # The runtime of this function should be O(n^2) where n is the height of the image.

    def naive_seam_recursion(self):
        coord = [] # initialize the list of coordinates
        min_energy = float("inf") # set the minimum energy to infinity
        for i in range(self.width): # iterate through the width
            energy = self.energy(i, 0) # set energy to the energy of the pixel
            path = self.naive_seam_recursion_helper(i, 0, energy, []) # call the helper function
            if path[-1][1] == self.height - 1: # if we are at the bottom row
                if path[-1][2] < min_energy: # if the energy of the path is less than the minimum energy
                    min_energy = path[-1][2] # set the minimum energy to the energy of the path
                    coord = path # set the list of coordinates to the path
        return coord # return the list of coordinates
        # The runtime of this function should be O(n^3) where n is the height of the image.
    def naive_seam_recursion_helper(self, x, y, energy, path):
        if y == self.height - 1: # if we are at the bottom row
            return path + [(x, y, energy)] # return the path with the coordinates of the pixel and the energy of the path
        else: # if we are not at the bottom row
            path = path + [(x, y, energy)] # add the coordinates of the pixel and the energy of the path to the path
            if x == 0: # if we are at the leftmost column
                return min(self.naive_seam_recursion_helper(x, y+1, energy + self.energy(x, y+1), path), 
                            self.naive_seam_recursion_helper(x+1, y+1, energy + self.energy(x+1, y+1), path))
                # return the minimum of the two paths
            elif x == self.width - 1: # if we are at the rightmost column
                return min(self.naive_seam_recursion_helper(x-1, y+1, energy + self.energy(x-1, y+1), path), 
                            self.naive_seam_recursion_helper(x, y+1, energy + self.energy(x, y+1), path))
                # return the minimum of the two paths
            else: # if we are in the middle
                return min(self.naive_seam_recursion_helper(x-1, y+1, energy + self.energy(x-1, y+1), path), 
                            self.naive_seam_recursion_helper(x, y+1, energy + self.energy(x, y+1), path),
                            self.naive_seam_recursion_helper(x+1, y+1, energy + self.energy(x+1, y+1), path))
                # return the minimum of the three paths
        # The runtime of this function should be O(n^3) where n is the height of the image.
    
    def remove_best_seam(self):
        self.remove_seam(self.best_seam())



