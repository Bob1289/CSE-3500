

if __name__ == '__main__':
    # Create a 2^k x 2^k board
    k = int(input('Enter a value for k: '))
    board = [[0 for _ in range(2**k)] for _ in range(2**k)]

    # remove the top left corner square
    board[0][0] = -1
    def print_board(board):
        for row in board:
            print(row)
        print()

    # You are given a 2^kx2^k board of squares (e.g. a chess board) with the top left square removed.
    # Prove, by giving a divide-and-conquer algorithm or argument, that you can exactly cover the
    # entire board with L-shaped pieces (each covering 3 squares).
    # You may assume that k is a positive integer.
    # Start by splitting the board into 4 quadrants, and then recursively solve the problem for each
    # quadrant. Place a L-shaped piece in the middle of the board and each quadrant. From there, you
    # can recursively solve the problem for each quadrant. You will need to place a L-shaped piece in
    # the middle of each quadrant. Continue this process until you have solved the problem for a 2x2
    # board. You will need to place a L-shaped piece in the middle of the board with the open side
    # facing towards the top left corner. You can then place
    # the remaining L-shaped pieces to cover the entire board. The oreintation of the L-shaped pieces
    # does not matter. There cannot be any overlapping L-shaped pieces. Mark each L-shaped piece with
    # a unique number. Do not remove any squares from the board. Print the board after each recursive
    # call. You may assume that k is a positive integer.
    def fill_board(board, row, col, size, count):
        if size == 2:
            for i in range(row, row + size):
                for j in range(col, col + size):
                    if board[i][j] == 0:
                        board[i][j] = count 
            return

        # place L-shaped piece in the middle of the board
        board[row + size // 2][col + size // 2] = count
        board[row + size // 2 - 1][col + size // 2] = count
        board[row + size // 2][col + size // 2 - 1] = count

        # recursively solve the problem for each quadrant
        fill_board(board, row, col, size // 2, count + 1)
        fill_board(board, row, col + size // 2, size // 2, count + 1)
        fill_board(board, row + size // 2, col, size // 2, count + 1)
        fill_board(board, row + size // 2, col + size // 2, size // 2, count + 1)

    fill_board(board, 0, 0, 2**k, 1)
    print_board(board)

    

    

        
    


    

