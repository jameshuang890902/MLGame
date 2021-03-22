"""
The template of the main script of the machine learning process
"""
import random
import os.path
import pickle

"""
The template of the main script of the machine learning process
"""


class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        filename = 'arkanoid_n3_20210322_knn_model.pickle'
        filepath = os.path.join(os.path.dirname(__file__), filename)
        self.model = pickle.load(open(filepath, 'rb'))
        self.ball_served = False
        self.ball_x_last1 = 93
        self.ball_y_last1 = 395
        self.ball_x_last2 = 93
        self.ball_y_last2 = 395
        self.ball_x_last3 = 93
        self.ball_y_last3 = 395
        print("load----------")
        import random
        import time
        random.seed(time.time())

        self.serve_list = ["SERVE_TO_LEFT"]
        self.move_list = ["MOVE_LEFT"]
        serve = random.choice(self.serve_list)
        move = random.choice(self.move_list)

        self.serve_step = []
        self.serve_step.insert(0, serve)
        # num = random.randint(0, 3)
        # for i in range(num):
        #     self.serve_step.insert(0, move)
        # print(self.serve_step)


    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or
                scene_info["status"] == "GAME_PASS"):
            return "RESET"
        
        if len(self.serve_step) != 0:
            command = self.serve_step[0]
            self.serve_step.remove(command)
            return command

        else:
            ball_x = scene_info["ball"][0]
            ball_y = scene_info["ball"][1]
            platform_left = scene_info["platform"][0]
            platform_right = scene_info["platform"][0] + 40
            from_right_wall = 200 - (scene_info["ball"][0] + 5)
            from_bottom = 400 - (scene_info["ball"][1] + 5)
            frame = scene_info["frame"]
            ball_x_last1 = self.ball_x_last1
            ball_y_last1 = self.ball_y_last1
            ball_x_last2 = self.ball_x_last2
            ball_y_last2 = self.ball_y_last2
            ball_x_last3 = self.ball_x_last3
            ball_y_last3 = self.ball_y_last3

            left_diff = ball_x - platform_left
            right_diff = ball_x - platform_right

            platform_mid = scene_info["platform"][0] + 20

            ball_vector_x = ball_x - ball_x_last1
            ball_vector_y = ball_y - ball_y_last1
            ball_side = ball_x - (platform_left + 40)
            #'ball_x', 'ball_y', 'platform_left', 'ball_x_last1',
       #'ball_y_last1', 'ball_vector_x', 'ball_vector_y'
            platfrom_x = self.model.predict([[frame, ball_x, ball_y,
            	platform_right, 
                	ball_x_last1, ball_y_last1,
                    	ball_vector_x,	ball_vector_y
                                           ]])
            
    #         'frame', 'ball_x', 'ball_y', 'platform_left', 'platform_right',
    #    'from_right_wall', 'from_bottom', 'ball_x_last1', 'ball_y_last1',
    #    'ball_vector_x', 'ball_vector_y', 'left_diff', 'right_diff'
            self.ball_x_last3 = self.ball_x_last2
            self.ball_y_last3 = self.ball_x_last2
            self.ball_x_last2 = self.ball_x_last1
            self.ball_y_last2 = self.ball_x_last1
            
            self.ball_x_last1 = scene_info["ball"][0]
            self.ball_y_last1 = scene_info["ball"][1]

        if platfrom_x < scene_info['platform'][0] + 5:
            return "MOVE_LEFT"
        elif platfrom_x > scene_info['platform'][0] + 5:
            return "MOVE_RIGHT"
        else:
            return "NONE"

        

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
        print("load2----------")
        import random
        import time
        random.seed(time.time())
        serve = random.choice(self.serve_list)
        move = random.choice(self.move_list)

        self.serve_step = []
        self.serve_step.insert(0, serve)
        # num = random.randint(0, 3)
        
        # for i in range(num):
        #     self.serve_step.insert(0, move)
        # print(self.serve_step)

# 'command', 'ball_x', 'ball_y', 'platform_left', 'platform_right',
       #'from_right_wall', 'from_bottom', 'ball_x_last1', 'ball_y_last1'
