import pygame,sys
from glm import *
from basic_classes import sorting
from math import isnan

class camera:
    def __init__(self, pos,  world):
        self.pos = vec3(pos)
        self.up=vec3(0,1,0)
        self.forward=vec3(0,0,1)
        self.right=vec3(1,0,0)
        self.speed = 10
        self.world = world
        self.fov=radians(60)
        self.near=0.5
        self.far=100
        self.yaw=-90
        self.pitch=0
        self.camspeed=0.05
        self.maxrotate=60

    def updateangles(self,dx,dy):
        self.yaw+=dx*self.camspeed
        self.pitch-=dy*self.camspeed
        if self.pitch>=self.maxrotate:
            self.pitch=self.maxrotate
        elif self.pitch<=-self.maxrotate:
            self.pitch=-self.maxrotate
        #print(self.yaw)

        yaw,pitch=radians(self.yaw),radians(self.pitch)
        self.forward.x=cos(yaw)*cos(pitch)
        self.forward.y=sin(pitch)
        self.forward.z=sin(yaw)*cos(pitch)
        self.right = cross(self.forward, self.up)

        
    def movement(self,dt):
        keys = pygame.key.get_pressed()
        scale=self.speed*dt

        if keys[pygame.K_w]:
            self.pos+=self.forward*scale

        if keys[pygame.K_a]:
            self.pos-=self.right*scale
            
        if keys[pygame.K_s]:
            self.pos-=self.forward*scale
            
        if keys[pygame.K_d]:
            self.pos+=self.right*scale

        if keys[pygame.K_SPACE]:
            self.pos+=self.up*scale

        if keys[pygame.K_LSHIFT]:
            self.pos-=self.up*scale

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    def render(self):
        self.alltris=[]
        for obj in self.world.scene:
            self.alltris.extend(obj.givetris(self))
        self.alltris=sorting(self.alltris)
        for tri in self.alltris:

            value=0.1
            for light in self.world.lights:
                val=light.getvalue(tri,self)
                if not(isnan(val)):
                    value+=val
            if tri[6]=='n':
                if value>1:
                    value=tri[5]
                else:
                    value=value*tri[5]
            else:
                if value>=0.7:
                    value=(255,255,255)
                else:
                    value=value*tri[5]                            
            pygame.draw.polygon(self.world.screen,value,((tri[0].x,tri[0].y),(tri[1].x,tri[1].y),(tri[2].x,tri[2].y)))         #triangle=[pt1,pt2,pt3,normal,midpt,colour,nature,2d midpt z]
            #pygame.draw.polygon(self.world.screen,vec3(255,255,255),((tri[0].x,tri[0].y),(tri[1].x,tri[1].y),(tri[2].x,tri[2].y)))
            #pygame.draw.line(self.world.screen, (0,0,0), (tri[0].x,tri[0].y), (tri[1].x,tri[1].y))
            #pygame.draw.line(self.world.screen, (0,0,0), (tri[1].x,tri[1].y), (tri[2].x,tri[2].y))
            #pygame.draw.line(self.world.screen, (0,0,0), (tri[2].x,tri[2].y), (tri[0].x,tri[0].y))
