from visual import *
from random import random

# Constants
cntBoxes = 5
spacing = .95
hBoxesD = cntBoxes / 2.0
hBoxes = int(hBoxesD)
hBoxes = hBoxesD - .5
offset = hBoxesD - .5

zt = 2.0 * pi / 360
hpi = pi / 2.0
inset = .01
mx = cntBoxes - inset

#scene = display(title='Rubix Cube', width=600, height=600,
#     center=(0,0,0), background=(0,.1,.1))
scene.range = (cntBoxes * 2, cntBoxes * 2, cntBoxes * 2)
#scene.fullscreen = 1
scene.ambient = 1

Forward_Up ( None, None, 10 ) 

fr = frame(size=(cntBoxes, cntBoxes, cntBoxes))
allParts = []

freeform = False
flyCamera = freeform
autoRotate = flyCamera


def AddFace(x, y, z):
    xPos = x-offset
    yPos = y-offset
    zPos = z-offset

    d = box(ax=-1, frame=fr, radius=spacing, pos=(xPos, yPos, zPos),
            size=(1, 1, 1), color=(.125, .125, .125))
            # size=(spacing, spacing, spacing), color=(1.*x/cntBoxes, 1.*y/cntBoxes, 1.*z/cntBoxes))
    allParts.append(d)


def AddSticker(x,y,z):
    AddFace(x,y,z)
    xPos = x-offset
    yPos = y-offset
    zPos = z-offset

    w = .002
    if x==0:
        allParts.append(box(ax=0, frame=fr, color=(1,.3,0), size=(w, spacing, spacing),pos=(xPos-.5, yPos, zPos)))
    if x==cntBoxes-1:
        allParts.append(box(ax=0, frame=fr, color=color.red, size=(w, spacing, spacing),pos=(xPos+.5, yPos, zPos)))
    if y==0:
        allParts.append(box(ax=1, frame=fr, color=color.yellow, size=(spacing, w, spacing),pos=(xPos, yPos-.5, zPos)))
    if y==cntBoxes-1:
        allParts.append(box(ax=1, frame=fr, color=color.green, size=(spacing, w, spacing),pos=(xPos, yPos+.5, zPos)))
    if z==0:
        allParts.append(box(ax=2, frame=fr, color=color.white, size=(spacing, spacing, w),pos=(xPos, yPos, zPos-.5)))
    if z==cntBoxes-1:
        allParts.append(box(ax=2, frame=fr, color=color.blue, size=(spacing, spacing, w),pos=(xPos, yPos, zPos+.5)))


def camera_fly(s,ang):
    if s == "left":
        fr.rotate(scene.forward, angle = -ang * zt, axis=scene.up)
    elif s == "right":
        fr.rotate(scene.forward, angle = ang * zt, axis=scene.up)
    elif s == "up":
        fr.rotate(scene.forward, angle = ang * zt, axis=cross(scene.up,scene.forward))
        fr.rotate(scene.up, angle = ang * zt, axis=cross(scene.up,scene.forward))
    elif s == "down":
        fr.rotate(scene.forward, angle = -ang * zt, axis=cross(scene.up,scene.forward))
        fr.rotate(scene.up, angle = -ang * zt, axis=cross(scene.up,scene.forward))

def ResetView():
    scene.forward = vector(-1,-1,-1)
    scene.up = vector(0,1,0)
    fr.axis = rotate(scene.up, angle = -hpi)
    fr.up = (1,1,0)


def decEq(d1, d2):
    return abs(d1 - d2) < 0.05


def decEg(d1, d2):
    return decEq(d1,d2) or (d1 > d2)


def RotatePlane(ppos, mpos):
    # Select all objects algorithm:
    # - Find the ppos.axis that has a 1.5.
    # - Find the mpos.axis that has a 1.
    # Rotate them around the 2nd axis pi/4 degrees. either + or -.
    # Round their positions back to cntBoxes.
    s = 0
    for i in range(3):
        s += abs(mpos[i])
    if s != 1:
        print "Out of bounds click!!"
        return [], 0,0,0,0,0,0,0,0

    axis = vector(0,0,0)
    orig = vector(0,0,0)
    angleRot = hpi
    axisTwist = -1
    matchAxis = 0
    for i in range(3):
        if decEq(abs(ppos[i]), hBoxesD):
            axis[i] = 1
    for i in range(3):
        if decEq(abs(mpos[i]), 1):
            axisTwist = i
            axis[i] = 2
            if (mpos[i]<0): angleRot = -angleRot
    #print "PPos", ppos,"Mpos", mpos
    #print "Axis", axis,
    for i in range(3):
        if axis[i] == 0:
            matchAxis = i
            axis[i] = 1
            orig[i] = ppos[i]
        elif axis[i] == 1:
            axis[i] = 0
        elif axis[i] == 2:
            axis[i] = 0
    # - Find all elements that match the 3rd axis value. 1.5 == 1.
    if (((matchAxis == 0) and (axisTwist == 1)) or
        ((matchAxis == 1) and (axisTwist == 2)) or
        ((matchAxis == 2) and (axisTwist == 0))
        ):
        angleRot = -angleRot
    s = 0
    for i in range(3):
        s += ppos[i];
    if s < 0: angleRot = -angleRot
    spinParts = []
    for part in allParts:
        p1 = part.pos[matchAxis]
        p2 = ppos[matchAxis]
        if (decEq(p1, p2) or \
            ((decEq(p2, hBoxes) and decEg(p1, p2)) or \
            (decEq(p2, -hBoxes) and decEg(p2, p1)))):
            spinParts.append(part)
            
    angleRep = 7
    angleRot = angleRot / angleRep
    #print "Axis", axis, "AxisTwist", axisTwist
    #print "Orig", orig, "Match", matchAxis, "#", len(spinParts), "Ang", angleRot / pi
    #print
    return spinParts, axis[0], axis[1], axis[2], \
           orig[0], orig[1], orig[2], angleRep, angleRot


def MakeRandomClick():
    axis = -1
    for part in allParts:
        axis = -1
        if part.ax >= 0:
            for i in range(3):
                if decEq(abs(part.pos[i]), hBoxesD):
                    axis = i;
            if axis >= 0:
                if random() < .1:
                    break;
    #print axis, part.size[axis],

    axis2 = axis-1
    if axis2 < 0: axis2 = 2
    mpos = vector(0, 0, 0)
    mpos[axis2] = 1
    return part.pos, mpos

#arrow(color=(1,0,0), axis=(cntBoxes,0,0), shaftwidth = .2)
#arrow(color=(0,1,0), axis=(0,cntBoxes,0), shaftwidth = .2)
#arrow(color=(0,0,1), axis=(0,0,cntBoxes), shaftwidth = .2)

f = AddSticker
for x in range(cntBoxes):
    for y in range(cntBoxes):
        for z in range(cntBoxes):
            f(x, y, z)
  
ResetView()
timeFreeMode = random() * 250 + 250
angleRep = 0
angleWait = 0

while 1:
    rate(50)

    if angleRep > 0:
        angleWait -= 1
        if angleWait < 0:
            angleWait = 4
            angleRep -= 1
            for part in spinParts:
                part.rotate(axis=spinAxis, origin=spinOrig, angle=angleRot)
    else:
        if scene.mouse.events:
            m = scene.mouse.getevent()
            if m.click == "left":
                if m.pick != None:
                    temp1 = (m.pickpos - m.pick.pos) * 3
                    temp1 = (round(temp1[0]),round(temp1[1]),round(temp1[2]))
                    (spinParts, ax,ay,az, ox,oy,oz, angleRep, angleRot) = \
                            RotatePlane(m.pick.pos, temp1)
                    spinAxis=(ax,ay,az)
                    spinOrig=(ox,oy,oz)

    if freeform:
        timeFreeMode -= 1
        if (timeFreeMode <= 0):
            flyCamera = not flyCamera
            autoRotate = not flyCamera
            timeFreeMode = random() * 500 + 250
        if (random() < .03) and (angleRep == 0):
            (ppos, mpos) = MakeRandomClick()
            (spinParts, ax,ay,az, ox,oy,oz, angleRep, angleRot) = \
                RotatePlane(ppos, mpos)
            spinAxis=(ax,ay,az)
            spinOrig=(ox,oy,oz)
            
            
    if flyCamera:
        ang = acos(dot(scene.up, cross(scene.up,scene.forward))) * .005
        scene.forward = rotate(scene.forward, angle=ang * random())
    elif autoRotate:
        scene.forward = rotate(scene.forward, angle=.5 * zt, axis=scene.up)
        
    if scene.kb.keys:
        s = scene.kb.getkey()
        camera_fly(s, 5)
        if s == " ":
            autoRotate = not autoRotate
            if autoRotate:
                flyCamera = False
        elif s == "f":
            flyCamera = not flyCamera
            if flyCamera:
                autoRotate = False
        elif s == "r":
            ResetView()
            autoRotate = False
            flyCamera = False
            freeform = False
        elif s == 'q':
            freeform = not freeform
            if freeform == False:
                autoRotate = False
                flyCamera = False
            else:
                flyCamera = True
