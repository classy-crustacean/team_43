import math
length_pp = int(input("Enter the length of the parallel plates (m^2): "))
width_pp = int(input("Enter the width of the parallel plates (m^2): "))
dist_pp = int(input("Enter the distance between the parallel plates (m): "))
u_r = int(input("Enter the rate of airflow (m/s): ")) # This is just in the positive x-direction
voltage = int(input("Enter the voltage (V): "))



area_pp = length_pp * width _pp

# Set values and constants

# Particle size 1 represents PM2.5, and 2 represents PM10
particle_size = 0
while (particle_size == 0)
  particle_size = int(input("Choose particle size:\n1: PM2.5\n2: PM10\n"))
  if (particle_size == 1):
    d = 0.0000000025
    p = 0.0000000092
  elif (particle_size == 2):
    d = 0.00000001
    p = 0.0000000116
  else:
    print("invalid particle size")
    particle_size = 0

m_p = p*1000/(2.688*10^25)
g = 9.81
re = 1*10**-6
c_d = 24/re
p_a = 0.9093
a = ((1/4)*(math.pi)*(d)**2)

# Drag is in the x-direction. Everything else is in the y-direction.
a = (-(m_p * g) - ((1/2)(c_d * (p_s - p_a) * a * u_r * u__r)) + ((1/6) * (math.pi) * (p_s - p_a) * g * (d**3)) + (voltage) / (dist_pp))) / (m_p)
a_x = -1/2*c_D * p *a *u_r *u_r # The acceleration in the x-direction
a_y = (-m_p*g + 1/6 * math.pi * p *g * d**3 + voltage / dist_pp)/m_p # The acceleration in the y-direction
t = (u_r - math.sqrt(u_r**2-4*(1/4*c_D * p *a *u_r *u_r)(length_pp)))/(1/2**c_D * p *a *u_r *u_r) # The time it takes one particle to travel from one side of the ESP to the other
if t < 0:
  t = (u_r + math.sqrt(u_r**2-4*(1/4*c_D * p *a *u_r *u_r)(length_pp)))/(1/2**c_D * p *a *u_r *u_r) # # The time it takes one particle to travel from one side of the ESP to the other if
  # the initial calculation for t was negative

greatest_distance = 1/2(a_y)*t**2 # The furthest below the top plate that the particles can be before they are no longer picked up by the electrostaic participator
# Efficiency calculations
if greatest distance > dist_pp:
  efficiency = 100
else:
  efficiency = (1-(dist_pp-greatest_distance)/dist_pp)*100
