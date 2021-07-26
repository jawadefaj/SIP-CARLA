import glob
import os
import sys
import time

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla


class ExtendedClient():
    pass

def filter_spawn_points(location,extent):
    client = carla.Client('127.0.0.1',2000)
    client.set_timeout(10.0)
    world = client.get_world()
    spawn_points = world.get_map().get_spawn_points()
    max_left = location.x-extent.x
    max_right = location.x+extent.x
    max_top = location.y+extent.y
    max_bottom = location.y-extent.y
    filtered_spawn_points=[]
    for spawn_point in spawn_points:
        x_co = spawn_point.location.x
        y_co = spawn_point.location.y
        if(x_co<max_left or x_co >max_right):
            break
        elif(y_co<max_bottom or y_co>max_top):
            break
        else:
            filtered_spawn_points.append(spawn_point)
    return filtered_spawn_points