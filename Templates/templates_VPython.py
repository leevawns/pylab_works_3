#icon = netcfgx3.ico

## Forward_Up

## Coordinate_Axis ( Length )
Coordinate_Axis ( 10 )

## Mouse events


## VPC Controls
VPC.Define () 
VPC.Define ( 2, 1 ) 
VPC.Define ( N_Button = 0, N_Slider = 0, N_Text = 0 )

## VPC Button
VPC.Set_Button ( N, Caption, Completion )

## VPC Text
VPC.Set_Text ( N, Caption, Completion = None )

## VPC Slider
VPC.Set_Slider ( 0, 'Voltage', 1, 12, 2, 'lin', '%5.1f', setbias )
VPC.Set_Slider ( N, Caption, Min, Max, Value,
                 LinLog, Format, Completion )

## Start Position
Forward_Up ( None, None, 25 )
Forward_Up ( ( 0, 3, -1 ), ( 0, 0, 1 ), -4 )

## Sphere
visual.sphere ()

## Cylinder
visual.cylinder (
  pos=(0,1,0), axis=(5,0,0), 
  color=(0,1,0), radius=0.1 )

## Arrow
visual.arrow (
  pos=(0,2,0), axis=(5,0,0), 
  shaftwidth=0.4 )

## Cone
visual.cone (
  pos=(0,3,0), axis=(5,0,0), 
  radius=0.5 )

## Pyramid
visual.pyramid (
  pos=(0,4,0), axis=(5,0,0), 
  color=(0.5,1,0.5), radius=0.5 )

## Ring
visual.ring (
  pos=(0,-1,0), axis=(0,0,1), 
  color=(0.5,1,0.5), thickness=0.2 )

## Box
visual.box (
  pos=(0,6,0), axis=(1,0,0), 
  color=(1,0,0), 
  length=5, width=4, height=2 )

## Ellipsoid
visual.ellipsoid (
  pos=(3,-1,0), axis=(0,0,1), 
  color=(1,0,0), 
  length=5, width=4, height=2 )

## Curve
visual.curve (pos=[(4,4),(5,4),(4,5)])

## Helix
visual.helix (
  pos=(0,2,1), axis=(5,0,0), 
  radius=2.5)

## Convex
#visual.convex

## Label
visual.label (pos=(-3,0,0),text='VPython')

## Faces
#visual.faces (

## Graph
#visual.graph


##|

## Color settings
ball.color = ( 1, 0, 1 )
ball.red 	 = 1
ball.green = 0
ball.blue  = 1

## Position settings
ball.pos = ( 0, 0, 0 )
ball.x	 = 0
ball.y   = 0
ball.z   = 0
ball.pos.x = 0
ball.pos.y = 0
ball.pos.z = 0




