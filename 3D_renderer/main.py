import pygame,sys
from camera import camera
from object3d import object3d
from basic_classes import *
from lights import *

class game:
    def __init__(self):
        pygame.init()
        self.width = 640
        self.height = 480
        self.aspect=self.width/self.height
        #self.screen = pygame.display.set_mode((self.width, self.height),pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.scene = []
        self.lights=[]
        self.createobjects()

    def createobjects(self):
        self.camera1 = camera((0,0,10), self)  
        self.lights.extend([directionlight((-9.18744,2.098,-10.5526))])
        n=1                                                         #create n*n*n objects in the scene
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    self.scene.append(object3d((i*5, j*5, k*5), (0, 0, 0),'models/mountains.obj', self,'s',(77,238,234))) 
                    #self.scene.append(object3d((5,0 ,0 ), (0, 0, 0),'models/untitled.obj', self,(25,255,25)))
        self.camera1.updateangles(0,0)
        
    def draw(self):
        self.screen.fill('BLACK')
        self.camera1.render()


    def events(self): 
        dt = self.clock.tick()*0.001
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mouse.set_visible(True)  
                    pygame.event.set_grab(False)
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    dx,dy=event.rel
                    self.camera1.updateangles(dx,dy)
        self.camera1.movement(dt)
        

    def run(self):
        while True:
            pygame.display.set_caption('FPS : '+str(int(self.clock.get_fps())))
            self.events()
            self.draw()
            pygame.display.update()
            #self.clock.tick(60)

testgame = game()
if __name__ == '__main__':
    testgame.run()



