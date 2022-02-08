#from turtle import pos
import pygame, sys, time
import math
from queue import PriorityQueue

# nodes/cell colors
white = (250, 250, 250)
red = (201, 102, 87)
green = (99, 212, 139)
yellow = (245, 255, 140)
lightGreen = (173, 255, 202)
lightBlue = (99, 153, 212)
darkBlue = (32, 78, 128)
black = (31, 28, 28)


# mouse events 
leftClick = 1
middleClick = 2
rightClick = 3
scrollUp = 4
scrollDown = 5


# pygame setup
pygame.init()
width = 800
screen = pygame.display.set_mode((width, width + 100))
font = pygame.font.SysFont("Arial", 20)
screen.fill(darkBlue)
pygame.display.set_caption("Pathfinding Algorithm")
clock = pygame.time.Clock()


# Classes setup
class Node:
    def __init__(self, row, col, color):
        self.row = row
        self.col = row
        self.color = color
        self.neigbors = []
        self.visited = False
        self.prev = None
        self.barrierList = []

    def getPos(self):
        return (self.row, self.col)
  
    def getRow(self):
        return self.row

    def getCol(self):
        return self.col

    def getColor(self):
        return self.color

    def getNeibors(self):
        return [(self.row, self.col-1), (self.row, self.col+1), (self.row-1, self.col), (self.row+1, self.col)]
        # up down left right

    def updatePos(self, newRow, newCol):
        self.row = newRow
        self.col = newCol
        return (self.row, self.col)

    def isBarrier(self, position, bool):
        # removes barrier if it was even a barrier in the first place
        if bool == False and position in self.barrierList:
            self.barrierList.remove(position)
            print(self.barrierList)
            return False

        # appends barrier position ONCE if not in the list
        elif bool == True:
            if position not in self.barrierList:
                self.barrierList.append(position)
                print(self.barrierList)
                return True
     


startingNode = Node(5, 5, green)
endNode = Node(35, 35, red)
barrierNode = Node(0, 0, black)


#print(startingNode.updatePos(10, 10))
#print(startingNode.getRow())
startingNode.barrier = True
print(startingNode.barrier)

class Button:
    def __init__(self, text):
        self.text = font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.blit(self.text, (0,0))

dijkstrasButton = Button("Dijkstra's Algorithm")


# Algorithms
'''
def dijkstrasAlgo(startRow, startCol):
    clock.tick(5)
    #count = 0
    #openSet = PriorityQueue()
    #openSet.put((0, count, ))
    #From each of the unvisited vertices, choose the vertex with the smallest distance and visit it.

    #Update the distance for each neighboring vertex, of the visited vertex, whose current distance is greater than its sum and the weight of the edge between them.

    #Repeat steps 1 and 2 until all the vertices are visited.
    #pygame.time.delay(700)
    x,y = pygame.mouse.get_pos() 
    x = int(x / 20) + 1
    y = int(y / 20) + 1
    for i in range(1, 10):
        if (startRow + i, startCol) in barrierNode.barrierList:
            print("BARRIER")
            break
        else:
            drawCell(startRow + i, startCol, lightGreen)
            drawGrid(width)

            pygame.time.delay(700)
            pygame.display.update()
'''
def dijkstrasAlgo(start, end):
    #Mark all nodes unvisited. Create a set of all the unvisited nodes called the unvisited set.
    #start = (5, 5)
    #end = (35, 35)
    unvisitedSet = []
    for row in range(1,40+1):
        for col in range(1,40+1):
            if (row, col) not in barrierNode.barrierList:
                unvisitedSet.append([row, col])
    #print(unvisitedSet)
    #visited = PriorityQueue()
    
    #Assign to every node a tentative distance value: set it to zero for our initial node and to infinity for all other nodes. 
    #The tentative distance of a node v is the length of the shortest path discovered so far between the node v and the starting node. 
    #Since initially no path is known to any other vertex than the source itself (which is a path of length zero), all other tentative distances are initially set to infinity. 
    #Set the initial node as current.
#dijkstrasAlgo(1,2,3)

















"""
0 1 2 . . . 800
1
2 
.
.
.
800


"""


# 40 x 40 grid ( 800 / 20 )

def drawGrid(size):
    #clock.tick(5)
    blockSize = 20
    for x in range(0, size, blockSize):
        #pygame.time.delay(50)
        for y in range(0, size, blockSize):
            #pygame.time.delay(50)
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, lightBlue, rect, 1)
            #pygame.display.update()

def drawCell(row, col, color):
    blockSize = 20
    for x in range(0, (800 * 2) + 1, blockSize):
        for y in range(0, (800 * 2) + 1 , blockSize):
            if (40*row == x) and (40*col == y):
                barrierNode.barrier = True
                pygame.draw.rect(screen, color, [(row-1)  * blockSize, (col-1) * blockSize, 20, 20]) 
               
       
def eraseCell(row, col):
    blockSize = 20
    for x in range(0, (800 * 2) + 1, blockSize):
        for y in range(0, (800 * 2) + 1 , blockSize):
            if (40*row == x) and (40*col == y):
                pygame.draw.rect(screen, darkBlue, [(row-1)  * blockSize, (col-1) * blockSize, 20, 20]) 




running = True
while running:
    drawGrid(width)
    screen.blit(dijkstrasButton.surface, (20, width+20))
    drawCell(startingNode.getRow(),startingNode.getCol(), startingNode.getColor())
    drawCell(endNode.getRow(),endNode.getCol(), endNode.getColor())


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # Draws in cell on left click or hold
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == leftClick or pygame.mouse.get_pressed()[0]:
            x,y = pygame.mouse.get_pos() 
            x = int(x / 20) + 1
            y = int(y / 20) + 1
            #print((x,y))
            #print(barrierNode.updatePos(x, y))
         
            if (startingNode.getPos()) == (x, y):
                print("Start node here")
            elif (endNode.getPos() == (x,y)):
                print("End node here")
    
            else:
                drawCell(x, y, barrierNode.getColor())
                print(barrierNode.isBarrier((x, y), True))
            #clock.tick(30)
        
        # Erases cell on right click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == rightClick or pygame.mouse.get_pressed()[2]:
            x,y = pygame.mouse.get_pos() 
            x = int(x / 20) + 1
            y = int(y / 20) + 1

            eraseCell(x, y)
            print(barrierNode.isBarrier((x, y), False))

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == leftClick and x == 6 and y == 42:
            print("test")
            dijkstrasAlgo(startingNode.getPos(), endNode.getPos())
            print(startingNode.getPos())
            print(endNode.getPos())

            #clock.tick(30)


    #drawCell(startingNode.getRow(),startingNode.getCol(), startingNode.getColor())
    #drawCell(endNode.getRow(),endNode.getCol(), endNode.getColor())
    pygame.display.update()