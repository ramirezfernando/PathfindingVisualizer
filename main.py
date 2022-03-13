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
startingNode = Node(3, 3, green)
endNode = Node(18, 18, red)
barrierNode = Node(0, 0, black)
pathfindNode = Node(0, 0, lightGreen)
shortestPathNode = Node(0, 0, yellow)

startingNode.barrier = True


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



# ------ Algorithms ------

def distance(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    #return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return abs(x2 - x1) + abs(y2 - y1)
    #return ((x2 - x1)**2 + (y2 - y1)**2)**(1/2)

def neighbors(coord):
    row, col = coord
    return [(row, col-1), (row, col+1), (row-1, col), (row+1, col)]

def shortestPath(cameFrom):
    count = 0
    for key in cameFrom:
        print(key, cameFrom[key])


def dijkstrasAlgo(startNode, endNode):
    #startPos = (5, 5)
    #endPos = (35, 35)
    current = startNode
    currentPos = startNode.getPos()
    startPos = startNode.getPos()

    cameFrom = {}

    # -- Start node with distance from start and position --
    openSet = PriorityQueue()
    openSet.put((0, startPos)) # (0, (5, 5))
    unvisitedSet = []
    openSetHash = {}
    for row in range(1,dimension+1):
	    for col in range(1,dimension+1):
		    if (row, col) not in barrierNode.barrierList:
			    unvisitedSet.append((row, col))
			    openSetHash[(row, col)] = 1000

    unvisitedSet.remove(startNode.getPos())


    # -- Main ---
    while currentPos != endNode.getPos():
        for neighbor in current.getNeighbors():
            pygame.time.delay(1)
            if neighbor in unvisitedSet:
                dist = distance(startPos, neighbor)
                cameFrom[neighbor] = current
				
                x, y = neighbor
                #pygame.time.delay(200)
                drawCell(x, y, lightGreen)
                drawGrid(width)
                pygame.display.update()

                if dist < openSetHash[neighbor]:
                    cameFrom[neighbor] = current

                    del openSetHash[neighbor]
                    openSetHash[neighbor] = dist
                    openSet.put((dist, neighbor))

                    
                    

   

        x, y = openSet.get()[1]
        pathfindNode.updatePos(x, y)
        currentPos = pathfindNode.getPos()
        current = pathfindNode

    
    #print(shortestPath)
    #print(startNode.getPos())

    #print(openSetHash)
    shortestPath = []
    startDist = 1
    #shortestPath.append((100,100))

    #temp = list(openSetHash)

    for i in openSetHash:
       
        #print(i, i+1)
        #print(i, distance(i, endNode.getPos()))
        
        if openSetHash[i] == startDist:
            #smallestPath = min(distance(i, endNode.getPos()), distance(shortestPath[0], endNode.getPos()))
            
            shortestPath.append(i)
            #shortestPath.remove(shortestPath[0])
            print(shortestPath)
            #print(shortestPath)
            #print(i, smallestPath)
             

        elif openSetHash[i] == startDist + 1:
            x, y = shortestPath[len(shortestPath) - 1]
            drawCell(x, y, yellow)
            drawGrid(width)
            #pygame.display.update()
            #print(shortestPath)

            #print(i, smallestPath)
            startDist += 1
            shortestPath.clear()
            print('\n')

    pygame.display.update()
    
            
   


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current):
    while current in came_from:
        current = came_from[current]
        #x, y = current
        #drawCell(x, y, yellow)
        print(current)

def aStar(start, end):

    
    '''
    count = 0
    open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for spot in unvisited}
	g_score[start] = 0
	f_score = {spot: float("inf") for spot in unvisited}
	f_score[start] = h(start.getPos(), end.getPos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end)
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()


		if current != start:
			current.make_closed()

	return False
    '''


# Used queue (FIFO)
def BFS(startNode, endNode):
    current = startNode
    currentPos = startNode.getPos()
    startPos = startNode.getPos()


    # -- Starting unvisited set ---
    unvisited = []
    for row in range(1,dimension+1):
        for col in range(1,dimension+1):
            if (row, col) not in barrierNode.barrierList:
                unvisited.append((row, col))




    visited = [] # List to keep track of visited nodes.
    queue = []     #Initialize a queue

    visited.append(startPos)
    queue.append(startPos)

    while queue:
        current = queue.pop(0) 

        for i in unvisited[current]:
            if i not in visited:
                queue.append(i)
                visited.append(i)

    



# Uses a stack (LIFO)
def DFS(start, end):
    # node function: up down left right, [0] , [1], [2], [3]
    # well do top, right ,down, left, [0], [3], [1], [2]
    unvisited = []

    for row in range(1,dimension+1):
        for col in range(1,dimension+1):
            if (row, col) not in barrierNode.barrierList:
                unvisited.append((row, col))

    visited = set()
    poss_way = [(0,1), (1,0)]


    start_tick = pygame.time.get_ticks()

    while poss_way:
        curr_search = poss_way.pop()
        x,y = curr_search[0], curr_search[1]

        if grid[x][y].color == BLACK:
            continue
        else:
            if (x,y) in visited:
                continue

            visited.add((x,y))

            grid[x][y].color = GREEN
            draw(x, y, yellow)
            pygame.time.wait(10)

            if y > 0 and (x, y-1) in unvisitedSet:
                poss_way.append((x,y-1))
                if grid[x][y-1].color == RED:
                    return True

            if x > 0 and grid[x-1][y].color != BLACK:
                poss_way.append((x-1,y))
                if grid[x-1][y].color == RED:
                    return True

            if  x < (rows-1) and grid[x+1][y].color != BLACK:
                poss_way.append((x+1,y))	
                if grid[x+1][y].color == RED:
                    return True

            if  y < (rows-1) and grid[x][y+1].color != BLACK:
                poss_way.append((x,y+1))
                if grid[x][y+1].color == RED:
                    return True


    






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
# Now its 20 x 20 grid ( 800 / 40)
blockSize = 40
dimension = width // blockSize

unvisitedSet = []
openSetHash = {}
for row in range(1,dimension+1):
    for col in range(1,dimension+1):
        if (row, col) not in barrierNode.barrierList:
            unvisitedSet.append((row, col))
            openSetHash[(row, col)] = 1000

def drawGrid(size):
    #clock.tick(5)
    for x in range(0, size, blockSize):
        #pygame.time.delay(50)
        for y in range(0, size, blockSize):
            #pygame.time.delay(50)
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, lightBlue, rect, 1)
            #pygame.display.update()

def drawCell(row, col, color):
    for x in range(0, (width) + 1, blockSize):
        for y in range(0, (width) + 1 , blockSize):
            if (blockSize*row == x) and (blockSize*col == y):
                barrierNode.barrier = True
                pygame.draw.rect(screen, color, [(row-1)  * blockSize, (col-1) * blockSize, blockSize, blockSize]) 
               
       
def eraseCell(row, col):
    for x in range(0, (width * 2) + 1, blockSize):
        for y in range(0, (width * 2) + 1 , blockSize):
            if (blockSize*row == x) and (blockSize*col == y):
                pygame.draw.rect(screen, darkBlue, [(row-1)  * blockSize, (col-1) * blockSize, blockSize, blockSize]) 






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
            x = int(x / blockSize) + 1
            y = int(y / blockSize) + 1
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
            x = int(x / blockSize) + 1
            y = int(y / blockSize) + 1

            eraseCell(x, y)
            print(barrierNode.isBarrier((x, y), False))


        if dijkstrasButton.pressed:
            dijkstrasAlgo(startingNode, endNode)

        if astarButton.pressed:
            aStar(startingNode, endNode)

        if bfsButton.pressed:
            BFS(startingNode, endNode)

        if dfsButton.pressed:
            DFS(startingNode, endNode)


        if clearpathButton.pressed:
            print("clear path")

            for node in barrierNode.barrierList:
                x,y = node
                eraseCell(x, y)
            barrierNode.barrierList.clear()

        if clearscreenButton.pressed:
            print("clear screen")
            
            for node in unvisitedSet:
                x,y = node
                eraseCell(x, y)
            barrierNode.barrierList.clear()

    pygame.display.update()