import pygame, sys, time

# node colors
white = (250, 250, 250)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

# mouse events 
leftClick = 1
middleClick = 2
rightClick = 3
scrollUp = 4
scrollDown = 5


pygame.init()
width = 800
screen = pygame.display.set_mode((width, width + 100))
font = pygame.font.SysFont("Arial", 20)
screen.fill(white)
pygame.display.set_caption("Pathfinding Algorithm")


clock = pygame.time.Clock()









class Node:
    def __init__(self, row, col, color):
        self.row = row
        self.col = row
        #self.x = row * width
        #self.y = col * width
        self.color = color
        self.neigbors = []
  
    def getRow(self):
        return self.row

    def getCol(self):
        return self.col

    def getColor(self):
        return self.color

    def getNeibors(self):
        return [(self.row, self.col-1), (self.row, self.col+1), (self.row-1, self.col), (self.row+1, self.col)]
        # up down left right

startingNode = Node(5, 5, green)
endNode = Node(35, 35, red)
barrierNode = Node(0, 0, black)

print(startingNode.getNeibors())
class Button:
    def __init__(self, text):
        self.text = font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.blit(self.text, (0,0))

dijkstrasButton = Button("Dijkstra's Algorithm")

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
            pygame.draw.rect(screen, black, rect, 1)
            #pygame.display.update()

def drawCell(row, col, color):
    blockSize = 20
    for x in range(0, (800 * 2) + 1, blockSize):
        for y in range(0, (800 * 2) + 1 , blockSize):
            if (40*row == x) and (40*col == y):
                pygame.draw.rect(screen, color, [(row-1)  * blockSize, (col-1) * blockSize, 20, 20]) 
               
       
def eraseCell(row, col):
    blockSize = 20
    for x in range(0, (800 * 2) + 1, blockSize):
        for y in range(0, (800 * 2) + 1 , blockSize):
            if (40*row == x) and (40*col == y):
                pygame.draw.rect(screen, white, [(row-1)  * blockSize, (col-1) * blockSize, 20, 20]) 







running = True
while running:
    drawGrid(width)
    screen.blit(dijkstrasButton.surface, (20, width+20))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # Draws in cell on left click or hold
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == leftClick or pygame.mouse.get_pressed()[0]:
            x,y = pygame.mouse.get_pos() 
            x = int(x / 20) + 1
            y = int(y / 20) + 1
            print(x,y)
            drawCell(x, y, barrierNode.getColor())
            #clock.tick(30)
        
        # Erases cell on right click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == rightClick:
            x,y = pygame.mouse.get_pos() 
            x = int(x / 20) + 1
            y = int(y / 20) + 1
            eraseCell(x, y)
          
    drawCell(startingNode.getRow(),startingNode.getCol(), startingNode.getColor())
    drawCell(endNode.getRow(),endNode.getCol(), endNode.getColor())
    pygame.display.update()