import pygame
from node import draw_square_grid, draw_triangle_grid, Node

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GREY = (128, 128, 128)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)


class Grid: # parent class, contains default square grid
    def __init__(self, rows, width):
        self.rows = rows
        self.width = width
        self.grid = []
        self.start = None
        self.end = None
        self.create_grid()

    def create_grid(self): # makes a square grid
        self.grid = []
        spacing = self.width // self.rows
        for i in range(self.rows):
            row = []
            for j in range(self.rows):
                row.append(Node(i, j, spacing, self.rows))
            self.grid.append(row)

    def mousepos(self, rows, width):
        pos = pygame.mouse.get_pos()  # pos = (x, y) mouse position
        y, x = pos  # get value of x and y from the mouse position
        spacing = width // rows
        row = y // spacing  # get row from y coordinate
        col = x // spacing  # get col from x coordinate
        return row, col

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (0, 0, self.width, self.width))
        # Paint over everything from the last frame
        for row in self.grid:
            for node in row:
                node.draw(screen)
        draw_square_grid(screen, self.rows, self.width)
        pygame.display.update()

    def check_adjacent_nodes(self):
        for row in self.grid:
            for node in row:
                node.update_neighbors(self.grid)

    def reset(self):
        for row in self.grid:
            for node in row:
                node.update_neighbors(self.grid)
                if node.isopen() or node.ispath() or node.isclosed() or node.ispath2():
                    node.makeplain()
        if self.start:
            self.start.makestart()
        if self.end:
            self.end.makeend()

    def clear(self):
        for row in self.grid:
            for node in row:
                node.makeplain()


class Triangle(Grid):
    def create_grid(self):
        self.grid = []
        spacing = self.width // self.rows
        for i in range(self.rows):
            row = []
            for j in range(self.rows):
                row.append(TriangleNode(i, j, spacing, self.rows))
            self.grid.append(row)

    def mousepos(self, rows, width):
        pos = pygame.mouse.get_pos()  # pos = (x, y) mouse position
        y, x = pos  # get value of x and y from the mouse position
        spacing = width // rows
        row = y // spacing  # get row from y coordinate
        col = x // spacing  # get col from x coordinate
        return row, col

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (0, 0, self.width, self.width))
        # paint over everthing on the last frame
        for row in self.grid:  # for every row(array) within grid
            for node in row:  # for every node within that row(array)
                node.draw(screen)  # draw the node onto the screen

        draw_triangle_grid(screen, self.rows, self.width)
        pygame.display.update()






class TriangleNode(Node):

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.get_triangle_points())

    def get_triangle_points(self):
        if self.row+1 == self.totalrows and (self.row + self.col) % 2 != 0:
            # Up-facing edge triangle, so it doesn't get in way of side panel
            return [
                (self.x, self.y + self.width),  # Bottom-left
                (self.x + self.width, self.y + self.width),  # Bottom-right
                (self.x + self.width, self.y)  # Top-center
            ]
        elif self.row+1 == self.totalrows and (self.row + self.col) % 2 == 0:
            # down-facing edge triangle
            return [
                (self.x, self.y),  # Top-left
                (self.x + self.width, self.y),  # Top-right
                (self.x + self.width, self.y + self.width)  # Bottom-center
            ]
        elif (self.row + self.col) % 2 != 0:
            # Up-facing triangle
            return [
                (self.x, self.y + self.width),  # Bottom-left
                (self.x + self.width*2, self.y + self.width),  # Bottom-right
                (self.x + self.width, self.y)  # Top-center
            ]
        else:
            # Down-facing triangle
            return [
                (self.x, self.y),  # Top-left
                (self.x + self.width*2, self.y),  # Top-right
                (self.x + self.width, self.y + self.width)  # Bottom-center
            ]

    def update_neighbors(self, grid):
        self.neighbors = [] #create array for neighbors to go into, stored as an attribute

        if (self.row + self.col) % 2 == 0:
            #triangle points downwards
            if self.row > 0 and not grid[self.row - 1][self.col].isblock():  # up
                self.neighbors.append(grid[self.row - 1][self.col])  # is node above available

            #if self.col < self.totalrows - 1 and not grid[self.row][self.col + 1].isblock():  # right
                #self.neighbors.append(grid[self.row][self.col + 1])  # is node right available

            if self.row < self.totalrows - 1 and not grid[self.row + 1][self.col].isblock():  # down
                self.neighbors.append(grid[self.row + 1][self.col])  # is node below available

            if self.col > 0 and not grid[self.row][self.col - 1].isblock():  # left
                self.neighbors.append(grid[self.row][self.col - 1])  # is node left available

        else:
            #if triangle points up
            if self.col < self.totalrows - 1 and not grid[self.row][self.col + 1].isblock():  # right
                self.neighbors.append(grid[self.row][self.col + 1])  # is node right available

            if self.row > 0 and not grid[self.row - 1][self.col].isblock():  # up
                self.neighbors.append(grid[self.row - 1][self.col])  # is node above available

            if self.row < self.totalrows - 1 and not grid[self.row + 1][self.col].isblock():  # down
                self.neighbors.append(grid[self.row + 1][self.col])  # is node below available

