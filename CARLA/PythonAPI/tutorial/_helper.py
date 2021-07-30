from random import random
import carla
from Configuration import Configuration

config = Configuration()

def connectToClient(host=None, port=None, timeout=5):
    if host is None:
        host = config.get('host')
    if port is None:
        port = config.get('port')
        
    try:
        client = carla.Client(host, port)
        client.set_timeout(timeout)
    except RuntimeError:
        print('Failed to connect to %s:%d.' % (host, port))
    
    if client is not None:
        print('CARLA %s connected at %s:%d.' % (client.get_server_version(), host, port))
        print(client)
        return client
    pass

def initializeTrafficManager(client=None, 
                             global_distance_leading_vehicle=1.0,
                             hybrid_mode=False,
                             synch_mode=False):
    if client is None:
        print("client can not be None")
        return
    world = client.get_world()
    traffic_manager = client.get_trafficmanager(8000)
    traffic_manager.set_global_distance_to_leading_vehicle(global_distance_leading_vehicle)
    if hybrid_mode:
        traffic_manager.set_hybrid_physics_mode(True)
    if synch_mode:
        synchronous_master = set_synch_mode(world, traffic_manager)
    return traffic_manager



def set_synch_mode(world, traffic_manager):
    settings = world.get_settings()
    traffic_manager.set_synchronous_mode(True)
    if not settings.synchronous_mode:
        synchronous_master = True
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = 0.05
        world.apply_settings(settings)
        print("synchronous_master set")
    else:
        synchronous_master = False
    
    return synchronous_master

def spawnVehicleOnWayPoint(world=None,
                           traffic_manager=None, 
                           vehicle_bp=None,
                           spawn_point_transform=None,
                           role_name='autopilot'):
    if None not in (world, traffic_manager, vehicle_bp, spawn_point_transform):
        # if vehicle_bp.has_attribute('color'):
        #     color = random.choice(vehicle_bp.get_attribute('color').recommended_values)
        #     vehicle_bp.set_attribute('color', color)
        # if vehicle_bp.has_attribute('driver_id'):
        #     driver_id = random.choice(vehicle_bp.get_attribute('driver_id').recommended_values)
        #     vehicle_bp.set_attribute('driver_id', driver_id)
        # vehicle_bp.set_attribute('role_name', role_name)
        spawned_vehicle = world.spawn_actor(vehicle_bp, spawn_point_transform)
        spawned_vehicle.set_autopilot(True)
        return spawned_vehicle
    else:
        print("vehicle_bp/spawn_location/traffic_manager/world can not be None")
        return

def destroyAllVehicleActor(world=None, vehicle_list=None):
    if vehicle_list is None and world is None:
        print("world and vehicle_list is empty")
        return 
    if vehicle_list is None:
        vehicle_list = world.get_actors().filter('vehicle.*')
    if len(vehicle_list) == 0:
        print("empty vehicle list")
    for vehicle in vehicle_list:
        vehicle_id = vehicle.id
        print('destroying vehicle with ID ', vehicle_id, vehicle.destroy())
    

def resetCarlaWorld(client):
    if client is not None:
        client.reload_world(True)
    else:
        print("empty client can not reload world")

def spawnObjectOnRoad(world, object_bp, spawn_location):
    pass

def set_camera_over_intersection(world, location=None, rotation=None):
    if world is None:
        return Exception('world object can not be empty')
    if location is None:
        cam_location = config.get('camera_location')
        location = carla.Location(x=cam_location['x'], y=cam_location['y'], z=cam_location['z'])
    if rotation is None:
        cam_rotation = config.get('camera_rotation')
        rotation = carla.Rotation(pitch=cam_rotation['pitch'], 
                                  yaw=cam_rotation['yaw'], 
                                  roll=cam_rotation['roll'])
    spectator = world.get_spectator()
    spectator.set_transform(carla.Transform(location, rotation))
    pass

def create_bounding_box(location, rotation, dim, color):
    if location is None:
        location = carla.Location(x=80, y=-133, z= 0)
    if rotation is None:
        rotation = carla.Rotation(pitch=-90, yaw=95, roll=0)
    bounding_box = carla.BoundingBox(location, carla.Vector3D(20,50,50))
    return bounding_box
    

def draw_bounding_box(world, bounding_box, color, thickness, life_time):

    pass

def test_configuration():
    loc = config.get('camera_location')
    rot = config.get('camera_rotation')
    print(loc, rot)