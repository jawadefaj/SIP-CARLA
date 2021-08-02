from helper import helper
import os
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

    def record_scene(self, filename="recording01.log", additional_param=True):
        self.client.start_recorder(filename, additional_param)

    def stop_record(self):
        self.client.stop_recorder()

    def replay_scene(self, filename="recording01.log", start=1, duration=0, camera=0, time_factor=1.0):
        self.set_recorder_playback(time_factor)
        self.client.replay_file(filename, start, duration, camera)

    def set_recorder_playback(self, time_factor):
        self.client.set_replayer_time_factor(time_factor)

    def store_recorded_data(self, filename="recording01.log", show_all= True, txt_file="output.txt"):

        output = self.client.show_recorder_file_info(filename, show_all)

        # creates the text file if it does not exist
        file = open(txt_file, "w+")
        file.close()

        # deletes all previous content from text file
        file = open(txt_file, "r+")
        file.truncate(0)
        file.close()

        # writes recorder output to text file
        text_file = open(txt_file, "w")
        n = text_file.write(output)
        text_file.close()
    