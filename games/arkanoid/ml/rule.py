class MLPlay:
    def __init__(self):
        self.ball_served = False
        self.ball_location_current = (93, 395)
        self.ball_location_last = (93, 395)
        self.ball_vector_current = (-7, -7)
        self.ball_vector_last = (-7, -7)


    def update(self, scene_info):
        if (scene_info["status"] == "GAME_OVER" or
                scene_info["status"] == "GAME_PASS"):
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            command = "SERVE_TO_RIGHT"
            
        
        else:
            
            #   update the current satae
            self.ball_location_current = scene_info["ball"]

            self.ball_vector_current = tuple(map(
                lambda i, j: i - j, self.ball_location_current, self.ball_location_last))
            
            
            
            #   the ball is move up
            if self.ball_vector_current[1] < 0:
                if scene_info["platform"][0] < 80:
                    command = "MOVE_RIGHT"

                elif scene_info["platform"][0] > 80:
                    command = "MOVE_LEFT"

                else:
                    command = "NONE"
            
            #   the ball is move down
            elif self.ball_vector_current[1] > 0:

                predict_x = self.ball_location_current[0]
                predict_y = self.ball_location_current[1]

                # the ball move right
                if self.ball_vector_current[0] > 0:
                    
                    while predict_y + 5 < 400 and predict_x < 200:
                        predict_x += self.ball_vector_current[0]
                        predict_y += self.ball_vector_current[1]
                    print("1" ,predict_x, predict_y)


                    if predict_x > 200:
                        predict_x = 200
                        print("2", predict_x, predict_y)

                        while predict_y + 5 < 400 and predict_x > 0:
                            predict_x -= self.ball_vector_current[0]
                            predict_y += self.ball_vector_current[1]
                        print("3", predict_x, predict_y)

                        if predict_x < 0:
                            predict_x = 0
                            print("4", predict_x, predict_y)
                            while predict_y + 5 < 400 and predict_x < 200:
                                predict_x -= self.ball_vector_current[0]
                                predict_y += self.ball_vector_current[1]
                            print("5", predict_x, predict_y)

                            if predict_y + 5 > 400:
                                predict_x -= predict_y - (400 - 5)
                                predict_y = 400 - 5
                                print("6", predict_x, predict_y)

                        elif predict_y + 5 > 400:
                            predict_x += predict_y - (400 - 5)
                            predict_y = 500 - 5
                            print("7", predict_x, predict_y)

                    elif predict_y + 5 > 400:
                        predict_x -= predict_y - (400 - 5)
                        predict_y = 400 - 5
                        print("8", predict_x, predict_y)


                # the ball move left
                elif self.ball_vector_current[0] < 0:

                    while predict_y + 5 < 400 and predict_x > 0:
                        predict_x += self.ball_vector_current[0]
                        predict_y += self.ball_vector_current[1]
                    print("1" ,predict_x, predict_y)


                    if predict_x < 0:
                        predict_x = 0
                        print("2", predict_x, predict_y)

                        while predict_y + 5 < 400 and predict_x < 200:
                            predict_x -= self.ball_vector_current[0]
                            predict_y += self.ball_vector_current[1]
                        print("3", predict_x, predict_y)

                        if predict_x > 200:
                            predict_x = 200
                            print("4", predict_x, predict_y)
                            while predict_y + 5 < 400 and predict_x > 0:
                                predict_x -= self.ball_vector_current[0]
                                predict_y += self.ball_vector_current[1]
                            print("5", predict_x, predict_y)

                            if predict_y + 5 > 400:
                                predict_x += predict_y - (400 - 5)
                                predict_y = 400 - 5
                                print("6", predict_x, predict_y)

                        elif predict_y + 5 > 400:
                            predict_x -= predict_y - (400 - 5)
                            predict_y = 400 - 5
                            print("7", predict_x, predict_y)

                    elif predict_y + 5 > 400:
                        predict_x += predict_y - (400 - 5)
                        predict_y = 400 - 5
                        print("8", predict_x, predict_y)
                
                print("predict_x", predict_x, "predict_y", predict_y)
                
                if predict_x < scene_info["platform"][0] + 5:
                    command = "MOVE_LEFT"
                
                elif predict_x > scene_info["platform"][0] + 35:
                    command = "MOVE_RIGHT"

                else:
                    command = "NONE"

            else:
                command = "NONE"
            
            #   update the last state to current state
            self.ball_location_last = self.ball_location_current
            self.ball_vector_last = self.ball_vector_current
        
        print("ball", scene_info["ball"])
        print("vector", self.ball_vector_current)
        return command

    def reset(self):
        self.ball_served = False
