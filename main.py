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

    def getNeighbors(self):
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
pathfindNode = Node(0, 0, lightGreen)

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


# --- Helper Function ---
def distance(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    return ((x2 - x1)**2 + (y2 - y1)**2)**(1/2)
#print(distance((5, 5),(35, 35)))


def dijkstrasAlgo(startNode, endNode):
    #startPos = (5, 5)
    #endPos = (35, 35)


    current = startNode
    currentPos = startNode.getPos()
    startPos = startNode.getPos()

    visitedSet = []
    visitedSet.append(currentPos)
    
    openCell = PriorityQueue()
    openCell.put((0, currentPos)) # (0, (5, 5))

    # -- Starting unvisited set ---
    unvisitedSet = []
    for row in range(1,40+1):
        for col in range(1,40+1):
            if (row, col) not in barrierNode.barrierList:
                unvisitedSet.append((row, col))
                
    #current = openCell.get() # (0, (5, 5))
    #print(current[1]) # (5, 5)
    
    while currentPos != endNode.getPos():
        for coordinate in current.getNeighbors():
            pygame.time.delay(1)
            if coordinate in unvisitedSet and coordinate not in visitedSet:

                # update distance of neighbors from start
                openCell.put((distance(startPos, coordinate), coordinate))
                

                unvisitedSet.remove(coordinate)
                visitedSet.append(coordinate)

                #print(coordinate)
                row, col = coordinate
                drawCell(row, col, lightGreen)
                drawGrid(width)
                pygame.display.update()

        # gets shortest distance from START 
        smallestDistanceinQueue = openCell.get()
        row, col = smallestDistanceinQueue[1]

        pathfindNode.updatePos(row, col)
        print(row, col)
        current = pathfindNode
        currentPos = pathfindNode.getPos()
        
    '''
    for coordinate in visitedSet:
        row, col = coordinate
        drawCell(row, col, yellow)
        pygame.display.update()
    '''
     
           
            

    #print(unvisitedSet)
    #Dijkstra's algorithm needs a priority queue to find the next node to explore.
  
    
    # 2 Assign to every node a tentative distance value: set it to zero for our initial node and to infinity for all other nodes. 
    #   The tentative distance of a node v is the length of the shortest path discovered so far between the node v and the starting node. 
    #   Since initially no path is known to any other vertex than the source itself (which is a path of length zero), all other tentative distances are initially set to infinity. 
    #   Set the initial node as current.

    # 3 For the current node, consider all of its unvisited neighbors and calculate their tentative distances through the current node. 
    # Compare the newly calculated tentative distance to the current assigned value and assign the smaller one. 
    # For example, if the current node A is marked with a distance of 6, and the edge connecting it with a neighbor B has length 2, 
    # then the distance to B through A will be 6 + 2 = 8. If B was previously marked with a distance greater than 8 then change it to 8. Otherwise, the current value will be kept.

















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

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == leftClick and (x >= 2 and x <= 9)  and y == 42:
            print("dijkstras algorithm")
            dijkstrasAlgo(startingNode, endNode)
          

            #clock.tick(30)


    #drawCell(startingNode.getRow(),startingNode.getCol(), startingNode.getColor())
    #drawCell(endNode.getRow(),endNode.getCol(), endNode.getColor())
    pygame.display.update()