import math
import numpy as mp
import pygame
import time
import random

class Walker():
    def __init__(self):

        mass_xpos = 0.1 # m
        mass_ypos = 1 # m
        mass_xvel = random.random()+5 # m/s
        mass_yvel = 0 # m/s
        foot_xpos = 0.1 # m
        foot_ypos = 0 # m
        self.state = [mass_xpos, mass_ypos, mass_xvel, mass_yvel, foot_xpos, foot_ypos]

        self.vdes = 5 # m/s Desired speed for the first step
        self.first = True

        self.gravity = 9.8 # m/s^2

        self.mass = 1 # kg

        self.xCOP = 0.1 # m

        self.counter = 5

        self.dt = 0.02

        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

        self.screenWidth = 1000
        self.screenHeight = 600

        self.display = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.display.fill(self.white)
        pygame.draw.line(self.display,self.black, (0, self.screenHeight/2), (self.screenWidth, self.screenHeight/2),5)

    def update(self):
        print("Updating")
        print(self.state[2])
        print(self.state[0])
        if (self.state[0] >= self.state[4]): # Step 1: Decide when to take a step
        	# only need to take one step
            time.sleep(0.5)
            self.step()
            self.counter -= 1

        cx = self.state[0]
        cy = self.state[1]
        cvx = self.state[2]
        cvy = self.state[3]
        fx = self.state[4]
        fy = self.state[5]

        dt = self.dt
        
        # Step 3: Calculate the change in states
        # want the acceleration of the system in x
        m = self.mass
        g = self.gravity
        COP = self.xCOP
        x = self.state[0] # self.state[0]
        y0 = self.state[1]
        footLoc = self.state[4]

        ax = (g*x - g * footLoc) / y0
        print("Ax", ax)
        # input("Cont)")

        # Step 4: Integrate these changes to update the states
        # use linear assuming acceleration
        self.euler_integration(ax, dt)
        # input("choc")
        self.draw()


    def euler_integration(self, ax, dt):
        V = self.state[2]
        x = self.state[0]
        self.state[0] = x + V * dt
        self.state[2] = self.state[2] + ax * dt
        

    def step(self):
    	# calculate where to step
        y0 = self.state[1]
        g = self.gravity
        vi = self.state[2]
        vf = self.vdes * self.counter / 5
        xf = math.sqrt((y0/g) * (vi**2 - vf**2))

        self.state[4] = self.state[4] + xf 
        print("Xf = ", xf)# Step 2: Calculate where to step and update the foot position
        # input("go")

    def draw(self):

        cx = self.state[0]*200 # m to pixels
        cy = self.screenHeight/2-self.state[1]*200 # m to pixels
        fx = self.state[4]*200 # m to pixels
        fy = self.screenHeight/2-self.state[5]*200 # m to pixels

        self.display.fill(self.white)
        pygame.draw.line(self.display,self.black, (0, self.screenHeight/2), (self.screenWidth, self.screenHeight/2),5)

        pygame.draw.line(self.display, self.blue, (cx, cy), (fx, fy),5)
        pygame.draw.circle(self.display, self.red, (round(cx), round(cy)), 20)

        speedString = ("%.2f" % self.state[2])
        textSurface = pygame.font.Font('freesansbold.ttf',40).render(speedString, True, self.black)
        textRect = textSurface.get_rect()
        textRect.center = (cx, cy-50)
        self.display.blit(textSurface, textRect)

        pygame.display.update()

        time.sleep(.03) # just makes it easier to see


if __name__ == '__main__':
    pygame.init()
    walker = Walker()

    sim = True
    
    while sim==True:
        walker.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or walker.counter == 0: 
                pygame.quit()
                sim = False
        # time.sleep(0.1)
