#Setup thingies#########################
import pygame, sys
from pygame.locals import *
from pygame import gfxdraw
import gamelog
import random
pygame.init()
clock = pygame.time.Clock()
framerate = 60
resX = 800
resY = 400

SCREEN = pygame.display.set_mode((resX, resY))
pygame.display.set_caption("Bounce")

WHITE = (255, 255, 255) #Defines colors for graphics
BLACK = (0, 0, 0)
BLUE = (0, 106, 255)
RED = (255, 0, 0)
YELLOW = (255, 189, 0)
GREEN = (0, 168, 0)

colorlist = [RED, YELLOW, GREEN, BLUE] #List of colors for balls--the RNG will select a random color to make the next ball.

myLog = gamelog.Logger(SCREEN)
myLog.maxlines = 10
#End Setup Thingies##############

#Ball and BallGroup Class to check for compatibility with final game
class Ball:
    def __init__(self, surf, color, coords, radius, velocity, acceleration, attr = None):
    #Creates an instance of Ball

        self.coords = list(coords)
        self.color = list(color)
        self.vel = list(velocity)
        self.acc = list(acceleration)
        self.property = attr #Special property--not used now but can be implemented for something else if needed 
        self.blurlist = []
        self.surf = surf
        self.radius = radius

    def update(self): #Updates the ball's position, velocity, and is where the physics for the ball happen.
        self.vel = [self.vel[0] + self.acc[0], self.vel[1] + self.acc[1]]
        
        self.coords = [self.coords[0] + self.vel[0], 
                       self.coords[1] + self.vel[1]]
        
        self.blurlist = []
        
    def bounceY(self):
        self.vel[1] = -self.vel[1]- self.acc[1]
        
    def bounceX(self):
        self.vel[0] = -self.vel[0] - self.acc[0]
        
    def draw(self):

        #Draw a smooth circle outline without those jagged pixellated edges
        pygame.gfxdraw.aacircle(self.surf, int(self.coords[0]), 
                                int(self.coords[1]), self.radius, self.color) 
        #Draw the filled center of the circle 
        pygame.gfxdraw.filled_circle(self.surf, int(self.coords[0]),                                      int(self.coords[1]), self.radius, self.color)
        #Circles are kinda like chocolate truffles--smooth on the outside, filled on the inside...
        
class BallGroup:
    def __init__(self):
        self.objects = []
        self.size = 0 #Keeps track of how many balls are in list
    def add(self, instance):
        self.objects.append(instance)
    def draw(self):
        for items in self.objects:
            items.draw()
    def remove(self, obj):#Because "kill" sounds too morbid...
        del(obj)
        
    def update(self):
        count = 0
        
        while count < len(self.objects):#Allows the list to become modifiable due to advanced for loops being immutable                            
            items = self.objects[count]
            items.update()
            if (items.coords[0] >= resX - items.radius or 
                    items.coords[0] <= items.radius):
                items.bounceX()
                
            if items.coords[1] > resY + 200:
                #items.bounceY()
                del(self.objects[count])
 
            count += 1
            
        self.size = len(self.objects)
        
   
        
    def clear(self): #Deletes all objects in group
        for num in range(0, len(self.objects)):
            del(self.objects[-1])

#Goal Code Start########
BLUEGOAL = range(0, int(resX / 4) - 1)
GREENGOAL = range(int(resX / 4), int(resX / 2) - 1)
YELLOWGOAL = range(int(resX / 2), int(resX * 3 / 4) - 1)
REDGOAL = range(int(resX * 3 / 4), int(resX))
GOALHEIGHT = 25
#Goal Code End########

myGroup = BallGroup()
mouse = (0, 0)
myBall = Ball(SCREEN, RED, 
                    mouse, 10, 
                    (0, 0), (0, 0))
myGroup.add(myBall)
while True:
    SCREEN.fill(WHITE) #Blanks screen
    
    myBall.coords = mouse
    
    myGroup.draw()
    for num in range(0, 4):
        pygame.draw.rect(SCREEN, colorlist[3 - num],
                                 ((resX / 4) * num, 0, (resX / 4), GOALHEIGHT))
        
    for event in pygame.event.get(): #Event handler--all events go here!
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[K_LMETA] or keys[K_RMETA]:
                if keys[K_q] or keys[K_w]:
                    pygame.quit()
                    sys.exit()
            
        if event.type == MOUSEMOTION:
            mouse = pygame.mouse.get_pos()

    pygame.display.update()
    clock.tick(framerate)
