#!/usr/bin/python3

# 0.05*((0.5*160e3)/(700e3-0.5*160e3))

vin = 0.05

Ly= 700e3

y2= 100e3 #160e3
y1= 60e3  #120e3

vout= -vin*(0.5*(y2+y1))/(Ly-0.5*(y2+y1))

print("vout="+str(vout))

print("vin fact="+str(vout/vin))
