from glm import *


def triangulate(polygon):
	newtriangles=[]
	while len(polygon)>3:
		b=polygon[-1]
		a=polygon[0]
		c=polygon[1]
		newtriangles.append((b,a,c))
		polygon.pop(0)
	newtriangles.append(tuple(polygon))
	return newtriangles


def midpoint(triangle):
	pt1,pt2,pt3,=triangle
	return (pt1+pt2+pt3)/3

def mpz(tri):
	return (tri[0].z+tri[1].z+tri[2].z)/3

def sorting(triangles):
	t=[]
	for i in triangles:
		t.append((i[0],i[1],i[2],i[3],i[4],i[5],i[6],mpz(i)))            #triangle=[pt1,pt2,pt3,normal,midpt,colour,nature,2d midpt z]
	return sorted(t,key=lambda x: x[7],reverse=True)


def load(file):                                  #load points from the obj file
    vertices=[]
    triangles=[]
    with open(file,'r') as file:
        for i in file:
            if i.startswith('v '):
                line=i.split()
                line.pop(0)
                c=0
                for i in line:
                    line[c]=float(i)
                    c+=1
                vertices.append(vec3(line))
            elif i.startswith("f "):
                line=i.split()
                line.pop(0)
                if '//' in line[0]:
                    element=[]
                    for j in line:
                        one=j.split('//')
                        element.append(one[0])
                    c=0
                    for i in element:
                        element[c]=int(i)-1
                        c+=1
                    if len(element)==3:
                        triangles.append(element)
                    else:
                        triangles.extend(triangulate(element))
                elif '/' in line[0]:
                    element=[]
                    for j in line:
                        one=j.split('/')
                        element.append(one[0])
                    c=0
                    for i in element:
                        element[c]=int(i)-1
                        c+=1
                    if len(element)==3:
                        triangles.append(element)
                    else:
                        triangles.extend(triangulate(element))
                else:
                    line=i.split()
                    line.pop(0)
                    c=0
                    for i in line:
                        line[c]=int(i)-1
                        c+=1
                    if len(line)==3:
                        triangles.append(line)
                    else:
                        triangles.extend(triangulate(line))

    return triangles,vertices                      


def projection(cam):
	return perspective(cam.fov,cam.world.aspect,cam.near,cam.far)

def look(cam):

	return lookAt(cam.pos,cam.pos+cam.forward,cam.up)

        
def final(pt):
	if pt.w!=0:
		pt/=pt.w
	return vec3(pt.xyz)

def scalling(pt,world):
	pt.x=(pt.x + 1) * world.width / 2
	pt.y=(1 - pt.y) * world.height / 2
	pt.z=pt.z*world.height/2
	return pt

def Final(pt,world):
	if pt.w!=0:
		pt/=pt.w
	pt.x=(pt.x + 1) * world.width / 2
	pt.y=(1 - pt.y) * world.height / 2
	pt.z=pt.z*world.height/2
	return vec3(pt.xyz)



def plane_equation(plane_point, plane_normal):
    d = -dot(plane_normal, plane_point)
    return vec4(plane_normal, d)

def point_plane_distance(plane, point):
    return dot(plane.xyz, point) + plane[3]

def intersect_segment_plane(p1, p2, plane):
    d1 = point_plane_distance(plane, p1)
    d2 = point_plane_distance(plane, p2)
    if d1 * d2 >= 0:
        return vec3(0)  # No intersection or the whole segment is on one side
    t = d1 / (d1 - d2)
    return p1 + t * (p2 - p1)

def clip_triangle_against_plane(triangle, plane_point, plane_normal):
    plane = plane_equation(plane_point, plane_normal)
    
    inside_points = []
    outside_points = []
    
    for point in triangle:
        if point_plane_distance(plane, point) >= 0:
            inside_points.append(point)
        else:
            outside_points.append(point)
    
    if len(inside_points) == 0:
        return []  # The whole triangle is outside the plane
    
    if len(inside_points) == 3:
        return [triangle]  # The whole triangle is inside the plane
    
    if len(inside_points) == 1 and len(outside_points) == 2:
        new_triangle = [inside_points[0]]
        new_triangle.append(intersect_segment_plane(inside_points[0], outside_points[0], plane))
        new_triangle.append(intersect_segment_plane(inside_points[0], outside_points[1], plane))
        return [new_triangle]
    
    if len(inside_points) == 2 and len(outside_points) == 1:
        new_triangles = []
        new_triangles.append([inside_points[0], inside_points[1], intersect_segment_plane(inside_points[0], outside_points[0], plane)])
        new_triangles.append([inside_points[1], intersect_segment_plane(inside_points[1], outside_points[0], plane), intersect_segment_plane(inside_points[0], outside_points[0], plane)])
        return new_triangles



def wrapcolour(colour):
	r,g,b=colour
	if r>255:
		r=255
	if g>255:
		g=255
	if b>255:
		b=255
	return (r,g,b)


