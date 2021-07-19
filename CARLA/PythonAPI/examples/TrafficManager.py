import glob
import os
import sys
import random
import time
import numpy as np
import cv2
import math
from collections import deque
import logging


from threading import Thread

from tqdm import tqdm

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla
from carla import VehicleLightState as vls
def main():
    client = carla.Client("localhost", 2000)
    client.set_timeout(25.0)
    vehicles_list = []
    synchronous_master = False
    try:
        tm = client.get_trafficmanager(8000)
        tm_port = tm.get_port()
        world = client.get_world()
        blueprint_library = world.get_blueprint_library()
        model = blueprint_library.filter("model3")[0]
        spawn_points = world.get_map().get_spawn_points()
        number_of_spawn_points = len(spawn_points)
        SpawnActor = carla.command.SpawnActor
        SetAutopilot = carla.command.SetAutopilot
        SetVehicleLightState = carla.command.SetVehicleLightState
        FutureActor = carla.command.FutureActor
        batch = []
        blueprints = world.get_blueprint_library().filter('vehicle.*')
        for n, transform in enumerate(spawn_points):
            if n>= 70:
                break
            blueprint = random.choice(blueprints)
            blueprint.set_attribute('role_name', 'autopilot')
            light_state = vls.NONE
            vehicle = SpawnActor(blueprint, transform).then(SetAutopilot(FutureActor, True, tm.get_port())).then(SetVehicleLightState(FutureActor, light_state))
            batch.append(vehicle)
        number = 0
        for response in client.apply_batch_sync(batch, synchronous_master):
            if response.error:
                logging.error(response.error)
            else:
                number+=1
                vehicles_list.append(response.actor_id)
        print('\nspawned %d vehicles' % number)
        tm.global_percentage_speed_difference(30.0)
        actor_list = world.get_actors()
        dangerous = vehicles_list[0:30]
        for id in dangerous:
            danger_car = actor_list.find(id)
            tm.ignore_lights_percentage(danger_car, 100)
            tm.distance_to_leading_vehicle(danger_car, 0)
            tm.vehicle_percentage_speed_difference(danger_car, -20)
        while True:
            world.wait_for_tick()
    finally:
        client.apply_batch([carla.command.DestroyActor(x) for x in vehicles_list])
        time.sleep(1.0)

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:

        print('\ndone.')