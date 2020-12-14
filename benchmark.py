import snake as s
import network as nw
import numpy as np
import time
import matplotlib.pyplot as plt


def benchmark(vision, game, path):
    highscore = 0
    start = time.time()
    N = nw.Network()
    N.load_from_file(path)
    print(vision())
    iter = 1000
    loopcount = 0
    y = []
    i = 0
    percent = 0
    while i < iter:
        action = np.argmax(N.feed_forward(vision()))
        game.move(action)
        if game.round_over:
            if highscore < len(game.snake)-1:
                highscore = len(game.snake)-1
            i += 1
            if game.loop:
                loopcount += 1
            y.append(len(game.snake)-1)
            game.reset_game()
            if int(i * 100 / iter) > percent:
                percent = int(i * 100 / iter)
                print(percent, "%")

    print("Loops:", loopcount)
    print("Average:", sum(y)/iter)
    print("Highscore:", highscore)
    print("Median:", np.median(y))
    print("Dauer des Benchmarks:",time.time()-start,"s")
    old_N = nw.Network()
    old_N.load_from_file("benchmarked_network")
    old_N.write_to_file("previous_benchmarked_network")
    N.write_to_file("benchmarked_network")
    input()                                # muss da stehen, sonst schließt sich das terminal :(
    return loopcount
    
mygame = s.Snake(10,10)
benchmark(mygame.get_primitive_vision_3,mygame,r"test6")
