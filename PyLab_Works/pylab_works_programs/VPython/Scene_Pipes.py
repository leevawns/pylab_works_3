#pipes.py by William Wright, wswright@ncsu.edu
from visual import *
from random import *

#Some constants
max_size = 25
max_num_pipes = 200
draw_rate = 25
draw_rate = 50
rotate_vector = (1,1,1)
do_rotate = true

#scene2 = display(title='Graph of position',width=600, height=600, fullscreen=1,center=(5,0,0), background=color.black)
our_pos = vector(0,0,0)#our current position
count = 0

f = frame()#creates a new frame to work with
sphere(frame=f, pos=our_pos, radius=1)
rotate_vector = vector(random(),random(),random())

scene.autoscale = False 
scene.autocenter = False
Forward_Up ( None, None, 100 )

while 1:#our loop
    rate(draw_rate)
    count = count + 1
    if do_rotate:
        f.rotate(angle=.01, axis=rotate_vector)
    if count > max_num_pipes:
        count = 0
        for obj in f.objects: #delete everything in the old frame
            obj.visible = false
        f = frame()#create a new frame
        #some tweaks for better performance after first wipe
        #scene2.autoscale = 0
        scene.autoscale = 0
        rotate_vector = vector(random(),random(),random())
    #generate a random number to determine if we are moving in x,y or z.
    which = randint(1,3)
    if which == 1:   #move in X direction
        #don't go outside of bounds, 10 in each direction
        max_move = max_size - our_pos.x #get maximum transition
        neg_move = -max_size - our_pos.x #get maximum negative transition
        if max_move < 0:
            max_move = 0
        x = randint(neg_move,max_move)
        newPipe = vector(x,0,0)
    elif which == 2: #move in Y direction
        #don't go outside of bounds, 10 in each direction
        max_move = max_size - our_pos.y #get maximum transition
        neg_move = -max_size - our_pos.y #get maximum negative transition
        if max_move < 0:
            max_move = 0
        y = randint(neg_move,max_move)
        newPipe = vector(0,y,0)
    else:            #move in Z direction
        #don't go outside of bounds, 10 in each direction
        max_move = max_size - our_pos.z #get maximum transition
        neg_move = -max_size - our_pos.z #get maximum negative transition
        if max_move < 0:
            max_move = 0
        z = randint(neg_move,max_move)
        newPipe = vector(0,0,z)

    #alright, we have our new pipe vector, so now lets create a
    #new pipe and then draw the sphere after it

    cylinder(frame=f, pos=our_pos, axis=newPipe, color=color.blue, radius=.75)
    our_pos = our_pos + newPipe
    sphere(frame=f, pos=our_pos, radius=1)
