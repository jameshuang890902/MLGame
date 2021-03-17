class MLPlay:
    

    
    
    def __init__(self):
        """
        Constructor
        """
        self.ball_served = False
        self.ball_move = "up_left"
        self.speed = 7  # todo add speed update for NORMAL

        self.location_current = [93, 395]
        self.location_last = [93 + 7, 395 + 7]


    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or
                scene_info["status"] == "GAME_PASS"):
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            command = "SERVE_TO_LEFT"

        else:

            #self.ball.update()
            #self.platform.update()
            #self.predict_obj = self.PREDICT(scene_info)
            self.location_current = list(scene_info["ball"])
            self.get_direction()
            print("ball direction", self.ball_move)
            self.location = list(scene_info["ball"])
            self.move = self.ball_move
            self.consider_bricks = scene_info["bricks"]
            self.consider_bricks_hard = scene_info["hard_bricks"]

            print("The all bound in this cycle:")
            # caculate the ball location when ball pass  y = 400
            while (self.location[1] < 400):
                # check which brick will be hit by ball
                hit_brick = self.check_hit_brick()
                print("check brick")
                if len(hit_brick) != 0:
                    print("hit_brick", hit_brick)
                    hit_side = self.check_hit_brick_side(hit_brick)
                    if hit_side == "horizontal":
                        if self.move == "up_left" or self.move == "up_right":
                            self.hit_horizontal(hit_brick[1] + 10)
                            print("hit_horizontal up")
                        elif self.move == "down_left" or self.move == "down_right":
                            self.hit_horizontal(hit_brick[1])
                            print("hit_horizontal down")
                    
                    elif hit_side == "vertical":
                        if self.move == "up_right" or self.move == "down_right":
                            self.hit_vertical(hit_brick[0])
                            print("hit vertical up")
                        elif self.move == "up_left" or self.move == "down_left":
                            self.hit_vertical(hit_brick[0] + 25)
                            print("hit vertical down")

                # check which wall will be hit by ball
                else:
                    hit_wall = self.check_hit_wall()

                    if hit_wall == "top_wall":
                        print("hit top wall")
                        self.hit_horizontal(0)
                    elif hit_wall == "left_wall":
                        print("hit left wall")
                        self.hit_vertical(0)
                    elif hit_wall == "right_wall":
                        print("hit right wall")
                        self.hit_vertical(200)
                    elif hit_wall == "no_hit":
                        print("just_fall")
                        self.fall()
                
                print("at predict", self.location)
                print("change direction", self.move)
                
            print("End this cycle")
            print()
            command = self.movement(scene_info)
            self.location_last = self.location_current



        return command

    # dicided the platform movement by predict location
    def movement(self, scene_info):

        if scene_info["platform"][0] + 35 < self.location[0]:
            command = "MOVE_RIGHT"

        elif scene_info["platform"][0] + 5 > self.location[0] + 5:
            command = "MOVE_LEFT"

        else:
            command = "NONE"

        return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False

    def get_direction(self):
        print(self.location_current, self.location_last)

        if self.location_current[0] == 0:
            if self.ball_move == "up_left":
                self.ball_move = "up_right"
            elif self.ball_move == "down_left":
                self.ball_move = "down_right"
        
        elif self.location_current[0] == 200:
            if self.ball_move == "up_right":
                self.ball_move = "up_left"
            elif self.ball_move == "down_right":
                self.ball_move = "down_left"

        elif self.location_current[1] == 0:
            if self.ball_move == "up_left":
                self.ball_move = "down_left"
            elif self.ball_move == "up_right":
                self.ball_move = "down_right"
        
        elif self.location_current[1] == 400:
            if self.ball_move == "down_left":
                self.ball_move = "up_left"
            elif self.ball_move == "down_right":
                self.ball_move = "up_right"
        
        if self.location_current[0] < self.location_last[0] and self.location_current[1] < self.location_last[1]:
            self.ball_move = "up_left"

        elif self.location_current[0] > self.location_last[0] and self.location_current[1] < self.location_last[1]:
            self.ball_move = "up_right"

        elif self.location_current[0] < self.location_last[0] and self.location_current[1] > self.location_last[1]:
            self.ball_move = "down_left"

        elif self.location_current[0] > self.location_last[0] and self.location_current[1] > self.location_last[1]:
            self.ball_move = "down_right"

        else:
            self.ball_move = "none"

    def power_of_distance(self, x1, y1, x2, y2):
        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    def check_hit_brick(self):

        possible_bricks = []
        closest_brick = []

        if self.move == "up_left":
            # print("check brick2")
            for brick in self.consider_bricks:
                if self.brick_left(brick) < self.ball_left() and self.brick_top(brick) < self.ball_top():
                    if 1 * (self.brick_left(brick) - self.ball_left()) + self.ball_top() <= self.brick_bottom(brick) and 1 * (self.brick_right(brick) - self.ball_left()) + self.ball_top() >= self.brick_top(brick):
                        possible_bricks.append(brick)


        elif self.move == "up_right":
            for brick in self.consider_bricks:
                if self.brick_right(brick) > self.ball_right() and self.brick_top(brick) < self.ball_top():
                    if -1 * (self.brick_left(brick) - self.ball_right()) + self.ball_top() >= self.brick_top(brick) and -1 * (self.brick_right(brick) - self.ball_right()) + self.ball_top() <= self.brick_bottom(brick):
                        possible_bricks.append(brick)

        elif self.move == "down_left":
            for brick in self.consider_bricks:
                if self.brick_left(brick) < self.ball_left() and self.brick_top(brick) > self.ball_top():
                    if -1 * (self.brick_left(brick) - self.ball_left()) + self.ball_bottom() >= self.brick_top(brick) and -1 * (self.brick_right(brick) - self.ball_left()) + self.ball_bottom() <= self.brick_bottom(brick):
                        possible_bricks.append(brick)

        elif self.move == "down_right":
            for brick in self.consider_bricks:
                if self.brick_right(brick) > self.ball_right() and self.brick_top(brick) > self.ball_top():
                    if 1 * (self.brick_left(brick) - self.ball_right()) + self.ball_bottom() <= self.brick_bottom(brick) and 1 * (self.brick_right(brick) - self.ball_right()) + self.ball_bottom() >= self.brick_top(brick):
                        possible_bricks.append(brick)



        if len(possible_bricks) != 0:
            min_distance = 1000000
            

            
            if self.move == "up_left":
                for brick in possible_bricks:
                    if self.power_of_distance(self.brick_right(brick),  self.ball_left(), self.brick_bottom(brick), self.ball_top()) <= min_distance:
                        closest_brick = brick
                        possible_bricks.remove(brick)
            
            elif self.move == "up_right":
                for brick in possible_bricks:
                    if self.power_of_distance(self.brick_left(brick),  self.ball_right(), self.brick_bottom(brick), self.ball_top()) <= min_distance:
                        closest_brick = brick
                        possible_bricks.remove(brick)

            elif self.move == "down_left":
                for brick in possible_bricks:
                    if self.power_of_distance(self.brick_right(brick),  self.ball_left(), self.brick_top(brick), self.ball_bottom()) <= min_distance:
                        closest_brick = brick
                        possible_bricks.remove(brick)

            elif self.move == "down_right":
                for brick in possible_bricks:
                    if self.power_of_distance(self.brick_left(brick),  self.ball_right(), self.brick_top(brick), self.ball_bottom()) <= min_distance:
                        closest_brick = brick
                        possible_bricks.remove(brick)

        return closest_brick

    def check_hit_brick_side(self, brick):
        if self.move == "up_left":
            # hit horizontal side
            if 1 * (self.brick_right(brick) - self.ball_left()) + self.ball_top() >= self.brick_bottom(brick):
                return "horizontal"
            # hit vertical side
            else :
                return "vertical"
        elif self.move == "up_right":
            # hit horizontal side
            if -1 * (self.brick_left(brick) - self.ball_right()) + self.ball_top() >= self.brick_bottom(brick):
                return "horizontal"
            # hit vertical side
            else:
                return "vertical"
        elif self.move == "down_left":
            # hit horizontal side
            if 1 * (self.brick_right(brick) - self.ball_left()) + self.ball_bottom() <= self.brick_top(brick):
                return "horizontal"
            # hit vertical side
            else:
                return "vertical"
        elif self.move == "down_right":
            # hit horizontal side
            if 1 * (self.brick_left(brick) - self.ball_right()) + self.ball_bottom() <= self.brick_top(brick):
                return "horizontal"
            # hit vertical side
            else:
                return "vertical"
        

    def check_hit_wall(self):
        
        if self.move == "up_left":
            # hit top wall
            if self.ball_top() - 0 <= self.ball_left() - 0:
                return "top_wall"
            # hit left wall
            else:   return "left_wall"

        elif self.move == "up_right":
            # hit top wall
            if self.ball_top() - 0 <= 200 - self.ball_right():
                return "top_wall"
            # hit right wall
            else: return "right_wall"
                
        elif self.move == "down_left":
            # hit left wall
            if 400 - self.ball_bottom() >= self.ball_left() - 0:
                return "left_wall"
            # no hit
            else:   return "no_hit"

        elif self.move == "down_right":
            # hit right wall
            if 400 - self.ball_bottom() >= 200 - self.ball_right():
                return "right_wall"
            # no hit
            else:   return "no_hit"
        
        else: return "no_hit"


    def hit_vertical(self, hit_x):

        if self.move == "up_left":
            self.move = "up_right"

            h_distance = self.ball_left() - hit_x
            self.location[0] = hit_x
            if h_distance % self.speed == 0:
                self.location[1] -= h_distance
            else:
                self.location[1] -= (int(h_distance / self.speed)+1) * self.speed
                if self.location[1] < 0:
                    self.location[1] = 0
                    

        elif self.move == "up_right":
            self.move = "up_left"
            h_distance = hit_x - self.ball_right()
            self.location[0] = hit_x - 5
            if h_distance % self.speed == 0:
                self.location[1] -= h_distance
            else:
                self.location[1] -= (int(h_distance /
                                         self.speed)+1) * self.speed
                if self.location[1] < 0:
                    self.location[1] = 0
        
        elif self.move == "down_left":
            self.move = "down_right"
            h_distance = self.ball_left() - hit_x
            self.location[0] = hit_x
            if h_distance % self.speed == 0:
                self.location[1] += h_distance
            else:
                self.location[1] += (int(h_distance /
                                         self.speed)+1) * self.speed
                if self.location[1] > 400:
                    self.location[1] = 400

        elif self.move == "down_right":
            self.move = "down_left"
            h_distance = hit_x - self.ball_right()
            self.location[0] = hit_x
            if h_distance % self.speed == 0:
                self.location[1] += h_distance
            else:
                self.location[1] += (int(h_distance /
                                         self.speed)+1) * self.speed
                if self.location[1] > 400:
                    self.location[1] = 400

    def hit_horizontal(self, hit_y):

        if self.move == "up_left":
            self.move = "down_left"
            v_distance = self.ball_top() - hit_y
            self.location[1] = hit_y
            if v_distance % self.speed == 0:
                self.location[0] -= v_distance
            else:
                self.location[0] -= (int(v_distance /
                                         self.speed)+1) * self.speed
                if self.location[0] < 0:
                    self.location[0] = 0

        elif self.move == "up_right":
            self.move = "down_right"
            v_distance = self.ball_top() - hit_y
            self.location[1] = hit_y
            if v_distance % self.speed == 0:
                self.location[0] += v_distance
            else:
                self.location[0] += (int(v_distance /
                                         self.speed)+1) * self.speed
                if self.location[0] > 200:
                    self.location[0] = 200

        elif self.move == "down_left":
            self.move = "up_left"
            v_distance = hit_y - self.ball_bottom()
            self.location[1] = hit_y - 5
            if v_distance % self.speed == 0:
                self.location[0] -= v_distance
            else:
                self.location[0] -= (int(v_distance /
                                         self.speed)+1) * self.speed
                if self.location[0] < 0:
                    self.location[0] = 0

        elif self.move == "down_right":
            self.move = "up_right"
            v_distance = hit_y - self.ball_bottom()
            self.location[1] = hit_y - 5
            if v_distance % self.speed == 0:
                self.location[0] += v_distance
            else:
                self.location[0] += (int(v_distance /
                                         self.speed)+1) * self.speed
                if self.location[0] > 200:
                    self.location[0] = 200

    def fall(self):

        v_distance = 400 - self.ball_bottom()
        self.location[1] = 400

        if v_distance % self.speed == 0:
            if self.move == "down_left":
                self.location[0] -= v_distance
            elif self.move == "down_right":
                self.location[0] += v_distance

        else:
            if self.move == "down_left":
                self.location[0] -= (int(v_distance /
                                         self.speed)+1) * self.speed
            elif self.move == "down_right":
                self.location[0] += (int(v_distance /
                                         self.speed)+1) * self.speed
    
    def ball_left(self):
        return self.location[0]

    def ball_right(self):
        return self.location[0] + 5

    def ball_top(self):
        return self.location[1]

    def ball_bottom(self):
        return self.location[1] + 5

    def brick_left(self, brick_location):
        return brick_location[0]

    def brick_right(self, brick_location):
        return brick_location[0] + 25

    def brick_top(self, brick_location):
        return brick_location[1]

    def brick_bottom(self, brick_location):
        return brick_location[1] + 10

    def up_left(self):
        return self.location

    def up_right(self):
        return [self.location[0] + 5, self.location[1]]

    def down_left(self):
        return [self.location[0], self.location[1] + 5]

    def down_right(self):
        return[self.location[0] + 5, self.location[1] + 5]
