#!/usr/bin/python3

# 0.05*((0.5*160e3)/(700e3-0.5*160e3))

vin = 0.05
#vin = 0.025

Ly= 700e3

#y2= 580e3 #-120e3
#y1= 540e3  #-160e3

y2= 640e3 #-60e3
y1= 600e3  #-100e3

#vout= -vin*(0.5*(y2+y1))/(Ly-0.5*(y2+y1))

vout= -vin*(Ly - 0.5*(y1+y2))/(0.5*(y1+y2))

print("vout="+str(vout))

print("vin fact="+str(vout/vin))
