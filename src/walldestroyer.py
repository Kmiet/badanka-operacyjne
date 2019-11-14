import json

WALL = 1

class Lab:
  def __init__(self, w, h, m):
    self.map = m
    self.width = w
    self.height = h

  def removeDeadEnds(self):
    for i in range(1, self.height - 1):
      for j in range(1, self.width - 1):
        if not self.map[i][j] is WALL:
          wall_count = 0
          if self.map[i-1][j] is WALL:
            wall_count += 1
          if self.map[i+1][j] is WALL:
            wall_count += 1
          if self.map[i][j-1] is WALL:
            wall_count += 1
          if self.map[i][j+1] is WALL:
            wall_count += 1

          if wall_count > 2:
            changed = False
            if not changed and self.map[i-1][j] is WALL:
              space_count = 0
              if i - 2 >= 0 and self.map[i-2][j] is not WALL:
                space_count += 1
              if self.map[i][j] is not WALL:
                space_count += 1
              if self.map[i-1][j-1] is not WALL:
                space_count += 1
              if self.map[i-1][j+1] is not WALL:
                space_count += 1

              if space_count > 1:
                changed = True
                self.map[i-1][j] = 0

            if not changed and self.map[i+1][j] is WALL:
              space_count = 0
              if self.map[i][j] is not WALL:
                space_count += 1
              if i + 2 < self.height and self.map[i+2][j] is not WALL:
                space_count += 1
              if self.map[i+1][j-1] is not WALL:
                space_count += 1
              if self.map[i+1][j+1] is not WALL:
                space_count += 1

              if space_count > 1:
                changed = True
                self.map[i+1][j] = 0

            if not changed and self.map[i][j-1] is WALL:
              space_count = 0
              if self.map[i-1][j-1] is not WALL:
                space_count += 1
              if self.map[i+1][j-1] is not WALL:
                space_count += 1
              if j - 2 >= 0 and self.map[i][j-2] is not WALL:
                space_count += 1
              if self.map[i][j] is not WALL:
                space_count += 1

              if space_count > 1:
                changed = True
                self.map[i][j-1] = 0

            if not changed and self.map[i][j+1] is WALL:
              space_count = 0
              if self.map[i-1][j+1] is not WALL:
                space_count += 1
              if self.map[i+1][j+1] is not WALL:
                space_count += 1
              if self.map[i][j] is not WALL:
                space_count += 1
              if j + 2 < self.width and self.map[i][j+2] is not WALL:
                space_count += 1

              if space_count > 1:
                changed = True
                self.map[i][j+1] = 0

            if not changed:
              raise Error('Cant fix')




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
  lab.removeDeadEnds()
  lab.save2file(fp)

if __name__ == "__main__":
  main()