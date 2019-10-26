from visual import *

# Capital letters constructed using curve functions.

# Joel Kahn
# 2004
# jj2kk4@yahoo.com

# This program is free software; you can redistribute it and/or
# modify it under the applicable terms of the GNU General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

autocenter = 1

#scene = display()
#scene.width = 1024
#scene.height = 738
#scene.x = 0
#scene.y = 0

letter_radius = 0.2

frame_A = frame()
frame_B = frame()
frame_C = frame()
frame_D = frame()
frame_E = frame()
frame_F = frame()
frame_G = frame()
frame_H = frame()
frame_I = frame()
frame_J = frame()
frame_K = frame()
frame_L = frame()
frame_M = frame()
frame_N = frame()
frame_O = frame()
frame_P = frame()
frame_Q = frame()
frame_R = frame()
frame_S = frame()
frame_T = frame()
frame_U = frame()
frame_V = frame()
frame_W = frame()
frame_X = frame()
frame_Y = frame()
frame_Z = frame()

curve_A = curve (radius = letter_radius, frame = frame_A)
curve_B = curve (radius = letter_radius, frame = frame_B)
curve_C = curve (radius = letter_radius, frame = frame_C)
curve_D = curve (radius = letter_radius, frame = frame_D)
curve_E = curve (radius = letter_radius, frame = frame_E)
curve_F = curve (radius = letter_radius, frame = frame_F)
curve_G = curve (radius = letter_radius, frame = frame_G)
curve_H = curve (radius = letter_radius, frame = frame_H)
curve_I = curve (radius = letter_radius, frame = frame_I)
curve_J = curve (radius = letter_radius, frame = frame_J)
curve_K = curve (radius = letter_radius, frame = frame_K)
curve_L = curve (radius = letter_radius, frame = frame_L)
curve_M = curve (radius = letter_radius, frame = frame_M)
curve_N = curve (radius = letter_radius, frame = frame_N)
curve_O = curve (radius = letter_radius, frame = frame_O)
curve_P = curve (radius = letter_radius, frame = frame_P)
curve_Q = curve (radius = letter_radius, frame = frame_Q)
curve_R = curve (radius = letter_radius, frame = frame_R)
curve_S = curve (radius = letter_radius, frame = frame_S)
curve_T = curve (radius = letter_radius, frame = frame_T)
curve_U = curve (radius = letter_radius, frame = frame_U)
curve_V = curve (radius = letter_radius, frame = frame_V)
curve_W = curve (radius = letter_radius, frame = frame_W)
curve_X = curve (radius = letter_radius, frame = frame_X)
curve_Y = curve (radius = letter_radius, frame = frame_Y)
curve_Z = curve (radius = letter_radius, frame = frame_Z)

curve_A.append (pos = (-0.5, -1.0, 0.0))
curve_A.append (pos = (0.0, 1.0, 0.0))
curve_A.append (pos = (0.5, -1.0, 0.0))
curve_A.append (pos = (0.25, 0.0, 0.0))
curve_A.append (pos = (-0.25, 0.0, 0.0))
frame_A.pos = (-12, 4, 0)

curve_B.append (pos = (-0.5, -1.0, 0.0))
curve_B.append (pos = (-0.5, 1.0, 0.0))
curve_B.append (pos = (0.0, 1.0, 0.0))
curve_B.append (pos = (1.0, 0.5, 0.0))
curve_B.append (pos = (0.0, 0.0, 0.0))
curve_B.append (pos = (-0.5, 0.0, 0.0))
curve_B.append (pos = (0.0, 0.0, 0.0))
curve_B.append (pos = (1.0, -0.5, 0.0))
curve_B.append (pos = (0.0, -1.0, 0.0))
curve_B.append (pos = (-0.5, -1.0, 0.0))
frame_B.pos = (-9, 4, 0)

curve_C.append (pos = (0.5, -1.0, 0.0))
curve_C.append (pos = (-0.5, -1.0, 0.0))
curve_C.append (pos = (-0.5, 1.0, 0.0))
curve_C.append (pos = (0.5, 1.0, 0.0))
frame_C.pos = (-6, 4, 0)

curve_D.append (pos = (-0.5, -1.0, 0.0))
curve_D.append (pos = (-0.5, 1.0, 0.0))
curve_D.append (pos = (0.0, 1.0, 0.0))
curve_D.append (pos = (1.0, 0.0, 0.0))
curve_D.append (pos = (0.0, -1.0, 0.0))
curve_D.append (pos = (-0.5, -1.0, 0.0))
frame_D.pos = (-3, 4, 0)

curve_E.append (pos = (0.5, 1.0, 0.0))
curve_E.append (pos = (-0.5, 1.0, 0.0))
curve_E.append (pos = (-0.5, 0.0, 0.0))
curve_E.append (pos = (0.0, 0.0, 0.0))
curve_E.append (pos = (-0.5, 0.0, 0.0))
curve_E.append (pos = (-0.5, -1.0, 0.0))
curve_E.append (pos = (0.5, -1.0, 0.0))
frame_E.pos = (0, 4, 0)

curve_F.append (pos = (0.5, 1.0, 0.0))
curve_F.append (pos = (-0.5, 1.0, 0.0))
curve_F.append (pos = (-0.5, 0.0, 0.0))
curve_F.append (pos = (0.0, 0.0, 0.0))
curve_F.append (pos = (-0.5, 0.0, 0.0))
curve_F.append (pos = (-0.5, -1.0, 0.0))
frame_F.pos = (3, 4, 0)

curve_G.append (pos = (0.5, 1.0, 0.0))
curve_G.append (pos = (-0.5, 1.0, 0.0))
curve_G.append (pos = (-0.5, -1.0, 0.0))
curve_G.append (pos = (0.5, -1.0, 0.0))
curve_G.append (pos = (0.5, 0.0, 0.0))
curve_G.append (pos = (0.0, 0.0, 0.0))
frame_G.pos = (6, 4, 0)

curve_H.append (pos = (-0.5, -1.0, 0.0))
curve_H.append (pos = (-0.5, 1.0, 0.0))
curve_H.append (pos = (-0.5, 0.0, 0.0))
curve_H.append (pos = (0.5, 0.0, 0.0))
curve_H.append (pos = (0.5, 1.0, 0.0))
curve_H.append (pos = (0.5, -1.0, 0.0))
frame_H.pos = (9, 4, 0)

curve_I.append (pos = (-0.5, 1.0, 0.0))
curve_I.append (pos = (0.5, 1.0, 0.0))
curve_I.append (pos = (0.0, 1.0, 0.0))
curve_I.append (pos = (0.0, -1.0, 0.0))
curve_I.append (pos = (0.5, -1.0, 0.0))
curve_I.append (pos = (-0.5, -1.0, 0.0))
frame_I.pos = (12, 4, 0)

curve_J.append (pos = (0.5, 1.0, 0.0))
curve_J.append (pos = (0.5, -1.0, 0.0))
curve_J.append (pos = (-0.5, -1.0, 0.0))
curve_J.append (pos = (-0.5, 0.0, 0.0))
frame_J.pos = (-12, 0, 0)

curve_K.append (pos = (0.5, 1.0, 0.0))
curve_K.append (pos = (-0.5, 0.0, 0.0))
curve_K.append (pos = (-0.5, 1.0, 0.0))
curve_K.append (pos = (-0.5, -1.0, 0.0))
curve_K.append (pos = (-0.5, 0.0, 0.0))
curve_K.append (pos = (0.5, -1.0, 0.0))
frame_K.pos = (-9, 0, 0)

curve_L.append (pos = (-0.5, 1.0, 0.0))
curve_L.append (pos = (-0.5, -1.0, 0.0))
curve_L.append (pos = (0.5, -1.0, 0.0))
frame_L.pos = (-6, 0, 0)

curve_M.append (pos = (-0.5, -1.0, 0.0))
curve_M.append (pos = (-0.5, 1.0, 0.0))
curve_M.append (pos = (0.0, 0.0, 0.0))
curve_M.append (pos = (0.5, 1.0, 0.0))
curve_M.append (pos = (0.5, -1.0, 0.0))
frame_M.pos = (-3, 0, 0)

curve_N.append (pos = (-0.5, -1.0, 0.0))
curve_N.append (pos = (-0.5, 1.0, 0.0))
curve_N.append (pos = (0.5, -1.0, 0.0))
curve_N.append (pos = (0.5, 1.0, 0.0))
frame_N.pos = (0, 0, 0)

curve_O.append (pos = (-0.5, -1.0, 0.0))
curve_O.append (pos = (-0.5, 1.0, 0.0))
curve_O.append (pos = (0.5, 1.0, 0.0))
curve_O.append (pos = (0.5, -1.0, 0.0))
curve_O.append (pos = (-0.5, -1.0, 0.0))
frame_O.pos = (3, 0, 0)

curve_P.append (pos = (-0.5, -1.0, 0.0))
curve_P.append (pos = (-0.5, 1.0, 0.0))
curve_P.append (pos = (0.5, 1.0, 0.0))
curve_P.append (pos = (0.5, 0.0, 0.0))
curve_P.append (pos = (-0.5, 0.0, 0.0))
frame_P.pos = (6, 0, 0)

curve_Q.append (pos = (0.25, -0.5, 0.0))
curve_Q.append (pos = (0.0, -1.0, 0.0))
curve_Q.append (pos = (-0.5, -1.0, 0.0))
curve_Q.append (pos = (-0.5, 1.0, 0.0))
curve_Q.append (pos = (0.5, 1.0, 0.0))
curve_Q.append (pos = (0.5, 0.0, 0.0))
curve_Q.append (pos = (0.25, -0.5, 0.0))
curve_Q.append (pos = (0.0, 0.0, 0.0))
curve_Q.append (pos = (0.5, -1.0, 0.0))
frame_Q.pos = (9, 0, 0)

curve_R.append (pos = (-0.5, -1.0, 0.0))
curve_R.append (pos = (-0.5, 1.0, 0.0))
curve_R.append (pos = (0.5, 1.0, 0.0))
curve_R.append (pos = (0.5, 0.0, 0.0))
curve_R.append (pos = (-0.5, 0.0, 0.0))
curve_R.append (pos = (0.5, -1.0, 0.0))
frame_R.pos = (12, 0, 0)

curve_S.append (pos = (0.5, 1.0, 0.0))
curve_S.append (pos = (-0.5, 1.0, 0.0))
curve_S.append (pos = (-0.5, 0.0, 0.0))
curve_S.append (pos = (0.5, 0.0, 0.0))
curve_S.append (pos = (0.5, -1.0, 0.0))
curve_S.append (pos = (-0.5, -1.0, 0.0))
frame_S.pos = (-12, -4, 0)

curve_T.append (pos = (-0.5, 1.0, 0.0))
curve_T.append (pos = (0.5, 1.0, 0.0))
curve_T.append (pos = (0.0, 1.0, 0.0))
curve_T.append (pos = (0.0, -1.0, 0.0))
frame_T.pos = (-9, -4, 0)

curve_U.append (pos = (-0.5, 1.0, 0.0))
curve_U.append (pos = (-0.5, -1.0, 0.0))
curve_U.append (pos = (0.5, -1.0, 0.0))
curve_U.append (pos = (0.5, 1.0, 0.0))
frame_U.pos = (-6, -4, 0)

curve_V.append (pos = (-0.5, 1.0, 0.0))
curve_V.append (pos = (0.0, -1.0, 0.0))
curve_V.append (pos = (0.5, 1.0, 0.0))
frame_V.pos = (-3, -4, 0)

curve_W.append (pos = (-0.5, 1.0, 0.0))
curve_W.append (pos = (-0.25, -1.0, 0.0))
curve_W.append (pos = (0.0, 1.0, 0.0))
curve_W.append (pos = (0.25, -1.0, 0.0))
curve_W.append (pos = (0.5, 1.0, 0.0))
frame_W.pos = (0, -4, 0)

curve_X.append (pos = (-0.5, 1.0, 0.0))
curve_X.append (pos = (0.0, 0.0, 0.0))
curve_X.append (pos = (0.5, 1.0, 0.0))
curve_X.append (pos = (-0.5, -1.0, 0.0))
curve_X.append (pos = (0.0, 0.0, 0.0))
curve_X.append (pos = (0.5, -1.0, 0.0))
frame_X.pos = (3, -4, 0)

curve_Y.append (pos = (-0.5, 1.0, 0.0))
curve_Y.append (pos = (0.0, 0.0, 0.0))
curve_Y.append (pos = (0.5, 1.0, 0.0))
curve_Y.append (pos = (0.0, 0.0, 0.0))
curve_Y.append (pos = (0.0, -1.0, 0.0))
frame_Y.pos = (6, -4, 0)

curve_Z.append (pos = (-0.5, 1.0, 0.0))
curve_Z.append (pos = (0.5, 1.0, 0.0))
curve_Z.append (pos = (-0.5, -1.0, 0.0))
curve_Z.append (pos = (0.5, -1.0, 0.0))
frame_Z.pos = (9, -4, 0)

Forward_Up ( None, None, 25 )

while True :
  pass