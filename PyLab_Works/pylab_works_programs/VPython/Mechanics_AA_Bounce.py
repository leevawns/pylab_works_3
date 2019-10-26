from visual import *

floor = box(length=4, height=0.5, width=4, color=color.blue)
 
ball = sphere(pos=(0,4,0), color=color.red)
ball.velocity = vector(0,-1,0)

#scene.visible = False
#scene.title = 'Panda' 
#scene.visible = True

Forward_Up ( None, None, 15 )

dt = 0.01
dt = 0.02
while 1:
    #rate(100)
    rate(50)
    ball.pos = ball.pos + ball.velocity*dt
    if ball.y < 1:
        ball.velocity.y = -ball.velocity.y
    else:
        ball.velocity.y = ball.velocity.y - 9.8*dt
