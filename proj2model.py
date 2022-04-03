from math import pi, sqrt
length_pp = float(input("Enter the length of the parallel plates (m): "))
width_pp = float(input("Enter the width of the parallel plates (m): "))
dist_pp = float(input("Enter the distance between the parallel plates (m): "))
u_r = float(input("Enter the rate of airflow (m/s): ")) # This is just in the positive x-direction
voltage = float(input("Enter the voltage (V): "))



area_pp = length_pp * width_pp

# Set values and constants

# Particle size 1 represents PM2.5, and 2 represents PM10
particle_size = int(input("Choose particle size:\n1: PM2.5\n2: PM10\n"))
while (not (particle_size == 1 or particle_size == 2)):
  print("invalid particle size")
  particle_size = int(input("Choose particle size:\n1: PM2.5\n2: PM10\n"))

if (particle_size == 1):
  d = 0.0000000025
  p = 1000
elif (particle_size == 2):
  d = 0.00000001
  p = 1000

m_p = p * pi / 6 * d**3 # Smog density times 1000L divided by 1000L/22.4L/mole * 6.022*10^23 particles/mole
g = 9.81
re = 1*10**-6
c_d = 24/re
p_a = 0.9093
cross_sectional_area = (0.25 * pi * d**2)
q = 1.602*10**-19

print("m_p", m_p)
print("g", g)
print('re', re)
print('c_d', c_d)
print('p_a', p_a)
print('cross sectional area', cross_sectional_area)

# Drag is in the x-direction. Everything else is in the y-direction.
a_x = -0.5 * c_d * p * cross_sectional_area * u_r * u_r / m_p # The acceleration in the x-direction
a_y = (-m_p * g + 1 / 6 * pi * p * g * d**3 + q * voltage / dist_pp) / m_p # The acceleration in the y-direction
t = (u_r - sqrt(u_r ** 2 - 4 * (0.25 * c_d * p * cross_sectional_area * u_r * u_r) * length_pp)) / (0.5 * c_d * p * cross_sectional_area * u_r * u_r) # The time it takes one particle to travel from one side of the ESP to the other
if t < 0:
  t = (u_r + sqrt(u_r**2-4*(1/4*c_d * p * cross_sectional_area * u_r * u_r) * length_pp)) / (0.5 * c_d * p * cross_sectional_area * u_r * u_r) # The time it takes one particle to travel from one side of the ESP to the other if
  # the initial calculation for t was negative
print(t)
greatest_distance = 0.5 * a_y * t ** 2 # The furthest below the top plate that the particles can be before they are no longer picked up by the electrostayic participator
print(greatest_distance)
# Efficiency calculations
if greatest_distance > dist_pp:
  efficiency = 100
else:
  efficiency = (1 - (dist_pp - greatest_distance) / dist_pp) * 100
print("efficiency: %.2f" % efficiency)
