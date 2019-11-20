import numpy as np

C1 = 1 # stala dla poprzedniej predkosci
C2 = 0.8 # stala dla lokalnego rozwiazania
C3 = 1 # stala dla globalnego rozwiazania

class Board:

  def __init__(self, shape, coin_percentage=0.4):
    self.shape = shape
    self.board = (np.random.rand(*shape) > (1.0 - coin_percentage))
    self.start = np.array(list(map(lambda x: int((x-1)/2), shape)))
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

def mutate_distances(prev_velocity, particle_best_distance, global_best_distance):
  # dla duzego mutation factor rob wieksze kroki w strone minimum globalnego
  # TODO: new_velocity = 

  R1 = np.random.rand()
  R2 = np.random.rand()
  R3 = np.random.rand()

  # =< 3 * x * y

  # [6.23, 8.71, 7.93, 4.41, 2.67] -> [6, 8, 8, 4, 3]

  v = C1 * R1 * prev_velocity + C2 * R2 * particle_best_distance + C3 * R3 * global_best_distance
  new_velocity = map(lambda x : np.round(x / (C1 * R1 + C2 * R2 + C3 * R3)), v)

  return new_velocity

# b.get_coins_number(paths[0])
np.random.seed(19686900)
b = Board((11, 11))
paths = np.random.randint(0, 4, (8, 7))
bests_for_particles = paths.copy()
bests_for_particles_coins = list(map(lambda x: b.get_coins_number(x), paths))
global_best = bests_for_particles[np.argmax(bests_for_particles_coins)]
global_best_coins = np.max(bests_for_particles_coins)
velocities = np.zeros(paths.shape)
for i in range(400):
  iteration_global_coins=0
  iteration_best_index=0
  for j in range(paths.shape[0]):
    particle_best_distance = get_distance(bests_for_particles[j], paths[j])
    global_best_distance = get_distance(global_best, paths[j])
    velocities[j] = mutate_distances(
      velocities[j], 
      particle_best_distance, 
      global_best_distance,
    )
    paths[j] = map(lambda x : x % 4, paths[j] + velocities[j])
    new_path_coins = b.get_coins_number(paths[j])

    if new_path_coins > bests_for_particles_coins[j]:
      bests_for_particles[j] = paths[j].copy()
      bests_for_particles_coins[j] = new_path_coins
    
    if new_path_coins > iteration_global_coins:
      iteration_global_coins = new_path_coins
      iteration_best_index = j

  if iteration_global_coins > global_best_coins:
    global_best_coins = iteration_global_coins
    global_best = paths[j].copy()

print(np.array([[1 if b.board[i][j] else 0 for i in range(np.shape(b.board)[0])] for j in range(np.shape(b.board)[1])]))
print(global_best, global_best_coins)