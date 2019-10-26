from visual import*
scene.background = (0,0,0)
origin = vector(0,0,0)
Forward_Up ( None, None, 20 )

posit = sphere()
posit.color = (0,0,1)
posit.radius = .4
posit.pos = (-2.37,0,0)
negat = sphere()
negat.color = (1,0,0)
negat.radius = .4
negat.pos = (2.63,0,0)
scene.autoscale = 0
i = -10
j=-10
k = 0
increment = .01
pq = 5
nq = -5

while True :
  rate ( 50 )
  if i<11:
    j = -10
    while j<11:
        mybox = box(pos=(i,j,0), axis = (1,0,0), length = .25, width = 0, height = .25)
        pdist = (mybox.pos - posit.pos)
        ndist = (mybox.pos - negat.pos)
        ppot = pq/(mag(pdist))
        npot = nq/(mag(ndist))
        pot = ppot+npot
        mybox.width=abs(pot/10)
        pdist.z = pot/20
        ndist.z = pot/20
        #pdist.z = 0
        #ndist.z = 0
        
        pfield = pq*pdist/(mag(pdist)**3)
        nfield = nq*ndist/(mag(ndist)**3)
        pfield.z = -pfield.z
        nfield.z = -nfield.z
        field = pfield + nfield
        green = 1 +.2*log(mag(field))
        if green < 0:
            green = 0
        mybox.color = (0, green, 0)
        if j%.5 ==0 and i%.5 == 0:
            pointer =arrow(pos=(i,j,pot/20), axis = .5*(field/(mag(field))), shaftwidth = .10)
            pointer.color = (1,0,1)
        #make the arrows 3-D
        #if j%1 == 0 and i%1 ==0:
         #   pointer = arrow(pos=(i,j,0), axis = (field.x/mag(field), field.y/mag(field), mag(field)), shaftwidth = .10)
         #   pointer.color = (0,0,0)
        j = j+.25
    i = i + .25
    '''while k<10:
    ball = sphere()
    ball.pos = ((posit.pos.x+.1*cos(k*pi/5+pi/10)),.1*sin(k*pi/5+pi/10),0)
    ball.radius = .05
    ball.color = (1,0,1)
    ball.direction = vector(0,0,0)
    ball.path = curve(color=ball.color, radius=ball.radius)
    ndist = (ball.pos-negat.pos)
    pdist = (ball.pos-posit.pos)
    while mag(ndist)>.10:
        pdist.x = (ball.pos.x-posit.pos.x)
        pdist.y = (ball.pos.y-posit.pos.y)
        pdist.z=0
        ndist.x = (ball.pos.x-negat.pos.x)
        ndist.y = (ball.pos.y-negat.pos.y)
        ndist.z=0
        pfield = pq*pdist/ (mag(pdist)**3)
        nfield = nq*ndist/ (mag(ndist)**3)
        #if mag(ball.pos-negat.pos)<(.71):
        #   break
        field = pfield + nfield
        ball.direction = field
        if mag(ball.pos-origin)>30:
            ball.pos = ball.pos + .5* (ball.direction/mag(ball.direction))
        else:
            ball.pos = ball.pos + (increment*(ball.direction/mag(ball.direction)))
        ball.path.append(pos=ball.pos)
        

    k=k+1'''
        
                
    
