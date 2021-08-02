

from agents.navigation.behavior_agent import BehaviorAgent


class spawnVehicleWithBehavior(BehaviorAgent):
    def __init__(self,
                 world,
                 vehicle_blueprint, 
                 spawn_point,
                 ignore_traffic_light, 
                 behavior):
        if world is None or vehicle_blueprint is None or spawn_point is None:
            return Exception("world/blueprint/spawn_point is None")
        self.vehicle = world.spawn_actor(vehicle_blueprint, spawn_point)

        super().__init__(self.vehicle, 
                         ignore_traffic_light=ignore_traffic_light, 
                         behavior=behavior)
        self.vehicle.set_autopilot()
        print('spawned a vehicle')
        return self.vehicle
