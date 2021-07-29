exec(open("init.py").read())
from Configuration import Configuration
import carla


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


def draw_bounding_box(world, 
                      location=None, 
                      rotation=None, 
                      dim=None, 
                      thickness=0.5, 
                      color=carla.Color(255,0,0,0)):
    if location is None:
        bb_location = config.get('box_location')
        location = carla.Location(x=bb_location['x'], 
                                  y=bb_location['y'],
                                  z=bb_location['z'])
    if rotation is None:
        bb_rotation = config.get('box_rotation')
        rotation = carla.Rotation(pitch=bb_rotation['pitch'], 
                                  yaw=bb_rotation['yaw'],
                                  roll=bb_rotation['roll'])
    if dim is None:
        bb_dim = config.get('box_dimention')
        dim = carla.Vector3D(x=bb_dim['x'],
                             y=bb_dim['y'],
                             z=bb_dim['z'])
    bounding_box = carla.BoundingBox(location, dim)
    debug = world.debug
    # print(location, rotation, bounding_box, thickness, color)
    debug.draw_box(bounding_box,
                   rotation, 
                   thickness, 
                   color,
                   0)
    return bounding_box


def filter_spawn_points(bounding_box, spawn_points):
    
    location = bounding_box.location
    extent = bounding_box.extent
    
    max_left = location.x-extent.x
    max_right = location.x+extent.x
    max_top = location.y+extent.y
    max_bottom = location.y-extent.y
    filtered_spawn_points=[]
    for spawn_point in spawn_points:
        x_co = spawn_point.location.x
        y_co = spawn_point.location.y
        if(x_co<max_left or x_co >max_right):
            continue
        elif(y_co<max_bottom or y_co>max_top):
            continue
        else:
            filtered_spawn_points.append(spawn_point)
    return filtered_spawn_points