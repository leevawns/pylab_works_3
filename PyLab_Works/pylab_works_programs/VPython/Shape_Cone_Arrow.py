# VPython carrow
#
# Make a cylindrical-bodied arrow with a cone point of identical dimensions
# as the standard built-in square arrow.
#
# v0.1: 18Jul2008 Aaron Miller- * seems to work on all files I've tried. Runs
#                 slower than the standard arrow, of course.  I'm not sure if
#                 it will handle being in a frame completely correctly.
#

# The best way to see how things look in your own files is to add the lines:
#   from carrow import *
#   arrow = carrow
# to the head of your programs. This will replace the standard "arrow" call
# with the cylindrical arrow for all instances. Hopefully it works well for you.

from __future__ import division
from visual import *

class carrow(): #object):
    def __init__(self, visible=1, frame=None, **kwargs):
        ra = self.__realarrow=arrow(visible=0, **kwargs)
        self.__realarrow.frame=frame
        self.__pos = vector(ra.pos)
        self.__axis = vector(ra.axis)
        self.__up = vector(ra.up)
        self.__color = ra.color
        self.__length = ra.length
        self.__shaftwidth = ra.shaftwidth
        self.__headwidth = ra.headwidth
        self.__headlength = ra.headlength 
        self.__caxis = vector(ra.axis)
        self.__caxis.mag = self.__axis.mag-self.__headlength
        self.__cy = cylinder(frame=frame, pos=self.__pos, axis=self.__caxis,
                             color=self.__color, radius=self.__shaftwidth/2.0,
                             up = self.__up, visible=visible)
        self.__co = cone(frame=frame,pos=self.__pos+self.__caxis, axis=self.__caxis,
                         radius=self.__headwidth/2.0, color=self.__color,
                         up = self.__up, visible=visible)
        self.__co.axis.mag = self.__headlength

    def __copy_from_realarrow(self):
        ra=self.__realarrow
        self.__length = ra.length
        self.__shaftwidth = ra.shaftwidth
        self.__headwidth = ra.headwidth
        self.__headlength = ra.headlength
        self.__axis = vector(ra.axis)
        self.__caxis = vector(ra.axis)
        self.__up = vector(ra.up)
        self.__caxis.mag = self.__axis.mag-self.__headlength
        self.__cy.axis=self.__caxis
        self.__cy.radius=self.__shaftwidth/2.0
        self.__cy.up = self.__up
        self.__co.pos = self.__pos+self.__caxis
        self.__co.axis = self.__caxis
        self.__co.radius = self.__headwidth/2.0
        self.__co.axis.mag = self.__headlength
        self.__co.up = self.__up

    def getframe(self):
        return self.__realarrow.frame
    def setframe(self,frame):
        self.__realarrow.frame=frame
        self.__co.frame = self.__cy.frame = self.__realarrow.frame
    frame = property(getframe,setframe)

    def getvis(self):
        return self.__cy.visible
    def setvis(self,visible):
        self.__cy.visible = self.__co.visible = visible
    visible = property(getvis,setvis)
        
    def getpos(self):
        return self.__pos

    def setpos(self, pos):
        self.__pos = vector(pos)
        self.__realarrow.pos=vector(pos)
        self.__cy.pos = vector(pos)
        self.__co.pos = vector(pos)+self.__caxis
    pos = property(getpos, setpos)

    def getaxis(self):
        return self.__axis

    def setaxis(self, axis):
        self.__axis = vector(axis)
        ra = self.__realarrow
        ra.axis=vector(axis)
        self.__copy_from_realarrow()

    axis = property(getaxis, setaxis)

    def getcolor(self):
        return self.__color
    
    def setcolor(self, color):
        self.__color = color
        self.__realarrow.color=color
        self.__cy.color = self.__realarrow.color
        self.__co.color = self.__realarrow.color

    color = property(getcolor, setcolor)

    def getred(self):
        return self.color[0]
    def setred(self, red):
        self.setcolor((red,self.color[1],self.color[2]))
    red = property(getred, setred)

    def getgreen(self):
        return self.color[1]
    def setgreen(self, green):
        self.setcolor((self.color[0],green,self.color[2]))
    green = property(getgreen, setgreen)

    def getblue(self):
        return self.color[2]
    def setblue(self, blue):
        self.setcolor((self.color[0],self.color[1],blue))
    blue = property(getblue, setblue)

    def gethl(self):
        return self.__headlength
    def sethl(self,hl):
        self.__realarrow.headlength=hl
        self.__copy_from_realarrow()
    headlength = property(gethl,sethl)

    def gethw(self):
        return self.__headwidth
    def sethw(self,hw):
        self.__realarrow.headwidth=hw
        self.__copy_from_realarrow()
    headwidth = property(gethw,sethw)

    def getfw(self):
        return self.__realarrow.fixedwidth
    def setfw(self,fw):
        self.__realarrow.fixedwidth=fw
    fixedwidth = property(getfw,setfw)

    def getsw(self):
        return self.__shaftwidth
    def setsw(self,sw):
        self.__realarrow.shaftwidth=sw
        self.__copy_from_realarrow()
    shaftwidth = property(getsw,setsw)

    def getup(self):
        return self.__up
    def setup(self,up):
        self.__realarrow.up=vector(up)
        self.__copy_from_realarrow()
    up = property(getup, setup)    
    
    def rotate(self,angle,axis=None,origin=None):
        if axis==None:
            axis=self.__axis
        if origin==None:
            origin=self.__pos
        self.__realarrow.rotate(angle=angle, axis=axis, origin=origin)
        self.__copy_from_realarrow()

# Set up window and sceen.
#scene = display(background=color.white)
scene.background = ( 1, 1, 1 )
b=carrow(axis=(0,0.5,0),color=color.blue)
a=carrow(axis=(0,0,1),color=color.red)

Forward_Up ( (-1,0,-2), None, 2 )

while True :
  rate ( 50 )
  
