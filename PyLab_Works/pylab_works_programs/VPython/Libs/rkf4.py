# RKF4:  Runga-Kutta-Fehlberg Integrator
#    Written by Charles Dyer, University of Toronto
#    Ported to C from Fortran by Charles Dyer
#    Ported to python by Charles Dyer, Allen Attard and Chris Burns (UofT)
#
# Usage:
#    1) You need to setup a function that defines the defferential
#       equations you wish to solve.  The function should have the following
#       template:
#          def rhs(x, y, yp)
#             x: (float)            the independent variable (e.g., time)
#             y: (float tuple  )     the dependent variables
#             yp: (float tuple)    the derivatives of the dependent variables
#                                   w.r.t. the independent variable
#
#    2) You need to set the initial conditions in y[]
#
#    4) loop and call rkf4() to advance each sub-interval.  rkf4() takes the
#       following parameters and returns a tuple:
#       (status, a_end, h_end) = rkf4(f, y, a, h, da, hmx, abserr, relerr, iter)
#          status (int):   returned status of the step.  One of:
#                          +ve:  success and status = iteration count
#                           -1:  too many iterations in this step
#                           -2:  bad input values of abserr, relerr, h or da
#                           -3:  h (step-size) has become too small for machine
#                                precision to handle.
#          a (float):      start of interval of the independent variable.  The
#                          end-point of the interval is returned (a_new)
#          h (float):      step size to try.  The actual value used is returned
#          da (float):     total step in independent variable (a_end = a + da)
#          hmx (float):    maximum step ever allowed.
#          iter (int):     maximum number of iterations allowed per step.
#              
#
# This is the source for an RKF4 or Runge-Kutta-Fehlberg 4th order
# ODE integrator. This code is adapted from original source in FORTRAN.
# 
# There are 22 constants needed for rkf as follows
#
# Sine there are no global variables in IDL (arg), set up a common block
#  with them.  This means you need to run init_rkf4() before using rkf4()
#  pretty clunky.
#
#
# This is the source for an RKF4 or Runge-Kutta-Fehlberg 4th order
# ODE integrator. This code is adapted from original source in FORTRAN.
# 
# There are 22 constants needed for rkf as follows:
#
from math import *
c11 = 9.375e-02                 # 3/32
c12 = 0.28125                   # 9/32
c13 = 0.375                     # 3/8

c21 = 0.8793809740555303        # 1932/2197
c22 = 3.277196176604461         # 7200/2197
c23 = 3.320892125625853         # 7296/2197
c24 = 0.9230769230769231        # 12/13

c31 = 2.032407407407407         # 439/216
c32 = 7.173489278752437         # 3680/513
c33 = 0.2058966861598441        # 845/4104

c41 = 0.2962962962962963        # 8/27
c42 = 1.381676413255361         # 3544/2565
c43 = 0.4529727095516569        # 1859/4104
c44 = 0.275                     # 11/40

c51 = 0.1157407407407407        # 25/216
c52 = 0.5489278752436647        # 1408/2565
c53 = 0.5353313840155945        # 2197/4104

c61 = 2.7777777777777778e-03    # 1/360
c62 = 2.9941520467836257e-02    # 128/4275
c63 = 2.9199893673577884e-02    # 2197/75240
c64 = 2.e-02                    # 1/50
c65 = 3.6363636363636364e-02    # 2/55

eps = 1.0;                         # Compute machine epsilon
while 1 + eps != 1: eps = eps/2.0
abserr = eps*100
relerr = eps*1000
 
#define SIGN(A,B) ((B) < 0 ? -(A) : (A))
def sign(a,b):                  # Copy sign of b to a (assuming a > 0).
  if b < 0: return -a
  else: return a

def rkf4(f,y,a,h,da,hmx,iter):
# f:      subroutine to compute y_prime: f(x,y,yp) where x = independent
#         variable, y = y[...] is the vector of dependent variables, and
#         yp = yp[...] is the vector of derivatives, ie. the RHS's of ODE's
# y[]:      dependent variables, initially = initial values 
# a:        start independent variable, end-point returned 
# h:        step-size to try, last used is returned 
# da:       total increment in independent variable 
# hmx:      maximum step allowed ever 
# iter:     maximum number of iterations allowed 
#
# rkf returns a success code as given below:
#      returned    status
#        +ve    success, and return value = iteration count
#        -1     exceeded iteration limit
#        -2     bad values supplied for abserr, relerr, h or da.
#        -3     h, the step-size, has become too small for machine precision
# In addition, a, h, and y[...] are returned. a is the end-point, and would
# be the next starting-point to continue integration. h is the step-size last
# used, and is usually a valid guess of what step to use on next interval.
#
# The return of status, a and h is in a tuple: (status,a,h)

  n = len(y)                                        # get dimension of system
  tmp = n*[0]; e = n*[0]; k1 = n*[0]; k2 = n*[0]    # Set up work space for
  k3 = n*[0]; k4 = n*[0]; k5 = n*[0]; k6 = n*[0]    # 8 vectors of length n
  
 
  if (relerr < 0) | (abserr < 0) | (hmx <= 0) | \
                    ( (relerr == 0) & (abserr == 0) ): return (-2,a,h)
  
  b = a + da                          # end point of the integration
  if abs(da) <= 13 * eps * max(abs(a), abs(b)) :
    return (-3,a,h)                   # da is too small.
  
  hmax = min(hmx, abs(da))
  if abs(h) <= 13 * eps * abs(a) : h = hmax
  kount = 0                           # zero function counter
  lasth = 0                           # not last step

  #-------------------------------------------------------------------------
  while 1 :                              # continue with new steps
    h = sign(min(abs(h), hmax), da)      # transfer sign of da to h
    if abs(b - a) <= 1.25 * abs(h) :     # close enough to leap
      h = b - a                          # size of last step required
      lasth = 1
    f(a, y, k1)                          # call the RHS function
    kount = kount + 1
  
    #-----------------------------------------------------------------------
    while 1 :                            # no good, try a new step size
      for i in range(n):
        tmp[i] = y[i] + 0.25 * h * k1[i] 
      arg = a + 0.25 * h 
      f(arg, tmp, k2)                    # call the RHS function
      for i in range(n):
        tmp[i] = y[i] + h * (c11 * k1[i] + c12 * k2[i]) 
      arg = a + h * c13 
      f(arg, tmp, k3)                    # call the RHS function
      for i in range(n):
        tmp[i] = y[i] + h * (c21 * k1[i] - c22 * k2[i] + c23 * k3[i]) 
      arg = a + h * c24 
      f(arg, tmp, k4)                    # call the RHS function
      for i in range(n):
        tmp[i] = y[i] + h * (c31 * k1[i] - 8 * k2[i] + c32 * k3[i] \
            - c33 * k4[i]) 
      arg = a + h 
      f(arg, tmp, k5)                    # call the RHS function
      for i in range(n):
        tmp[i] = y[i] + h * (-c41 * k1[i] + 2 * k2[i] - c42 * k3[i] \
            + c43 * k4[i] - c44 * k5[i]) 
      arg = a + 0.5 * h 
      f(arg, tmp, k6)                    # call the RHS function
      for i in range(n):
        tmp[i] = y[i] + h * (c51 * k1[i] + c52 * k3[i] \
            + c53 * k4[i] - 0.2 * k5[i])
        e[i] = h * (c61 * k1[i] - c62 * k3[i] - c63 * k4[i] \
            + c64 * k5[i] + c65 * k6[i])
      
      ratio = 0
      for i in range(n):
        te = abs(e[i]) / (relerr * abs(tmp[i]) + abserr) 
        ratio = max(ratio, te)           # largest error
      
      if ratio <= 1.0 :                  # are within error bound
        for i in range(n): y[i] = tmp[i] 
        a = a + h                        # increment start value by step size
        kount = kount + 5
      
        if kount >= iter :
          return (-1,a,h)                # too many function evaluations.
      
        if lasth == 1 :
          return (kount,a,h)             # successful return
        if ratio > 6.5536e-4 :
          h = h * (0.8/sqrt(sqrt(ratio)))       # make h larger
        else : h = h * 5.0 
      
        break                                   # jump to outer loop
  
      if ratio < 4096 :            # h changes by no more than a factor of 10
        h = h * (0.8/sqrt(sqrt(ratio)))         # errors are 5th order
      else : h = h * 0.1 
      
      if abs(h) <= 13 * eps * max(abs(a), abs(b)) :
        return (-3,a,h)                         # h has become too small.
      
      if kount >= iter :
        return (-1,a,h)               # too many function evaluations.
      lasth = 0                       # step too large, is no longer last step
    #-----------------------------------------------------------------------
  #-------------------------------------------------------------------------


# Here follows the graphing part.  We make a BLT graph 
