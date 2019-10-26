from __future__ import division
from visual import *

test_materials_individually = False

#scene.width = scene.height = 600
scene.range = 7
scene.forward = (1,-1,-1)

axis = (1,0,0)
##obj = box
##obj = cylinder; axis = (0,1,0)
obj = sphere
R = 0.9
L = 10

#scene.visible = 0
lite = local_light( pos = (0,0,0), color = (.6,.6,0.3) )
lite.m = sphere( pos = lite.pos, radius = 0.1, color = (1,1,.8), material = materials.emissive)

spheres = []
for mat in (materials.materials+[None]):
    if test_materials_individually: scene.visible = 0
    if mat: print mat.name
    spheres.append( obj( radius = R,
                         length = sqrt(2)*R,
                         height = sqrt(2)*R,
                         width = sqrt(2)*R,
                         axis = axis,
                         material = mat ) )
    if test_materials_individually: scene.visible = 1
    
box( pos = (0,-0.5*R,0), size=(L,R,L), material = materials.wood )

N = 4
xi = -L/2 + 1.5*R
dx = (L - 3*R)/(N-1)
for i,s in enumerate(spheres):
    if i <= 1:
        s.pos = (xi + (1-i+0.5)*dx, R, xi)
    elif 2 <= i <= 5:
        s.pos = (xi+(5-i)*dx, R, xi+1.5*dx)
    elif 6 <= i <= 8:
        s.pos = (xi+(i-6+0.5)*dx, R, xi+3*dx)
    else:
        s.pos = (xi+2.5*dx, R, xi)
    loc = s.pos-vector(0,R,0)
    #if hasattr(s.material, "name"):
    #    s.label = label( text = s.material.name, pos = loc )
    #else:
    #    s.label = label( text = "Legacy", pos = loc )
    if hasattr(s.material, "color"):
        s.color = s.material.color

#scene.visible = 1
Forward_Up ( None, None, 10 )

while 1:
    rate(50)
    for s in spheres:
        s.rotate( axis=scene.up, angle=.01 )
    lite.pos = lite.m.pos = scene.mouse.project( point=scene.center, normal=scene.forward )
    if scene.mouse.clicked:
        p = scene.mouse.getclick().pick
        if p and p is not lite.m:
            scene.center = p.pos
