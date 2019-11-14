import json
import random

COIN_CHANCE = 0.2

COIN = 2
WALL = 1

class Lab:
  def __init__(self, w, h, m):
    self.map = m
    self.width = w
    self.height = h

  def addCoins(self):
    for i in range(1, self.height - 1):
      for j in range(1, self.width - 1):
        if self.map[i][j] is not WALL and random.uniform(0, 1) < COIN_CHANCE:
          self.map[i][j] = COIN



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
  lab.addCoins()
  lab.save2file(fp)

if __name__ == "__main__":
  main()