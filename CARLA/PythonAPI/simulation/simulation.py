from helper import helper

class simulation():
    def __init__(self, client=None):
        if client is None:
            client = helper.connectToClient()
        self.client = client
        self.world = client.get_world()
        self.bounding_box = None
        self.configure_simulation()
        pass

    def configure_simulation(self):
        helper.set_camera_over_intersection(self.world)
        self.bounding_box = helper.draw_bounding_box(self.world)
        pass

    def reset_simulation(self):
        helper.reset_carla_world(self.client)

    # record a scene 

    # replay a scene 