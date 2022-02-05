import pygame, sys, time

white = (250, 250, 250)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

pygame.init()
width = 800
screen = pygame.display.set_mode((width, width + 100))
font = pygame.font.SysFont("Arial", 20)
screen.fill(white)
pygame.display.set_caption("Pathfinding Algorithm")


#clock = pygame.time.Clock()









class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = row
        self.x = row * width
        self.y = col * width
        self.color = white
        self.neigbors = []
        self.width = width

    def getPosition(self):
        return self.row, self.col

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

def drawCell(row, col):
    blockSize = 20
    for x in range(0, (800 * 2) + 1, blockSize):
        for y in range(0, (800 * 2) + 1 , blockSize):
            if (40*row == x) and (40*col == y):
                pygame.draw.rect(screen, [0,255,0], [(row-1)  * blockSize, (col-1) * blockSize, 20, 20]) 
               
       








running = True
while running:
    drawGrid(width)
    screen.blit(dijkstrasButton.surface, (20, width+20))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawCell(1, 1)
            
    pygame.display.update()