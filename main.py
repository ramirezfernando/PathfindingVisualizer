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
     

# -- Node setup -- 
startingNode = Node(5, 5, green)
endNode = Node(35, 35, red)
barrierNode = Node(0, 0, black)
pathfindNode = Node(0, 0, lightGreen)

startingNode.barrier = True
print(startingNode.barrier)


class Button:
	def __init__(self,text,width,height,pos,elevation):
		#Core attributes 
		self.pressed = False
		self.elevation = elevation
		self.dynamic_elecation = elevation
		self.original_y_pos = pos[1]

		# top rectangle 
		self.top_rect = pygame.Rect(pos,(width,height))
		self.top_color = '#475F77'

		# bottom rectangle 
		self.bottom_rect = pygame.Rect(pos,(width,height))
		self.bottom_color = '#354B5E'
		#text
		self.text_surf = font.render(text,True,'#FFFFFF')
		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

	def draw(self):
		# elevation logic 
		self.top_rect.y = self.original_y_pos - self.dynamic_elecation
		self.text_rect.center = self.top_rect.center 

		self.bottom_rect.midtop = self.top_rect.midtop
		self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

		pygame.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius = 12)
		pygame.draw.rect(screen,self.top_color, self.top_rect,border_radius = 12)
		screen.blit(self.text_surf, self.text_rect)
		self.check_click()

	def check_click(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.top_rect.collidepoint(mouse_pos):
			self.top_color = '#D74B4B'
			if pygame.mouse.get_pressed()[0]:
				self.dynamic_elecation = 0
				self.pressed = True
			else:
				self.dynamic_elecation = self.elevation
				if self.pressed == True:
					#print('click')
					self.pressed = False
		else:
			self.dynamic_elecation = self.elevation
			self.top_color = '#475F77'


dijkstrasButton = Button("Dijkstra's Algorithm",200,40,(30,810),5)
astarButton = Button("A* Search Algorithm", 200, 40, (250, 810),5)
bfsButton = Button("Breadth-first search", 200, 40, (30, 860),5)
dfsButton = Button("Depth-first search", 200, 40, (250, 860),5)

clearpathButton = Button("Clear Path", 200, 40, (550, 810),5)
clearscreenButton = Button("Clear Screen", 200, 40, (550, 860),5)





# --- Helper Function ---
def distance(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
#print(distance((5, 5),(35, 35)))


def dijkstrasAlgo(startNode, endNode):
    #startPos = (5, 5)
    #endPos = (35, 35)


    current = startNode
    currentPos = startNode.getPos()
    startPos = startNode.getPos()

    visitedSet = []

    # -- Start node with distance from start and position --
    openSet = PriorityQueue()
    openSet.put((0, startPos)) # (0, (5, 5))
    openSetHash = {}
    # -- Starting unvisited set ---
    unvisitedSet = []
    for row in range(1,40+1):
        for col in range(1,40+1):
            if (row, col) not in barrierNode.barrierList:
                unvisitedSet.append((row, col))
                #openSet.put((100, (row, col))) # instead of infinity im using 100
                openSetHash[(row, col)] = 100
    unvisitedSet.remove(startNode.getPos())


    
    # -- Main ---
    while currentPos != endNode.getPos():
        #x, y = openSet.get()[1]
        #current.updatePos(x, y)
        for neighbor in current.getNeighbors():
            pygame.time.delay(2)
            if neighbor in unvisitedSet:
                dist = distance(startPos, neighbor)
                print(dist)

                x, y = neighbor
                drawCell(x, y, lightGreen)
                drawGrid(width)
                pygame.display.update()

                if dist < openSetHash[neighbor]:
                    openSet.put((distance, neighbor))
                    #del openSetHash[neighbor]

        current = pathfindNode
        x, y = openSet.get()[1]
        pathfindNode.updatePos(x, y)

        visitedSet.append(current)
             
                



            









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
    # screen setup
    drawGrid(width)
    dijkstrasButton.draw()
    astarButton.draw()
    bfsButton.draw()
    dfsButton.draw()
    clearpathButton.draw()
    clearscreenButton.draw()



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


        if dijkstrasButton.pressed:
            print("dijkstra")


        if astarButton.pressed:
            print("A*")

        if bfsButton.pressed:
            print("BFS")

        if dfsButton.pressed:
            print("DFS")


        if clearpathButton.pressed:
            print("clear path")

        if clearscreenButton.pressed:
            print("clear screen")
            
            for node in barrierNode.barrierList:
                x,y = node
                eraseCell(x, y)
            barrierNode.barrierList.clear()

    pygame.display.update()