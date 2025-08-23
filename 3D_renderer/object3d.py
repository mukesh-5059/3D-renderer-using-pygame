from glm import *
from basic_classes import *


class object3d:
    def __init__(self, pos, angle, file, world,nature,colour=(255,255,255)):
        self.pos = vec3(pos)
        self.angle = vec3(angle)
        self.world = world
        self.triangles, self.vertices = load(file)
        self.colour=vec3(colour)
        self.nature=nature
        
    def calcmodel_viewmat(self):
        translation_matrix = translate(mat4(1.0), self.pos)
        rotation_matrix = rotate(mat4(1.0), self.angle.x, vec3(1, 0, 0)) * \
                          rotate(mat4(1.0), self.angle.y, vec3(0, 1, 0)) * \
                          rotate(mat4(1.0), self.angle.z, vec3(0, 0, 1))
        
        return translation_matrix * rotation_matrix


    def transform(self, pt):
        return self.modelmat * vec4(pt, 1)

    def view(self,cam):
        return lookAt(cam.pos, cam.pos + cam.forward, cam.up) 

    def calcprojectmat(self, cam):
        projectionmat = perspective(cam.fov, cam.world.aspect, cam.near, cam.far)
        return projectionmat

    def givetris(self, cam):
        triangles = []
        projmat=self.calcprojectmat(cam)
        self.modelmat=self.calcmodel_viewmat()
        view=self.view(cam)

        for tri in self.triangles:
            pt1 = self.transform(self.vertices[tri[0]])
            pt2 = self.transform(self.vertices[tri[1]])
            pt3 = self.transform(self.vertices[tri[2]])

            

            #print(mp)

            vec1 = pt2 - pt1
            vec2 = pt3 - pt1
            normal = normalize(cross(vec1.xyz, vec2.xyz))
            value = dot(normal, pt1.xyz - cam.pos)

            if value <= 0:
                #mp=midpoint((Final(pt1,self.world),Final(pt2,self.world),Final(pt3,self.world)))
                mp=midpoint((final(pt1),final(pt2),final(pt3)))
                pt1=view*pt1
                pt2=view*pt2
                pt3=view*pt3
                cllipedtris=clip_triangle_against_plane((pt1.xyz,pt2.xyz,pt3.xyz),vec3(0,0,-0.5),vec3(0,0,-1))
                #if pt1.z<0 and pt2.z<0 and pt3.z<0:
                for tri in cllipedtris:
                    pt1 = final(projmat*vec4(tri[0],1))
                    pt2 = final(projmat*vec4(tri[1],1))
                    pt3 = final(projmat*vec4(tri[2],1))
                    pt1=scalling(pt1, self.world)
                    pt2=scalling(pt2, self.world)
                    pt3=scalling(pt3, self.world)
                #print(pt1)
                    triangles.append((pt1, pt2, pt3, normal, mp, self.colour,self.nature))

        return triangles
