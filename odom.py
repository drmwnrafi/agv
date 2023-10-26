from math import cos, sin,radians, degrees

# meter
radius = 0.05
wheelbase = 0.433
x_local = 0
y_local = 0

# deg/s
v_motor_kanan = 10
v_motor_kiri = 9

# deg
psi = 0

# m/s
vx_local = 0
vy_local = 0

omega = radius*(v_motor_kanan-v_motor_kiri)/wheelbase
psi += omega

if psi > 360:
    psi -= 360
elif psi < 0:
    psi+=360

vx_local = radius*(v_motor_kanan*cos(radians(psi))+v_motor_kiri*cos(radians(psi)))/2
vy_local = radius*(v_motor_kanan*sin(radians(psi))+v_motor_kiri*sin(radians(psi)))/2

x_local += vx_local
y_local += vy_local

print("x_local : ",x_local)
print("y_local : ",y_local)
print("vx_local : ",vx_local)
print("vy_local : ",vy_local)
print("psi : ", degrees(psi))
print("omega : ", degrees(omega))