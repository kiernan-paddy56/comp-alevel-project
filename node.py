import pygame

def draw_square_grid(screen, rows, width): #for drawing our background grid lines
  spacing = width// rows #finds the spacing between the nodes/node width
  for i in range(rows+1):
    pygame.draw.line(screen, GREY,(0, i*spacing), (width,i*spacing)) #horizontal lines
    pygame.draw.line(screen, GREY,(i*spacing, 0), (i*spacing,width)) #verticle lines

def draw_triangle_grid(screen, rows, width):
  tri_side = width // rows  # triangle side length
  for i in range(rows+1):
    pygame.draw.line(screen, GREY,(0, i*tri_side), (width,i*tri_side)) #horizontal lines
  for i in range(rows//2):
    pygame.draw.line(screen, GREY, (0, 2*i * tri_side), (width-(2*i*tri_side), width))  # diagonal from left
    pygame.draw.line(screen, GREY, (width, 2 * i * tri_side), ((2 * i * tri_side), width))  # diagonal from right
    pygame.draw.line(screen, GREY, (2 * i * tri_side, 0), (width, width - (2 * i * tri_side)))  # diagonal from top
    pygame.draw.line(screen, GREY, (2 * i * tri_side, 0), (0, 2*i * tri_side))  # diagonal from top

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



class Node:

  def __init__(self, row, col, width, totalrows):
    self.row = row
    self.col = col
    self.x = row * width
    self.y = col * width #finds the position of the node given its coordinates and width
    self.color = WHITE #all nodes start as being white(empty space/ free block)
    self.width = width #width and height of the blocks
    self.neighbors = [] #array for all the neighbors of a node
    self.totalrows = totalrows

  def get_node_info_(self):
    array = [self.row, self.col, self.color]
    return array


  def getpos(self):
    return (self.row+0.5*self.width), (self.col+0.5*self.width)

  def isopen(self):
    return self.color == ORANGE #is node open

  def isclosed(self):
    return self.color == BLUE #is node closed

  def ispath(self):
    return self.color == PURPLE #is node open

  def isblock(self):
    return self.color == BLACK #is node a block

  def isstart(self):
    return self.color == GREEN #is node the start node

  def isend(self):
    return self.color == RED #is node the end node

  def ispath2(self):
    return self.color == MAGENTA #is node the end node

  def isplain(self):
    return self.color == WHITE # is node a plain node

  def makeopen(self):
    self.color = ORANGE #turn to opened

  def makeclose(self):
    self.color = BLUE #turn to closed

  def makeblock(self):
    self.color = BLACK #become a block

  def makestart(self):
    self.color = GREEN #chosen as start node

  def makeend(self):
    self.color = RED #chosen as end node

  def makepath2(self):
    self.color = MAGENTA #chosen as end node

  def makeplain(self):
    self.color = WHITE #switch back to plain node

  def makepath(self):
    self.color = PURPLE #for final path as optimal solution

  def draw(self, screen): #method we call when we want to draw node on the screen
    pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width))
    #only parameter needed to draw the node when we call it later will be screen
    #the rest of the parameters here are stored as atributes


  def update_neighbors(self, grid): #so we know all of the available neighbors to a node
    self.neighbors = [] #create array for neighbors to go into, stored as an attribute

    if self.row < self.totalrows -1 and not grid[self.row+1][self.col].isblock(): #down
      self.neighbors.append(grid[self.row+1][self.col]) #is node below available
      #we need the -1 as we start from 0 in rows so the last row is totalrows -1

    if self.row > 0 and not grid[self.row-1][self.col].isblock(): #up
      self.neighbors.append(grid[self.row-1][self.col]) #is node above available

    if self.col < self.totalrows -1 and not grid[self.row][self.col+1].isblock(): #right
      self.neighbors.append(grid[self.row][self.col+1]) #is node right available

    if self.col > 0 and not grid[self.row][self.col-1].isblock(): #left
      self.neighbors.append(grid[self.row][self.col-1]) #is node left available

    if self.col > 0 and self.row > 0 and not grid[self.row-1][self.col-1].isblock():
      #leftup
      self.neighbors.append(grid[self.row-1][self.col-1]) #is node leftup available

    if self.col > 0 and self.row < self.totalrows -1 and \
    not grid[self.row+1][self.col-1].isblock(): #leftdown
      self.neighbors.append(grid[self.row+1][self.col-1]) #is node leftdown available


    if self.row > 0 and self.col < self.totalrows -1 and \
    not grid[self.row-1][self.col+1].isblock(): #rightup
      self.neighbors.append(grid[self.row-1][self.col+1]) #is node righup available

    if self.row < self.totalrows -1 and self.col < self.totalrows -1 and\
    not grid[self.row+1][self.col+1].isblock(): #rightdown
      self.neighbors.append(grid[self.row+1][self.col+1]) #is node rightdown available
