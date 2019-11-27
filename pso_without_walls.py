import numpy as np
import sys
import json
from optparse import OptionParser

C1 = 1  # stala dla poprzedniej predkosci
C2 = 0.8  # stala dla lokalnego rozwiazania
C3 = 1  # stala dla globalnego rozwiazania


class Board:

    def __init__(self, shape, coin_percentage=0.4, board=None):
        self.shape = shape
        self.board = self.load_board(board) if board is not None else (np.random.rand(*shape) > (1.0 - coin_percentage))  
        self.start = np.array(list(map(lambda x: int((x - 1) / 2), shape)))
        self.move_mapping = [np.array([-1, 0]), np.array([0, 1]), np.array([1, 0]), np.array([0, -1])]      

    def load_board(self, board):
        with open(board, "rb") as in_file:
            return np.load(in_file)

    def get_coins_number(self, moves):
        current_poz = self.start.copy()
        result = int(self.board[tuple(current_poz)])
        visited = {tuple(current_poz)}
        for move in moves:
            current_poz += self.move_mapping[move]
            if tuple(current_poz) not in visited:
                visited.add(tuple(current_poz))
                result += int(self.board[tuple(current_poz)])
        return result


def init_parser():
    parser =  OptionParser()
    parser.add_option("-i", dest="i",   default=None, help="Sciezka pliku wejsciowego") 
    parser.add_option("-o", dest="o",   default=None, help="Sciezka pliku wyjsciowego") 
    parser.add_option("-s", dest="seed",default=None, help="Seed dla np.random") 
    parser.add_option("-c", dest="cfg", default="config.json", help="Sciezka pliku konfiguracyjnego")  
    return parser


def get_distance(path_1, path_2):
    return np.array(list(map(lambda x: x if x >= 0 else 4 + x, (path_1 - path_2))))


def mutate_distances(prev_velocity, particle_best_distance, global_best_distance):
    R1 = np.random.rand()
    R2 = np.random.rand()
    R3 = np.random.rand()

    v = C1 * R1 * prev_velocity + C2 * R2 * particle_best_distance + C3 * R3 * global_best_distance
    new_velocity = np.array(list(map(lambda x: np.round(x / (C1 * R1 + C2 * R2 + C3 * R3)), v)))

    return new_velocity


def main(argv):
    global C1, C2, C3
    parser = init_parser()
    (options, args) = parser.parse_args()
    with open(options.cfg) as cfg_file:
        cfg = json.load(cfg_file)
    C1, C2, C3 = (cfg["c1"], cfg["c2"], cfg["c3"])
    print(cfg)

    if options.seed is not None and options.seed.isnumeric() :
        np.random.seed(int(options.seed))    # does not work xD
    b = Board((cfg["size"], cfg["size"]), coin_percentage=cfg["coin_density"], board=options.i)
    paths = np.random.randint(0, 4, (cfg["paths"], cfg["maxlen"]))
    bests_for_particles = paths.copy()
    bests_for_particles_coins = np.array([b.get_coins_number(x) for x in paths])
    global_best = bests_for_particles[np.argmax(bests_for_particles_coins)]
    global_best_coins = np.max(bests_for_particles_coins)
    print("Before:", ["↑→↓←"[x] for x in global_best], ", Coins: ", global_best_coins)
    velocities = np.zeros(paths.shape)
    for i in range(cfg["iters"]):
        iteration_global_coins = 0
        iteration_best_index = 0
        for j in range(paths.shape[0]):
            particle_best_distance = get_distance(bests_for_particles[j], paths[j])
            global_best_distance = get_distance(global_best, paths[j])
            velocities[j] = mutate_distances(
                velocities[j],
                particle_best_distance,
                global_best_distance,
            )
            paths[j] = np.array(list(map(lambda x: x % 4, paths[j] + velocities[j])))
            new_path_coins = b.get_coins_number(paths[j])

            if new_path_coins > bests_for_particles_coins[j]:
                bests_for_particles[j] = paths[j].copy()
                bests_for_particles_coins[j] = new_path_coins

            if new_path_coins > iteration_global_coins:
                iteration_global_coins = new_path_coins
                iteration_best_index = j

        if iteration_global_coins > global_best_coins:
            global_best_coins = iteration_global_coins
            global_best = paths[iteration_best_index].copy()

    visualized = np.array([[1 if b.board[i][j] else 0 for j in range(np.shape(b.board)[1])] for i in range(np.shape(b.board)[0])])
    if options.o is not None:
        with open(options.o, "wb") as out_file:
            np.save(out_file, visualized)
    else:
        print(visualized)
    print("After :", ["↑→↓←"[x] for x in global_best], ", Coins: ", global_best_coins)


if __name__ == "__main__":
   main(sys.argv[1:])