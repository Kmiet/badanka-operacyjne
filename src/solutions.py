import json
import random

WALL = 1
max_w = 50
max_h = 50

def is_valid(pos, graph):
  x, y = pos
  return 0 <= x and x < max_h and 0 <= y and y < max_w and graph[x][y] != WALL


def dfs(initPos, graph, visited, depth):
  if depth == 1:
    return [initPos]
  x, y = initPos
  for (dx, dy) in [(0,-1), (0,1), (-1,0), (1,0)]:
    x1 = x + dx
    y1 = y + dy
    if is_valid((x1, y1), graph) and not visited[x1][y1]:
      visited[x1][y1] = True
      return [initPos] + dfs((x1, y1), graph, visited, depth-1)


class Lab:
  def __init__(self, w, h, m):
    self.map = m
    self.width = w
    self.height = h
    max_w = w
    max_h = h


  def genSolutions(self):
    for i in range(5):
      i_x = random.randint(0, self.height)
      i_y = random.randint(0, self.width)
      visited = [[False for i in range(self.height)] for j in range(self.width)]
      print(dfs((i_x, i_y), self.map, visited, 10))


  def save2file(self, filePath):
    with open(filePath, "w") as file:
      file.write(json.dumps({
        "width": self.width,
        "height": self.height, 
        "map": self.map
      }))
      file.close()


def parse2lab(filePath):
  with open(filePath) as file:
    data = json.load(file)
    file.close()
    return Lab(data['width'], data['height'], data['map'])


def main():
  fp = 'data/lab1.json'
  lab = parse2lab(fp)
  lab.genSolutions()
  # lab.save2file(fp)

if __name__ == "__main__":
  main()