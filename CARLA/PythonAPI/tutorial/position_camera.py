
exec(open("init_notebook.py").read())
from helper import *
import time
client = connectToClient()

world = client.get_world()
spectator = set_camera_over_intersection(world)

extent = carla.Vector3D(x=100, y=100)
location = carla.Location(x=80, y=-133, z=0)
bounding_box = carla.BoundingBox(location, extent)
rotation = carla.Rotation(pitch=-90, yaw=95, roll=0)
extent1 = carla.Vector3D(z=20,y=20)

debug_helper = world.debug


debug_helper.draw_box(carla.BoundingBox(spectator.get_transform().location,extent1),spectator.get_transform().rotation, 0.05, carla.Color(20,160,255,0),0)

