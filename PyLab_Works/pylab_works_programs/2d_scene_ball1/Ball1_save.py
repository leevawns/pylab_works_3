# create the ojects and initialize them
Set_Coordinates ( (-10, -10) , (200, None) )
Create_Axis ( ( 0, 0 ) )
R = 10
ball = Create_Circle ( R )
ball.x     = 0
ball.y     = 150
ball.vx    = 3
ball.Color = (200, 100, 0 )
dt   = 0.02

# simulation that runs continuously
while True :
  ball.x   = ball.x + ball.vx * dt
  ball.y   = ball.y - ball.vy * dt
  if ( ball.y <= R ) and ( ball.vy > 0 ) :
    ball.vy = -0.8 * ball.vy
    ball.y  = R
  else :
    ball.vy = ball.vy + 9.8 * dt
