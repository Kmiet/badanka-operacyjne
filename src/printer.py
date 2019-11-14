import json

COIN = 2
WALL = 1

COIN_SYMBOL = "$"
WALL_SYMBOL = "#"

class Lab:
  def __init__(self, w, h, m):
    self.map = m
    self.width = w
    self.height = h

  def __str__(self):
    lab_str = ""
    for i in range(self.height):
      for j in range(self.width):
        if self.map[i][j] == COIN:
          lab_str += COIN_SYMBOL
        elif self.map[i][j] == WALL:
          lab_str += WALL_SYMBOL
        else:
          lab_str += " "
      lab_str += "\n"
    return lab_str

def parse2lab(filePath):
  with open(filePath) as file:
    data = json.load(file)
    file.close()
    return Lab(data['width'], data['height'], data['map'])

def main():
  fp = 'data/lab1.json'
  lab = parse2lab(fp)
  print(lab)

if __name__ == "__main__":
  main()