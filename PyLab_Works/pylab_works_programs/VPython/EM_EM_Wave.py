### EMWave.py
### Electromagnetic Plane Wave visualization (requires VPython)
### Rob Salgado
### salgado@physics.syr.edu     http://physics.syr.edu/~salgado/
### v0.5  2001-11-07 tested on Windows 2000
### v0.51 2003-02-16 tested on Windows 2000
###         with Python-2.1.1.exe and VPython-2001-10-31.exe
### v1.00 2004-03-21 tested on Windows 2000
###         with Python-2.3.3.exe and VPython-2003-10-15.exe

from visual import *

showNeighboringWaves=1

print"""
Electromagnetic Plane Wave visualization (v1.00) 2004-03-21
Rob Salgado (salgado@physics.syr.edu)

The blue arrows are Electric Field vectors.
The red arrows are Magnetic Field vectors.

The thick green vector representing
dE/dt ("time-rate-of-change-of-the-magnitude-of-the-electric-field")
is associated with the spatial arrangement of the magnetic field according to
the AMPERE-MAXWELL Law (as evaluated on the green loop).
[Use the RightHandRule to determine the sense of circulation on the green loop.
The direction of change of the electric field is determined by your thumb.]

The thick yellow vector representing
dB/dt ("time-rate-of-change-of-the-magnitude-of-the-magnetic-field")
is associated with the spatial arrangement of the electric field according to
the FARADAY Law (as evaluated on the yellow loop).
[Use the RightHandRule to determine the sense of circulation on the yellow loop.
The direction of change of the magnetic field is determined by the
opposite direction of where your thumb points (due to Faraday's minus sign).]

Intuitively, dE/dt tells the current value of E at that point to look like
the value of E at the point to its left (in this example).
In other words, the pattern of the electric field moves to the RIGHT.

Similarly, dB/dt tells the current value of B at that point to look like
the value of B at the point to its left (in this example).
In other words, the pattern of the magnetic field moves to the RIGHT.

Thus, this electromagnetic plane wave moves to the RIGHT.

WHAT YOU CAN DO:
    move the mouse to reposition the loops
    click the mouse to start and stop the animation
    change the showNeighboringWaves parameter to hide or show the other waves
"""

#scene = display(title="EM Wave (Rob Salgado)")
scene.autoscale=0
#scene.range=(6,6,6)
#scene.forward=(-1.0, -1.250, -4)
#scene.newzoom=1
 
Forward_Up ( (-1.0, -1.250, -4), None, 30 ) 

scene.background=color.black
EField=[]
EField2=[]
Ecolor=[color.blue,color.yellow, color.cyan]

BField=[]
BField2=[]
Bcolor=[color.red,color.green, color.magenta]
ddtcolor=[color.green, color.yellow]
Emax=4.
separation=10.

magnify=2.5
S=20
omega=0.1
wavelength=S
k=2*pi/wavelength

t=0
trun=0
fi=0

for i in arange(-S,S):
    Ev=arrow(pos=(i,0,0),axis=(0,0,0),color=Ecolor[0],shaftwidth=0.2, fixedwidth=1)
    EField.append(Ev)

for i in arange(-S,S):
    Bv=arrow(pos=(i,0,0),axis=(0,0,0),color=Bcolor[0],shaftwidth=0.2, fixedwidth=1)
    BField.append(Bv)


if showNeighboringWaves>0:
    for j in arange(1,3):
        for i in arange(-S,S):
            Ev=arrow(pos=(i,0,j*separation),axis=(0,0,0),color=Ecolor[0],shaftwidth=0.2, fixedwidth=1)
            EField.append(Ev)
        for i in arange(-S,S):
            Bv=arrow(pos=(i,0,j*separation),axis=(0,0,0),color=Bcolor[0],shaftwidth=0.2, fixedwidth=1)
            BField.append(Bv)

        for i in arange(-S,S):
            Ev=arrow(pos=(i,0,-j*separation),axis=(0,0,0),color=Ecolor[0],shaftwidth=0.2, fixedwidth=1)
            EField.append(Ev)
        for i in arange(-S,S):
            Bv=arrow(pos=(i,0,-j*separation),axis=(0,0,0),color=Bcolor[0],shaftwidth=0.2, fixedwidth=1)
            BField.append(Bv)

height=separation/2.
FaradayLoop=curve(pos=[(-1,-height,0),(-1,height,0),  (1,height,0), (1,-height,0),(-1,-height,0)],color=ddtcolor[1])
AmpereLoop= curve(pos=[(-1,0,-height),(-1,0,height),  (1,0,height), (1,0,-height),(-1,0,-height)],color=ddtcolor[0])

dBdt=arrow(pos=(fi,0,0),axis=(0,0,0),color=ddtcolor[1],shaftwidth=0.35,headwidth=0.7, fixedwidth=1)
dEdt=arrow(pos=(fi,0,0),axis=(0,0,0),color=ddtcolor[0],shaftwidth=0.35,headwidth=0.7, fixedwidth=1)
dBdtlabel = label(pos=(fi,0,0), text='dB/dt',color=ddtcolor[1], xoffset=20, yoffset=12, height=16, border=6)
dEdtlabel = label(pos=(fi,0,0), text='dE/dt',color=ddtcolor[0], xoffset=20, yoffset=12, height=16, border=6)

while 1:
    #rate(60) #v0.51 suggested by Jonathan Brandmeyer to reduce mouse polling when idle
    rate ( 50 )

    newfi=int(scene.mouse.pos.x)
    newfi=max(min(newfi,S-2),-(S-2))

    phase=k*(newfi-S)-omega*t
    if fi <> newfi:  #MOVE THE LOOP
        EField[S+fi-1].color=Ecolor[0]
        EField[S+fi+1].color=Ecolor[0]
        BField[S+fi-1].color=Bcolor[0]
        BField[S+fi+1].color=Bcolor[0]
        fi=newfi
        EField[S+fi-1].color=Ecolor[1]
        EField[S+fi+1].color=Ecolor[1]
        BField[S+fi-1].color=Bcolor[1]
        BField[S+fi+1].color=Bcolor[1]

        FaradayLoop.x[0]=fi-1
        FaradayLoop.x[1]=fi-1
        FaradayLoop.x[2]=fi+1
        FaradayLoop.x[3]=fi+1
        FaradayLoop.x[4]=FaradayLoop.x[0]

        AmpereLoop.x[0]=fi-1
        AmpereLoop.x[1]=fi-1
        AmpereLoop.x[2]=fi+1
        AmpereLoop.x[3]=fi+1
        AmpereLoop.x[4]=AmpereLoop.x[0]

    #UPDATE THE FIELDS
    for i in arange(0,len(EField)):
        amp=Emax*sin(k*(i%(2*S)-S)-omega*t)
        EField[i].axis.y=amp
        BField[i].axis.z=amp

    #UPDATE THE dB/dt
    dBdt.axis.z=magnify*omega*Emax*abs(cos(phase))*-sign( dot(EField[S+newfi+1].axis-EField[S+newfi-1].axis,vector(0,1,0)) )
    if dot(dBdt.axis,BField[S+newfi].axis)>0:
        dBdtlabel.text='dB/dt>0'
        dBdt.pos=(newfi,0,BField[S+newfi].axis.z)
    elif dot(dBdt.axis,BField[S+newfi].axis)<0:
        dBdtlabel.text='dB/dt<0'
        dBdt.pos=(newfi,0,BField[S+newfi].axis.z-dBdt.axis.z)
    else:
        dBdtlabel.text='dB/dt=0'
        dBdt.pos=(newfi,0,BField[S+newfi].axis.z)
    dBdtlabel.pos=BField[S+newfi].pos+BField[S+newfi].axis

    #UPDATE THE dE/dt
    dEdt.axis.y=magnify*omega*Emax*abs(cos(phase))*sign( dot(BField[S+newfi+1].axis-BField[S+newfi-1].axis,vector(0,0,-1)) )
    if dot(dEdt.axis,EField[S+newfi].axis)>0:
        dEdtlabel.text='dE/dt>0'
        dEdt.pos=(newfi,EField[S+newfi].axis.y,0)
    elif dot(dEdt.axis,EField[S+newfi].axis)<0:
        dEdtlabel.text='dE/dt<0'
        dEdt.pos=(newfi,EField[S+newfi].axis.y-dEdt.axis.y,0)
    else:
        dEdtlabel.text='dE/dt=0'
        dEdt.pos=(newfi,EField[S+newfi].axis.y,0)
    dEdtlabel.pos=EField[S+newfi].pos+EField[S+newfi].axis

    if scene.mouse.clicked:  #CLICK TOGGLE PAUSE/RUN TIME
        scene.mouse.getclick()
        trun = (trun+1)%2
    if trun>0:
        t+=0.1



