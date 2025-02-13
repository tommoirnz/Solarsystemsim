from vpython import *
import math
import pygame

# -------------------------------
# Initialize Pygame and the Joystick
# -------------------------------
pygame.init()
pygame.joystick.init()
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Joystick detected:", joystick.get_name())
else:
    print("No joystick detected. Exiting since joystick control is required.")
    exit()

# -------------------------------
# Rescaled Orbital Radii (adjusted for the larger Sun)
# -------------------------------
# Old Sun radius was 2.5, new Sun radius is 5.0.
# Rescale: new_distance = new_sun_radius + (old_distance - old_sun_radius)
new_sun_radius = 5.0
old_sun_radius = 2.5

mercury_orbit_radius = new_sun_radius + (3.9 - old_sun_radius)   # 5 + 1.4 = 6.4
venus_orbit_radius   = new_sun_radius + (7.3 - old_sun_radius)   # 5 + 4.8 = 9.8
earth_orbit_radius   = new_sun_radius + (10 - old_sun_radius)    # 5 + 7.5 = 12.5
mars_orbit_radius    = new_sun_radius + (15.2 - old_sun_radius)  # 5 + 12.7 = 17.7

jupiter_orbit_radius = new_sun_radius + (52 - old_sun_radius)    # 5 + 49.5 = 54.5
saturn_orbit_radius  = new_sun_radius + (96 - old_sun_radius)    # 5 + 93.5 = 98.5

# Orbital Periods for inner planets (simulation seconds; arbitrary for visual effect)
mercury_orbital_period = 20
venus_orbital_period   = 45
earth_orbital_period   = 60
mars_orbital_period    = 113

mercury_orbital_rate = 2 * math.pi / mercury_orbital_period
venus_orbital_rate   = 2 * math.pi / venus_orbital_period
earth_orbital_rate   = 2 * math.pi / earth_orbital_period
mars_orbital_rate    = 2 * math.pi / mars_orbital_period

# --- Jupiter Parameters (Outer Planet) ---
jupiter_orbital_period  = 712
jupiter_orbital_rate    = 2 * math.pi / jupiter_orbital_period
jupiter_radius          = 11.2
jupiter_spin_rate       = 2 * math.pi / (10/2.4)

# --- Saturn Parameters ---
saturn_orbital_period   = 1770
saturn_orbital_rate     = 2 * math.pi / saturn_orbital_period
saturn_radius           = 9.5
saturn_spin_rate        = 2 * math.pi / (10/1.8)

# Spin (Rotation) Rates (simulation seconds)
earth_spin_rate   = 2 * math.pi / 10
mercury_spin_rate = 2 * math.pi / 590
venus_spin_rate   = -2 * math.pi / 2430
mars_spin_rate    = 2 * math.pi / 10

# Planet Radii (relative to Earth radius = 1)
earth_radius   = 1
mercury_radius = 0.38
venus_radius   = 0.95
mars_radius    = 0.53

# Earth's Axial Tilt
axial_tilt = math.radians(23.5)

# Sun rotation: one full rotation every 27 days (scaled).
sun_spin_rate = 2 * math.pi / 270

# -------------------------------
# Define Ring Colours (with yellow replaced by grey)
# -------------------------------
pale_tan    = vector(210/255, 180/255, 140/255)
subtle_gray = vector(0.7, 0.7, 0.7)
subtle_pink = vector(1, 0.75, 0.8)
subtle_brown= vector(0.6, 0.4, 0.2)
ring_colors = [pale_tan, subtle_gray, subtle_pink, subtle_brown, subtle_gray]

# -------------------------------
# Scene Setup
# -------------------------------
scene.title = "Solar System: Sun, Mercury, Venus, Earth, Moon, Mars, Jupiter, Saturn"
scene.width = 2000    # Doubled width
scene.height = 1600   # Doubled height
scene.background = color.black
scene.center = vector(0, 0, 0)
scene.range = 300    # Expanded visible range
scene.ambient = color.gray(0.3)
scene.lights = []
light_source = distant_light(direction=vector(0, -1, -1), color=color.white)
additional_light = distant_light(direction=vector(-1, -1, 0), color=color.white)
scene.camera.pos = vector(30, 20, 30)
scene.camera.axis = -scene.camera.pos

# Adjust the camera clipping planes to prevent clipping.
scene.camera.near = 0.1
scene.camera.far = 500

# -------------------------------
# Create the Sun (now twice as large)
# -------------------------------
sun = sphere(pos=vector(0, 0, 0), radius=new_sun_radius,
             texture="2k_sun.jpg",
             emissive=True)

# -------------------------------
# Create the Earth with Tilt
# -------------------------------
spin_axis = rotate(vector(0, 1, 0), angle=axial_tilt, axis=vector(1, 0, 0))
month = 1
base_orbit_angle = 2 * math.pi * (month - 1) / 12
initial_pos = vector(earth_orbit_radius * math.cos(base_orbit_angle),
                     0,
                     earth_orbit_radius * math.sin(base_orbit_angle))
earth = sphere(pos=initial_pos, radius=earth_radius, texture=textures.earth)
earth.up = spin_axis

# -------------------------------
# Create the Moon with Local Texture
# -------------------------------
moon_orbit_radius = 1.5
moon_orbital_rate = 2 * math.pi / 5
moon = sphere(pos=earth.pos + vector(moon_orbit_radius, 0, 0),
              radius=0.27,
              texture="2k_moon.jpg")

# -------------------------------
# Create Mercury, Venus, and Mars with Local Textures
# -------------------------------
mercury = sphere(pos=vector(mercury_orbit_radius, 0, 0),
                 radius=mercury_radius,
                 texture="mercurymap.jpg")
venus = sphere(pos=vector(venus_orbit_radius, 0, 0),
               radius=venus_radius,
               texture="venusmap.jpg")
mars = sphere(pos=vector(mars_orbit_radius, 0, 0),
              radius=mars_radius,
              texture="2k_mars.jpg")

# -------------------------------
# Create Jupiter with Surface Map
# -------------------------------
jupiter = sphere(pos=vector(jupiter_orbit_radius, 0, 0),
                 radius=jupiter_radius,
                 texture="jupiter.jpg")

# -------------------------------
# Create Saturn with Multiple Thin Rings
# -------------------------------
saturn = sphere(pos=vector(saturn_orbit_radius, 0, 0),
                radius=saturn_radius,
                texture="saturn.jpg")

# ---- Saturn Outer Rings ----
saturn_rings = []
outer_ring_inner_bound = saturn_radius * 2.0
outer_ring_outer_bound = saturn_radius * 2.5
for i in range(10):
    ring_radius = outer_ring_inner_bound + (outer_ring_outer_bound - outer_ring_inner_bound) * i / 9.0
    new_ring = ring(pos=saturn.pos,
                    axis=vector(0, 1, 0),
                    radius=ring_radius,
                    thickness=saturn_radius * 0.01,
                    color=ring_colors[i % len(ring_colors)])
    saturn_rings.append(new_ring)

# ---- Saturn Inner Rings ----
saturn_inner_rings = []
inner_ring_inner_bound = saturn_radius * 1.75
inner_ring_outer_bound = saturn_radius * 2.0
num_inner_rings = 5
for i in range(num_inner_rings):
    ring_radius = inner_ring_inner_bound + (inner_ring_outer_bound - inner_ring_inner_bound) * i / (num_inner_rings - 1)
    new_ring = ring(pos=saturn.pos,
                    axis=vector(0, 1, 0),
                    radius=ring_radius,
                    thickness=saturn_radius * 0.01,
                    color=ring_colors[i % len(ring_colors)])
    saturn_inner_rings.append(new_ring)

# -------------------------------
# Joystick 6DOF Camera Control Function (with additional vertical movement)
# -------------------------------
def update_camera_from_joystick():
    global cam_forward, cam_up, cam_right
    trans_speed = 0.5
    rot_speed = 0.05
    deadzone = 0.1

    for event in pygame.event.get():
        pass

    # Pitch (Axis 1: pull back = pitch up, push forward = pitch down)
    pitch_val = joystick.get_axis(1)
    if abs(pitch_val) >= deadzone:
        pitch_angle = -rot_speed * pitch_val
        cam_forward = rotate(cam_forward, angle=pitch_angle, axis=cam_right)
        cam_up = rotate(cam_up, angle=pitch_angle, axis=cam_right)

    # Roll (Axis 0: left/right)
    roll_val = joystick.get_axis(0)
    if abs(roll_val) >= deadzone:
        roll_angle = rot_speed * roll_val
        cam_up = rotate(cam_up, angle=roll_angle, axis=cam_forward)
        cam_right = rotate(cam_right, angle=roll_angle, axis=cam_forward)

    # Throttle Translation (Forward/Reverse)
    if joystick.get_button(0):
        scene.camera.pos += cam_forward * trans_speed
    if joystick.get_button(1):
        scene.camera.pos -= cam_forward * trans_speed

    # New Buttons: Vertical Movement Up/Down
    if joystick.get_button(2):
        scene.camera.pos += vector(0, 1, 0) * trans_speed
    if joystick.get_button(3):
        scene.camera.pos += vector(0, -1, 0) * trans_speed

    scene.camera.axis = cam_forward * 20
    scene.camera.up = cam_up

# -------------------------------
# Setup 6DOF Camera Control Variables
# -------------------------------
cam_forward = scene.camera.axis.norm()
cam_up = scene.camera.up.norm()
cam_right = cross(cam_forward, cam_up).norm()

# -------------------------------
# UI Control: Month Slider
# -------------------------------
dummy_bind = lambda s: None
scene.append_to_caption("\n\nMonth (1 = Jan, ... 12 = Dec): ")
month_slider = slider(min=1, max=12, value=1, length=220, bind=dummy_bind)

# -------------------------------
# Light Toggle Switch
# -------------------------------
second_light_enabled = True
def toggle_second_light(evt):
    global second_light_enabled, additional_light
    if evt.key.lower() == 'l':
        second_light_enabled = not second_light_enabled
        if second_light_enabled:
            additional_light.color = color.white
            scene.ambient = color.gray(0.3)
            print("Additional light turned ON")
        else:
            additional_light.color = color.black
            scene.ambient = color.gray(0.05)
            print("Additional light turned OFF")
scene.bind('keydown', toggle_second_light)

# -------------------------------
# Main Animation Loop
# -------------------------------
t = 0
dt = 0.01

while True:
    rate(50)
    t += dt

    # Rotate the Sun
    sun.rotate(angle=sun_spin_rate * dt, axis=vector(0, 1, 0), origin=sun.pos)

    # --- Update Earth's Orbital Position and Rotation ---
    month = month_slider.value
    base_orbit_angle = 2 * math.pi * (month - 1) / 12
    earth_orbit_angle = base_orbit_angle + earth_orbital_rate * t
    earth.pos = vector(earth_orbit_radius * math.cos(earth_orbit_angle),
                       0,
                       earth_orbit_radius * math.sin(earth_orbit_angle))
    earth.rotate(angle=earth_spin_rate * dt, axis=spin_axis, origin=earth.pos)

    # --- Update Moon's Orbital Position ---
    moon_angle = moon_orbital_rate * t
    moon_offset = vector(moon_orbit_radius * math.cos(moon_angle),
                         0,
                         moon_orbit_radius * math.sin(moon_angle))
    moon.pos = earth.pos + moon_offset

    # --- Update Mercury's Orbital Position and Rotation ---
    mercury_angle = mercury_orbital_rate * t
    mercury.pos = vector(mercury_orbit_radius * math.cos(mercury_angle),
                         0,
                         mercury_orbit_radius * math.sin(mercury_angle))
    mercury.rotate(angle=mercury_spin_rate * dt, axis=vector(0, 1, 0), origin=mercury.pos)

    # --- Update Venus's Orbital Position and Rotation ---
    venus_angle = venus_orbital_rate * t
    venus.pos = vector(venus_orbit_radius * math.cos(venus_angle),
                       0,
                       venus_orbit_radius * math.sin(venus_angle))
    venus.rotate(angle=venus_spin_rate * dt, axis=vector(0, 1, 0), origin=venus.pos)

    # --- Update Mars's Orbital Position and Rotation ---
    mars_angle = mars_orbital_rate * t
    mars.pos = vector(mars_orbit_radius * math.cos(mars_angle),
                      0,
                      mars_orbit_radius * math.sin(mars_angle))
    mars.rotate(angle=mars_spin_rate * dt, axis=vector(0, 1, 0), origin=mars.pos)

    # --- Update Jupiter's Orbital Position and Rotation ---
    jupiter_angle = jupiter_orbital_rate * t
    jupiter.pos = vector(jupiter_orbit_radius * math.cos(jupiter_angle),
                         0,
                         jupiter_orbit_radius * math.sin(jupiter_angle))
    jupiter.rotate(angle=jupiter_spin_rate * dt, axis=vector(0, 1, 0), origin=jupiter.pos)

    # --- Update Saturn's Orbital Position, Rotation, and Rings ---
    saturn_angle = saturn_orbital_rate * t
    saturn.pos = vector(saturn_orbit_radius * math.cos(saturn_angle),
                        0,
                        saturn_orbit_radius * math.sin(saturn_angle))
    saturn.rotate(angle=saturn_spin_rate * dt, axis=vector(0, 1, 0), origin=saturn.pos)
    for ring_obj in saturn_rings:
        ring_obj.pos = saturn.pos
        ring_obj.rotate(angle=saturn_spin_rate * dt, axis=vector(0, 1, 0), origin=saturn.pos)
    for inner_ring_obj in saturn_inner_rings:
        inner_ring_obj.pos = saturn.pos
        inner_ring_obj.rotate(angle=saturn_spin_rate * dt, axis=vector(0, 1, 0), origin=saturn.pos)

    # --- Update the Light Direction (based on Earth's position) ---
    light_source.direction = norm(sun.pos - earth.pos)

    # --- Update Camera Control Using Joystick ---
    update_camera_from_joystick()
