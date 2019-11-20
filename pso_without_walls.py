import numpy as np

class Board:

  def __init__(self, shape, coin_percentage=0.4):
    self.shape = shape
    self.board = (np.random.rand(*board_shape) > (1.0 - coin_percentage))
    self.start = np.array(list(map(lambda x: int((x-1)/2), board_shape)))
    self.move_mapping = [np.array([-1, 0]), np.array([0, 1]), np.array([1, 0]), np.array([0, -1])]

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

def get_distance(path_1, path_2):
  return np.array(list(map(lambda x: x if x >= 0 else 4 + x, (path_1 - path_2))))

def mutate_distances(prev_velocity, particle_best_distance, global_best_distance, mutation_factor):
  # dla dużego mutation factor rób większe kroki w strone minimum globalnego
  # TODO: new_velocity = 
  return new_velocity

# b.get_coins_number(paths[0])
b = Board((9, 9))
paths = np.random.randint(0, 4, (4, 5))
bests_for_particles = paths.copy()
bests_for_particles_coins = list(map(lambda x: b.get_coins_number(x), paths))
global_best = bests_for_particles[np.argmax(bests_for_particles_coins)]
global_best_coins = np.max(bests_for_particles_coins)
velocities = np.zeros(paths.shape)
for i in range(100):
  for j in range(paths.shape[0]):
    particle_best_distance = get_distance(bests_for_particles[j], paths[j])
    global_best_distance = get_distance(global_best, paths[j])
    velocities[j] = mutate_distances(
      velocities[j], 
      particle_best_distance, 
      global_best_distance,
    )
    paths[j] = paths[j] + velocities[j]
    # TODO: aktualizacja bestów