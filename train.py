import numpy as np
import time
import network as nw
import snake as s
import random
import matplotlib.pyplot as plt
#import benchmark as bm


class Agent(object):
    def __init__(self,er_rate,er_end):
        self.path = "test6"
        self.width = 5
        self.height = 5
        #self.Q = nw.Network([2,6,4])
        self.Q = nw.Network([6, 6, 4])
        #self.Q = nw.Network([24, 18, 4])
        #self.Q = Network([6, 12, 12, 4])
        self.Q_target = nw.Network()
        #self.Q.load_from_file(self.path)
        self.update_Q_target(self.path)
        self.discount = 1
        #self.learning_rate = 0.0001
        self.learning_rate = 0.001
        #self.exploration_rate = 0.9#
        self.exploration_rate = er_rate
        self.exploration_init = er_rate
        self.exp_rate_end = er_end
        self.replay_memory = []
        self.game = s.Snake(self.width, self.height)
        self.vision = self.game.get_primitive_vision_3

    def update_Q_target(self, path=None):
        self.Q.write_to_file(path)
        self.Q_target.load_from_file(path)

    def train(self, iter):
        i = 0
        k = 1
        x = []
        highscore = [0]
        start = time.time()
        percent = 0
        self.replay_memory = []
        while i < iter:
            action = 0
            if np.random.uniform() < self.exploration_rate:
                action = np.random.randint(0, 4)
            else:
                action = np.argmax(self.Q.feed_forward(self.vision()))

            last_state = self.vision()               
            reward = self.game.move(action)
            self.replay_memory.append([last_state, action, reward, self.vision()])

            if k % 4 == 0 and len(self.replay_memory) >= 32:    
                batch = random.sample(list(range(len(self.replay_memory))), 32)
                for b in batch:
                    target = self.replay_memory[b][2] + self.discount * np.max(
                        self.Q_target.feed_forward(self.replay_memory[b][3]))
                    pos = self.replay_memory[b][1]
                    state = self.replay_memory[b][0]
                    self.Q.update_weights_and_bias(self.Q.back_propagation(state, pos, target),
                                                   self.learning_rate)

            if self.game.round_over:     
                if i == 0:
                    highscore[-1] = len(self.game.snake) - 1
                elif highscore[-1]>=len(self.game.snake) - 1:
                    highscore.append(highscore[-1])
                else:
                    highscore.append(len(self.game.snake) - 1)
                x.append(len(self.game.snake) - 1)
                self.game.reset_game()
                if int(i * 100 / iter) > percent: #Prozentanzeige
                    percent = int(i * 100 / iter)
                    print(percent, "%")
                    print(time.time() - start)
                    start = time.time()
                r = np.max((iter-i)/iter,0) #epsilon decay
                self.exploration_rate = (self.exploration_init-self.exp_rate_end)*r + self.exp_rate_end

                i += 1
            if k % 1000 == 0:
                self.update_Q_target(self.path)
            if len(self.replay_memory) > 50000:
                self.replay_memory.pop(0)
            k += 1
        return x,highscore


#A = Agent(0.2,0.04)
A = Agent(0.2,0.05)
my_list,highscore = A.train(5000)

z = [my_list[0]]
for i in range(1, len(my_list)):
    if i < 50:
        l = my_list[:i]
    else:
        l = my_list[i - 50:i]
    z.append(sum(l) / len(l))
y = range(len(my_list))
#plt.plot(y, my_list)
plt.plot(y, z)
plt.plot(y,highscore)
plt.show()
