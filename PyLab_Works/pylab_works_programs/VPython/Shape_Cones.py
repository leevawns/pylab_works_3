from visual import *

Forward_Up ( (-1,-2,-1), None, 80 )
Coordinate_Axis ( 20 )

# Contributed by Thom Ives; modified by Bruce Sherwood and David Sherer
# July 2002

newframe = frame # this makes "newframe()" mean what "frame()" usually means

class tube () : #(object):
    def __init__(self, frame=None, pos=(0,0,0), axis=(1,0,0), r1=2.0, r2=10.0, color=color.blue, incs=25):
        self.frame = newframe(pos=pos, axis=axis, frame=frame)
        self.__pos = vector(pos)
        self.__axis = vector(axis)
        self.__r1 = r1
        self.__r2 = r2
        self.__color = color
        self.incs = incs
        VertexList, NormalList = self.buildfaces()
        self.faces = faces(frame=self.frame, pos=VertexList, normal=NormalList, color=color)

    def buildfaces(self):
        VertexList = []    # Create an empty vertex list for the body's vertices.
        NormalList = []     # Ditto for the vertex normals.
        length = mag(self.axis)
        costheta = 1.0
        sintheta = 0.0
        dtheta = 2*pi/self.incs
        cosdtheta = cos(dtheta)
        sindtheta = sin(dtheta)
        fnormal = vector(1,0,0)
        bnormal = vector(-1,0,0)

        for i in range(self.incs):

        # Calculate four pts that form a small rectangle on each of the surfaces.
        # Use these points to make the vertices of two triangles that form each of these reactangles.
        # Find a normal to the rectangle. Store vertices and normals.
        # Repeat for the number of increments you want - more increments better visual quality.

            # recursion relations for cosine and sine of (theta+dtheta); avoid lots of trig functions
            newcostheta = costheta*cosdtheta-sintheta*sindtheta
            newsintheta = sintheta*cosdtheta+costheta*sindtheta

            # Back Face Triangles, Vector / Vertices and Triangles
            pb1 = vector(0.0,self.r1*costheta,self.r1*sintheta)
            pb2 = vector(0.0,self.r2*costheta,self.r2*sintheta)
            pb3 = vector(0.0,self.r2*newcostheta,self.r2*newsintheta)
            pb4 = vector(0.0,self.r1*newcostheta,self.r1*newsintheta)
            VertexList = VertexList + [pb1,pb3,pb2,pb1,pb4,pb3]
            NormalList = NormalList + [bnormal,bnormal,bnormal,bnormal,bnormal,bnormal]

            # Front Face Points
            pf1 = pb1+vector(length,0,0)
            pf2 = pb2+vector(length,0,0)
            pf3 = pb3+vector(length,0,0)
            pf4 = pb4+vector(length,0,0)
            VertexList = VertexList + [pf1,pf2,pf3,pf1,pf3,pf4]
            NormalList = NormalList + [fnormal,fnormal,fnormal,fnormal,fnormal,fnormal]

            # Inside Face Triangles; normals chosen for smoothing
            norm1 = vector(0,-costheta,-sintheta)
            norm2 = vector(0,-newcostheta,-newsintheta)
            VertexList = VertexList + [pb1,pf1,pf4,pb1,pf4,pb4]
            NormalList = NormalList + [norm1,norm1,norm2,norm1,norm2,norm2]

            # Outside Face Triangles; normals chosen for smoothing
            norm1 = vector(0,costheta,sintheta)
            norm2 = vector(0,newcostheta,newsintheta)
            VertexList = VertexList + [pf2,pb2,pb3,pf2,pb3,pf3]
            NormalList = NormalList + [norm1,norm1,norm2,norm1,norm2,norm2]

            sintheta = newsintheta
            costheta = newcostheta

        return VertexList, NormalList

    def getpos(self):
        return self.__pos

    def setpos(self, pos):
        self.frame.pos = self.__pos = vector(pos)

    pos = property(getpos, setpos)

    def getaxis(self):
        return self.__axis

    def setaxis(self, axis): # scale all points in front face
        self.frame.axis = self.__axis = vector(axis)
        length = mag(self.__axis)
        for nn in range(0, 24*self.incs, 24):
            for dd in [6,7,8,9,10,11, 13,14,16, 18,21,23]:
                self.faces.pos[nn+dd][0] = length

    axis = property(getaxis, setaxis)

    def rebuild(self):
        VertexList, NormalList = self.buildfaces()
        self.faces.pos = VertexList
        self.faces.normal = NormalList

    def getr1(self):
        return self.__r1

    def setr1(self, r1): # scale all points involving r1
        k = r1/self.r1
        for nn in range(0, 24*self.incs, 24):
            for dd in [0,3,4, 6,9,11, 12,13,14,15,16,17]:
                self.faces.pos[nn+dd][1] *= k
                self.faces.pos[nn+dd][2] *= k
        self.__r1 = r1

    r1 = property(getr1, setr1)

    def getr2(self):
        return self.__r2

    def setr2(self, r2):# scale all points involving r2
        k = r2/self.r2
        for nn in range(0, 24*self.incs, 24):
            for dd in [1,2,5, 7,8,10, 18,19,20,21,22,23]:
                self.faces.pos[nn+dd][1] *= k
                self.faces.pos[nn+dd][2] *= k
        self.__r2 = r2

    r2 = property(getr2, setr2)

    def getcolor(self):
        return self.__color

    def setcolor(self, color):
        self.__color = color
        self.faces.color = color

    color = property(getcolor, setcolor)

class frustum(): #object):
    # Forms a cone with the top cut off. Mag of axis sets height.
    def __init__(self, frame=None, pos=(0,0,0), axis=(0,0,1), r1=2.0, r2=10.0, color=color.red, incs=25):
        self.frame = newframe(pos=pos, axis=axis, frame=frame)
        self.__pos = vector(pos)
        self.__axis = vector(axis)
        self.__r1 = r1
        self.__r2 = r2
        self.__color = color
        self.incs = incs
        VertexList, NormalList = self.buildfaces()
        self.faces = faces(frame=self.frame, pos=VertexList, normal=NormalList, color=color)

    def buildfaces(self):
        VertexList = []     # Create an empty vertex list for the body's vertices.
        NormalList = []     # Ditto for the vertex normals.
        length = mag(self.axis)
        costheta = 1.0
        sintheta = 0.0
        dtheta = 2*pi/self.incs
        cosdtheta = cos(dtheta)
        sindtheta = sin(dtheta)
        p0 = vector(length,0.0,0.0)
        p5 = vector(0.0,0.0,0.0)

        for i in range(self.incs):

        # Calculate four pts that form a small rectangle on each of the surfaces.
        # Use these points to make the vertices of two triangles that form each of these reactangles.
        # Find a normal to the rectangle. Store vertices and normals.
        # Repeat for the number of increments you want - more increments better visual quality.

            # recursion relations for cosine and sine of (theta+dtheta); avoid lots of trig functions
            newcostheta = costheta*cosdtheta-sintheta*sindtheta
            newsintheta = sintheta*cosdtheta+costheta*sindtheta

            # Vector / Vertices and Triangles
            p1 = vector(length,self.r1*costheta,self.r1*sintheta)
            p2 = vector(0.0,self.r2*costheta,self.r2*sintheta)
            p3 = vector(0.0,self.r2*newcostheta,self.r2*newsintheta)
            p4 = vector(length,self.r1*newcostheta,self.r1*newsintheta)
            VertexList = VertexList + [p0,p1,p4,p1,p2,p3,p1,p3,p4,p5,p3,p2]
            snorm1 = vector(dot(p0-p5,p1-p2)*(p0-p5) - (p1-p2))
            snorm2 = vector(dot(p0-p5,p4-p3)*(p0-p5) - (p4-p3))
            snorm1.mag = 1; snorm2.mag = 1
            fnorm = vector(1,0,0); bnorm = vector(-1,0,0)
            NormalList = NormalList + [fnorm,fnorm,fnorm,snorm1,snorm1,snorm2,\
                                       snorm1,snorm2,snorm2,bnorm,bnorm,bnorm]

            sintheta = newsintheta
            costheta = newcostheta

        return VertexList, NormalList

    def getpos(self):
        return self.__pos

    def setpos(self, pos):
        self.frame.pos = self.__pos = vector(pos)

    pos = property(getpos, setpos)

    def getaxis(self):
        return self.__axis

    def setaxis(self, axis): # scale all points in front face
        self.frame.axis = self.__axis = vector(axis)
        length = mag(self.__axis)
        for nn in range(0, 12*self.incs, 12):
            for dd in [0,1,2,3,6,8]:
                self.faces.pos[nn+dd][0] = length

    axis = property(getaxis, setaxis)

    def rebuild(self):
        VertexList, NormalList = self.buildfaces()
        self.faces.pos = VertexList
        self.faces.normal = NormalList

    def getr1(self):
        return self.__r1

    def setr1(self, r1): # scale all points involving r1
        k = r1/self.r1
        for nn in range(0, 12*self.incs, 12):
            for dd in [1,2,3,6,8]:
                self.faces.pos[nn+dd][1] *= k
                self.faces.pos[nn+dd][2] *= k
        self.__r1 = r1

    r1 = property(getr1, setr1)

    def getr2(self):
        return self.__r2

    def setr2(self, r2):# scale all points involving r2
        k = r2/self.r2
        for nn in range(0, 12*self.incs, 12):
            for dd in [4,5,7,11]:
                self.faces.pos[nn+dd][1] *= k
                self.faces.pos[nn+dd][2] *= k
        self.__r2 = r2

    r2 = property(getr2, setr2)

    def getcolor(self):
        return self.__color

    def setcolor(self, color):
        self.__color = color
        self.faces.color = color

    color = property(getcolor, setcolor)

class spherepart(): #object):
    # This routine draws partial spheres. Mag of axis determines radius, b raises base from halfway pt,
    # and f determines how much to subtract from the radius to form a flat surface.
    # Default parameters draw a hemisphere with radius = 2.0.
    def __init__(self, frame=None, pos=(0,0,0), axis=(2,0,0), b=0.0, f=0.0, color=color.yellow, incs=25):
        self.frame = newframe(pos=pos, axis=axis, frame=frame)
        self.__pos = vector(pos)
        self.__axis = vector(axis)
        self.b = b
        self.f = f
        self.r = mag(self.axis)
        self.phi_b = asin(self.b/mag(self.axis))
        self.phi_f = asin((mag(self.axis)-self.f)/mag(self.axis))
        self.__color = color
        self.incs = incs
        VertexList, NormalList = self.buildfaces()
        self.faces = faces(frame=self.frame, pos=VertexList, normal=NormalList, color=color)

    def buildfaces(self):
        VertexList = []    # Create an empty vertex list for the body's vertices.
        NormalList = []     # Ditto for the vertex normals.
        length = mag(self.axis)

        cosphi = cos(self.phi_b)
        sinphi = sin(self.phi_b)
        dphi = (self.phi_f - self.phi_b)/self.incs
        cosdphi = cos(dphi)
        sindphi = sin(dphi)
        p0 = vector(self.r*sinphi,0,0);        n0 = (-1.0,0.0,0.0)
        p5 = vector(self.r-self.f,0,0);        n5 = (1.0,0.0,0.0)

        for i in range(self.incs):
            newcosphi = cosphi*cosdphi-sinphi*sindphi
            newsinphi = sinphi*cosdphi+cosphi*sindphi

            costheta = 1.0
            sintheta = 0.0
            dtheta = 2*pi/self.incs
            cosdtheta = cos(dtheta)
            sindtheta = sin(dtheta)

            for j in range(self.incs):

        # Calculate four pts that form a small rectangle on each of the surfaces.
        # Use these points to make the vertices of two triangles that form each of these reactangles.
        # Find a normal to the rectangle. Store vertices and normals.
        # Repeat for the number of increments you want - more increments better visual quality.

                # recursion relations for cosine and sine of (theta+dtheta); avoid lots of trig functions
                newcostheta = costheta*cosdtheta-sintheta*sindtheta
                newsintheta = sintheta*cosdtheta+costheta*sindtheta

                # Vector / Vertices and Triangles
                p1 = vector(self.r*sinphi,self.r*costheta*cosphi,self.r*sintheta*cosphi)
                p2 = vector(self.r*sinphi,self.r*newcostheta*cosphi,self.r*newsintheta*cosphi)
                p3 = vector(self.r*newsinphi,self.r*newcostheta*newcosphi,self.r*newsintheta*newcosphi)
                p4 = vector(self.r*newsinphi,self.r*costheta*newcosphi,self.r*sintheta*newcosphi)

                # normals chosen for smoothing - an Oil of Olay technique
                n1 = vector(sinphi,costheta*cosphi,sintheta*cosphi)
                n2 = vector(sinphi,newcostheta*cosphi,newsintheta*cosphi)
                n3 = vector(newsinphi,newcostheta*newcosphi,newsintheta*newcosphi)
                n4 = vector(newsinphi,costheta*newcosphi,sintheta*newcosphi)

                if i > 0 and i < (self.incs-1):
                    VertexList = VertexList + [p1,p2,p3,p1,p3,p4]
                    NormalList = NormalList + [n1,n2,n3,n1,n3,n4]
                elif i == 0:
                    VertexList = VertexList + [p0,p2,p1,p1,p2,p3,p1,p3,p4]
                    NormalList = NormalList + [n0,n0,n0,n1,n2,n3,n1,n3,n4]
                elif i == (self.incs-1):
                    VertexList = VertexList + [p1,p2,p3,p1,p3,p4,p4,p3,p5]
                    NormalList = NormalList + [n1,n2,n3,n1,n3,n4,n5,n5,n5]

                sintheta = newsintheta
                costheta = newcostheta

            sinphi = newsinphi
            cosphi = newcosphi

        return VertexList, NormalList

    def getpos(self):
        return self.__pos

    def setpos(self, pos):
        self.frame.pos = self.__pos = vector(pos)

    pos = property(getpos, setpos)

    def getaxis(self):
        return self.__axis

    def setaxis(self, axis): # scale all points in front face
        k = mag(vector(axis))/mag(self.axis)
        self.frame.axis = self.__axis = vector(axis)
        for pos in self.faces.pos:
            pos[0] *= k; pos[1] *= k; pos[2] *= k

    axis = property(getaxis, setaxis)

    def rebuild(self):
        VertexList, NormalList = self.buildfaces()
        self.faces.pos = VertexList
        self.faces.normal = NormalList

    def getcolor(self):
        return self.__color

    def setcolor(self, color):
        self.__color = color
        self.faces.color = color

    color = property(getcolor, setcolor)

if scene.mouse.clicked :
  while scene.mouse.clicked :
    scene.mouse.getclick()

#if __name__ == '__main__':
# Provide a simple program to illustrate how the tube object works.
scene.background = color.white # White background - duh!
f = frame()
State = 0  #  Problem !!!! in next 3 lines
Lens = tube(frame=f, pos=(0,0,15), axis=(0,0,1.0), r1=2.0, r2=4.0, color=color.blue)
Base = frustum(frame=f, pos=(0,0,0), axis=(0,0,5.0), r1=5.0, r2=8.0, color=color.red)
Tip = spherepart(frame=f, pos=(0,0,5), axis=(0,0,10.0), b=0.0, f=0.0, color=color.yellow)

State = 0
while True :
    rate ( 50 )

    if scene.mouse.clicked :
      while scene.mouse.clicked :
        scene.mouse.getclick()
      if State == 0 :
        #scene.mouse.getclick() # wait for a mouse click
        Lens.pos = (0,0,20.0)
        Lens.axis = (0,0,2.0)
        Lens.r1 = 5.0
        Lens.r2 = 20.0
        Base.r1 = 2.5
        Tip.axis = (0,0,2.5)
        State += 1
      elif State == 1 :
        i = 0
        State += 1
        
    if State == 2 :
      f.axis = (2.0*sin(pi/100*i),0.0,2.0*cos(pi/100*i))
      #Base.axis = (5.0*sin(pi/100*i),0.0,5.0*cos(pi/100*i))
      #Tip.axis = (2.5*sin(pi/100*i),0.0,2.5*cos(pi/100*i))
      i = i + 1
