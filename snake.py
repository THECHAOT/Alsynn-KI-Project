import numpy as np
import copy

class Snake(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = np.zeros((height, width), dtype=int)
        self.snake = [[height // 2, width // 2]]
        self.field[self.snake[0][0], self.snake[0][1]] = 2
        self.apple_position = [0, 0]
        self.new_apple()
        self.reward_apple = 1
        self.reward_death = -1
        #self.reward_step = -0.01
        self.reward_step = -0.1
        self.reward = 0
        self.round_over = False
        self.steps = 0
        self.loop = False

    def reset_game(self):
        self.loop = False
        self.steps = 0
        self.reward = 0
        self.round_over = False
        self.field = np.zeros((self.height, self.width), dtype=int)
        self.snake = [[self.height // 2, self.width // 2]]
        self.field[self.snake[0][0], self.snake[0][1]] = 2
        self.new_apple()

    def new_apple(self):
        pos = np.random.randint(low=(0, 0), high=(self.height, self.width), size=2)
        while self.field[pos[0]][pos[1]] > 0:
            pos = np.random.randint(low=(0, 0), high=(self.height, self.width), size=2)
        self.apple_position = [pos[0], pos[1]]
        self.field[pos[0], pos[1]] = 3

    def move(self, direction):
        self.steps += 1
        if self.steps > 100:
            self.round_over = True
            self.loop = True
            return 0
        vec = [0, 0]
        if direction == 0:
            vec = [0, 1]
        elif direction == 1:
            vec = [-1, 0]
        elif direction == 2:
            vec = [0, -1]
        elif direction == 3:
            vec = [1, 0]
        if self.snake[-1][0] + vec[0] < 0 or self.snake[-1][0] + vec[0] >= self.height:
            self.round_over = True
            self.reward += self.reward_death
            return self.reward_death
        if self.snake[-1][1] + vec[1] < 0 or self.snake[-1][1] + vec[1] >= self.width:
            self.round_over = True
            self.reward += self.reward_death
            return self.reward_death
        new_pos = [self.snake[-1][0] + vec[0], self.snake[-1][1] + vec[1]]
        if self.field[new_pos[0], new_pos[1]] == 1 and new_pos != self.snake[0]:
            self.round_over = True
            self.reward += self.reward_death
            return self.reward_death
        if self.field[new_pos[0], new_pos[1]] == 0 or new_pos == self.snake[0]:
            old_head = self.snake[-1].copy()
            
            self.field[self.snake[-1][0], self.snake[-1][1]] = 1
            self.snake.append(new_pos)
            tail = self.snake.pop(0)
            self.field[tail[0]][tail[1]] = 0
            self.field[new_pos[0]][new_pos[1]] = 2
            
            head = self.snake[-1].copy()
            
            if abs(head[0]-self.apple_position[0]) + abs(head[1]-self.apple_position[1]) > abs(old_head[0]-self.apple_position[0]) + abs(old_head[1]-self.apple_position[1]):               
                self.reward += self.reward_step
                return self.reward_step
            else:
                return 0
        elif self.field[new_pos[0], new_pos[1]] == 3:
            self.field[self.snake[-1][0], self.snake[-1][1]] = 1
            self.snake.append(new_pos)
            self.field[new_pos[0], new_pos[1]] = 2
            if len(self.snake) < self.width * self.height:
                self.new_apple()
                self.reward += self.reward_apple
                self.steps = 0
                #return self.reward_apple + self.reward_step
                return self.reward_apple
            else:
                self.round_over = True
                self.reward += 10
                return 10

    def get_reward(self, direction):
        vec = [0, 0]
        if direction == 0:
            vec = [0, 1]
        elif direction == 1:
            vec = [-1, 0]
        elif direction == 2:
            vec = [0, -1]
        elif direction == 3:
            vec = [1, 0]

        if self.snake[-1][0] + vec[0] < 0 or self.snake[-1][0] + vec[0] >= self.height:
            return self.reward_death
        if self.snake[-1][1] + vec[1] < 0 or self.snake[-1][1] + vec[1] >= self.width:
            return self.reward_death
        new_pos = [self.snake[-1][0] + vec[0], self.snake[-1][1] + vec[1]]
        if self.field[new_pos[0], new_pos[1]] == 1 and new_pos != self.snake[0]:
            return self.reward_death
        if self.field[new_pos[0], new_pos[1]] == 0 or new_pos == self.snake[0]:
            return self.reward_step
        elif self.field[new_pos[0], new_pos[1]] == 3:
            return self.reward_apple

    def get_vision(self):
        vision = []
        distance_to_wall = []
        apple_in_direction = []
        tail_in_direction = []
        
        directions = [[0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1]]
        #directions = [[0, 1], [-1, 0], [0, -1], [1, 0]]
        for dir in directions:
            head = self.snake[-1].copy()
            i = 0
            #while True:
            head[0]+=dir[0]
            head[1]+=dir[1]
                #print(self.snake[-1],"+",dir,"=",head)
            if not (0<=head[0]<self.height and 0<=head[1]<self.width):
                distance_to_wall.append(1)
            else:
                distance_to_wall.append(0)
                #i+=1
        for dir in directions:
            head = self.snake[-1].copy()
            while True:
                head[0]+=dir[0]
                head[1]+=dir[1]
                if not (0<=head[0]<self.height and 0<=head[1]<self.width) or self.field[head[0]][head[1]] == 1:
                    apple_in_direction.append(0)
                    break
                if self.field[head[0]][head[1]] == 3:
                    apple_in_direction.append(1)
                    break
        for dir in directions:
            head = self.snake[-1].copy()
            while True:
                head[0]+=dir[0]
                head[1]+=dir[1]
                if not (0<=head[0]<self.height and 0<=head[1]<self.width):
                    tail_in_direction.append(0)
                    break
                if self.field[head[0]][head[1]] == 1:
                    tail_in_direction.append(1)
                    break
        for i in range(8):
            #vision.append((distance_to_wall[i]<1)*1)
            vision.append(distance_to_wall[i])
            vision.append(apple_in_direction[i])
            vision.append(tail_in_direction[i])
        #print(self.get_arr(vision,3),"   ",self.get_arr(vision,2),"   ",self.get_arr(vision,1))
        #print(self.get_arr(vision,4),"   ",[0,0,0],"   ",self.get_arr(vision,0))
        #print(self.get_arr(vision,5),"   ",self.get_arr(vision,6),"   ",self.get_arr(vision,7))
        #print("")
        return vision
        
        
    def get_octo_vision(self):
        vision = []
        distance_to_wall = []
        apple_in_direction = []
        tail_in_direction = []
        
        directions = [[0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1]]
        #directions = [[0, 1], [-1, 0], [0, -1], [1, 0]]
        for dir in directions:
            head = self.snake[-1].copy()
            i = 0
            #while True:
            head[0]+=dir[0]
            head[1]+=dir[1]
                #print(self.snake[-1],"+",dir,"=",head)
            if not (0<=head[0]<self.height and 0<=head[1]<self.width):
                distance_to_wall.append(1)
            else:
                if self.field[head[0]][head[1]] == 1:       
                    distance_to_wall.append(1)
                else:
                    distance_to_wall.append(0)
        for dir in directions:
            head = self.snake[-1].copy()
            while True:
                head[0]+=dir[0]
                head[1]+=dir[1]
                if not (0<=head[0]<self.height and 0<=head[1]<self.width) or self.field[head[0]][head[1]] == 1:
                    apple_in_direction.append(0)
                    break
                if self.field[head[0]][head[1]] == 3:
                    apple_in_direction.append(1)
                    break
        for dir in directions:
            head = self.snake[-1].copy()
            while True:
                head[0]+=dir[0]
                head[1]+=dir[1]
                if not (0<=head[0]<self.height and 0<=head[1]<self.width):
                    tail_in_direction.append(0)
                    break
                if self.field[head[0]][head[1]] == 1:
                    tail_in_direction.append(1)
                    break
        for i in range(8):
            #vision.append((distance_to_wall[i]<1)*1)
            vision.append(distance_to_wall[i])
            vision.append(apple_in_direction[i])
            vision.append(tail_in_direction[i])
        #print(self.get_arr(vision,3),"   ",self.get_arr(vision,2),"   ",self.get_arr(vision,1))
        #print(self.get_arr(vision,4),"   ",[0,0,0],"   ",self.get_arr(vision,0))
        #print(self.get_arr(vision,5),"   ",self.get_arr(vision,6),"   ",self.get_arr(vision,7))
        #print("")
        return vision
        
    def get_arr(self,vision,i):
        return vision[3*i:3*(i+1)]
        
    # Primitive Sicht enthält deutlich weniger Informationen

    # Output: 2d, Richtungsvektor zum Apfel
    def get_primitive_vision_1(self):
        vision = 4 * [0]
        head = self.snake[-1]
        apple = self.apple_position
        # vec = [apple[0] - head[0], apple[1] - head[1]]
        vec = [apple[1] - head[1], head[0] - apple[0]]
        # if vec[0] > 0:
        #     vec[0] = 1
        # if vec[1] > 0:
        #     vec[1] = 1
        vec[0] = np.sign(vec[0])
        vec[1] = np.sign(vec[1])

        return vec

    # Output: 3d, Richtungsvektor zum Apfel und 1 in dritter Komponente, falls auf dem Weg der Tod lauert
    def get_primitive_vision_2(self):
        vec = self.get_primitive_vision_1()
        if self.field[self.snake[-1][0] - vec[1], self.snake[-1][1]] == 1 or self.field[
            self.snake[-1][0], self.snake[-1][1] + vec[0]] == 1:
            vec.append(1)
        else:
            vec.append(0)
        return vec

    def get_primitive_vision_3(self):
        vec = self.get_primitive_vision_1()
        for i in range(4):
            if self.get_reward(i) == self.reward_death:
                vec.append(1)
            else:
                vec.append(0)
        return vec
 