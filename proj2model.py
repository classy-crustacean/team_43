print("Enter the length of the parallel plates (m^2): ")
length_pp = int(input())
print("Enter the width of the parallel plates (m^2): ")
width_pp = int(input())
print("Enter the distance between the parallel plates (m): ")
dist_pp = int(input())
print("Enter the rate of airflow (m/s): ")
u_r = int(input()) # This is just in the positive x-direction
print("Enter the voltage (V): ")
voltage = int(input())

area_pp = length_pp * width _pp

# Set values and constants

m_p = ?
g = 9.81
re = 1*10**-6
c_d = 24/re
p_s = ?
P_a = 0.9093
d = ?
a = ((1/4)*(math.pi)*(d_p)**2)
sigma = ?
p = p_s-p_a

import math
# Drag is in the x-direction. Everything else is in the y-direction.
a = (-(m_p * g) - ((1/2)(c_d * (p_s - p_a) * a * u_r * u__r)) + ((1/6) * (math.pi) * (p_s - p_a) * g * (d**3)) + ((sigma * voltage) / (area_pp * dist_pp))) / (m_p)
a_x = -1/2*c_D * p *a *u_r *u_r
a_y = (-m_p*g + 1/6 * math.pi * p *g * d**3 + sigma * voltage / (area_pp * dist_pp))/m_p
t = (u_r - math.sqrt(u_r**2-4*(1/4*c_D * p *a *u_r *u_r)(length_pp)))/(1/2**c_D * p *a *u_r *u_r)
if t < 0:
  t = (u_r + math.sqrt(u_r**2-4*(1/4*c_D * p *a *u_r *u_r)(length_pp)))/(1/2**c_D * p *a *u_r *u_r)

greatest_distance = 1/2(a_y)*t**2
if greatest distance > dist_pp:
  efficiency = 100
else:
  efficiency = (1-(dist_pp-greatest_distance)/dist_pp)*100
