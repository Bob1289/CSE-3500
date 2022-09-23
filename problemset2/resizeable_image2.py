
def naive_seam(self):
    coord = []
    min_energy = float('inf')
    for i in range(self.width):
        energy = self.energy(i, 0)
        coord.append((i, 0))
        for j in range(1, self.height):
            if i == 0:
                if self.energy(i, j) < self.energy(i+1, j):
                    energy += self.energy(i, j)
                    coord.append((i, j))
                else:
                    energy += self.energy(i+1, j)
                    coord.append((i+1, j))
                    i += 1
            elif i == self.width - 1:
                if self.energy(i, j) < self.energy(i-1, j):
                    energy += self.energy(i, j)
                    coord.append((i, j))
                else:
                    energy += self.energy(i-1, j)
                    coord.append((i-1, j))
                    i -= 1
            else:
                if self.energy(i, j) < self.energy(i-1, j) and self.energy(i, j) < self.energy(i+1, j):
                    energy += self.energy(i, j)
                    coord.append((i, j))
                elif self.energy(i-1, j) < self.energy(i+1, j):
                    energy += self.energy(i-1, j)
                    coord.append((i-1, j))
                    i -= 1
                else:
                    energy += self.energy(i+1, j)
                    coord.append((i+1, j))
                    i += 1
        if energy < min_energy:
            min_energy = energy
            min_coord = coord
        coord = []
    return min_coord

    
def naive_seam_recursion(self):
    coord = []
    min_energy = float('inf')
    for i in range(self.width): # iterate through the width
        energy = self.energy(i, 0) # set energy to the energy of the pixel
        coord = self.naive_seam_recursion_helper(i, 0, energy, [(i, 0)]) # call the helper function
        if coord[-1][1] == self.height - 1: # if we are at the bottom row
            if coord[-1][0] < min_energy: # if the energy of the seam is less than the minimum energy
                min_energy = coord[-1][0] # set the minimum energy to the energy of the seam
                min_coord = coord # set the minimum coordinates to the coordinates of the seam
    return min_coord # return the minimum coordinates
    # The runtime of this function should be O(n^3) where n is the height of the image.
def naive_seam_recursion_helper(self, x, y, energy, coord):
    if y == self.height - 1:
        return coord
    else:
        if x == 0:
            if self.energy(x, y+1) < self.energy(x+1, y+1):
                energy += self.energy(x, y+1)
                coord.append((x, y+1))
                return self.naive_seam_recursion_helper(x, y+1, energy, coord)
            else:
                energy += self.energy(x+1, y+1)
                coord.append((x+1, y+1))
                return self.naive_seam_recursion_helper(x+1, y+1, energy, coord)
        elif x == self.width - 1:
            if self.energy(x-1, y+1) < self.energy(x, y+1):
                energy += self.energy(x-1, y+1)
                coord.append((x-1, y+1))
                return self.naive_seam_recursion_helper(x-1, y+1, energy, coord)
            else:
                energy += self.energy(x, y+1)
                coord.append((x, y+1))
                return self.naive_seam_recursion_helper(x, y+1, energy, coord)
        else:
            if self.energy(x-1, y+1) < self.energy(x, y+1) and self.energy(x-1, y+1) < self.energy(x+1, y+1):
                energy += self.energy(x-1, y+1)
                coord.append((x-1, y+1))
                return self.naive_seam_recursion_helper(x-1, y+1, energy, coord)
            elif self.energy(x, y+1) < self.energy(x+1, y+1):
                energy += self.energy(x, y+1)
                coord.append((x, y+1))
                return self.naive_seam_recursion_helper(x, y+1, energy, coord)
            else:
                energy += self.energy(x+1, y+1)
                coord.append((x+1, y+1))
                return self.naive_seam_recursion_helper(x+1, y+1, energy, coord)

def naive_seam_recursion(self):
        coord = []
        coord.append((0, 0))
        return self.naive_seam_recursion_helper(coord)

def naive_seam_recursion_helper(self, coord):
    if coord[-1][1] == self.height - 1:
        return coord
    else:
        if coord[-1][0] == 0:
            if self.energy(coord[-1][0], coord[-1][1] + 1) < self.energy(coord[-1][0] + 1, coord[-1][1] + 1):
                coord.append((coord[-1][0], coord[-1][1] + 1))
            else:
                coord.append((coord[-1][0] + 1, coord[-1][1] + 1))
        elif coord[-1][0] == self.width - 1:
            if self.energy(coord[-1][0] - 1, coord[-1][1] + 1) < self.energy(coord[-1][0], coord[-1][1] + 1):
                coord.append((coord[-1][0] - 1, coord[-1][1] + 1))
            else:
                coord.append((coord[-1][0], coord[-1][1] + 1))
        else:
            if self.energy(coord[-1][0] - 1, coord[-1][1] + 1) < self.energy(coord[-1][0], coord[-1][1] + 1) and self.energy(coord[-1][0] - 1, coord[-1][1] + 1) < self.energy(coord[-1][0] + 1, coord[-1][1] + 1):
                coord.append((coord[-1][0] - 1, coord[-1][1] + 1))
            elif self.energy(coord[-1][0], coord[-1][1] + 1) < self.energy(coord[-1][0] + 1, coord[-1][1] + 1):
                coord.append((coord[-1][0], coord[-1][1] + 1))
            else:
                coord.append((coord[-1][0] + 1, coord[-1][1] + 1))
        return self.naive_seam_recursion_helper(coord)
        