from glm import *

class pointlight:
    def __init__(self, pos, intensity=1, distmax=10, distmin=1):
        self.pos = vec3(pos)
        self.intensity = intensity
        self.distmax = distmax
        self.distmin = distmin

    def getvalue(self, tri, cam):
        light_to_pt = self.pos - tri[4]
        dist = length(light_to_pt)
        side = dot(tri[3],normalize(light_to_pt))
        
        if side<0:
        	side=0
        if dist <= self.distmin:
            return self.intensity*side
        elif dist > self.distmax:
            return 0
        else:
            return self.intensity * (self.distmax - dist) / (self.distmax - self.distmin)*side



class directionlight:
	def __init__(self,dir,intensity=1):
		self.dir=normalize(vec3(dir))
		if self.dir==(0,0,0):
			self.dir=vec3(1,0,0)
		self.intensity=intensity


	def getvalue(self,tri,cam):
		value=dot(tri[3],self.dir)
		if value<=0:
			value=0.1
		return self.intensity*value


class camlight:
	def __init__(self,dir,intensity=1):
		self.dir=vec3(dir)
		if self.dir==(0,0,0):
			self.dir=vec3(1,0,0)
		self.intensity=intensity


	def getvalue(self,tri,cam):
		self.dir=-cam.forward
		value=dot(tri[3],normalize(self.dir))
		if value<=0:
			value=0.1
		return self.intensity*value


class torchlight:
	def __init__(self,dir,intensity=1,angle=40,distmax=40,distmin=1):
		self.dir=dir
		self.intensity=intensity
		self.angle=cos(radians(angle/2))
		self.distmax = distmax
		self.distmin = distmin

	def getvalue(self,tri,cam):
		self.dir=cam.forward
		lighttopt=tri[4]-cam.pos
		nl=normalize(lighttopt)
		val=dot(normalize(self.dir),nl)
		dist=length(lighttopt)
		side = -dot(tri[3],nl)
		#print(side)
		if side<0:
			side=0
		if val>self.angle and dist<self.distmax:
			value=1-((1-val)/(1-self.angle))
			#print(value)
			return value*self.intensity*side*(self.distmax - dist) / (self.distmax - self.distmin)
		else:
			return 0
