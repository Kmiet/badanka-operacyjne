import json
import random
import numpy as np

WIDTH = 15
HEIGHT = 15

kPoints = []
chosen = []
walls = []

def addWall1(p):
  x, y, k = p
  if x > 0 and not chosen[x - 1][y]:
    kPoints.append([x, y, 3])

  if x < WIDTH - 1 and not chosen[x + 1][y]:
    kPoints.append([x, y, 1])

  if y > 0 and not chosen[x][y - 1]:
    kPoints.append([x, y, 0])

  if y < HEIGHT - 1 and not chosen[x][y + 1]:
    kPoints.append([x, y, 2])


def addWall2(p, m):
  count = 0
  x, y, k = p

  for i in range(4):
    if not walls[x][y][i]:
      count += 1

  if count < m:
    addWall1(p)


def movePointK(p):
  x, y, k = p

  if k == 0:
    return [x, y - 1, k]
  elif k == 1:
    return [x + 1, y, k]
  elif k == 2:
    return [x, y + 1, k]
  elif k == 3:
    return [x - 1, y, k]


def updateWalls(p):
  global kPoints
  x, y, k = p
  kPoints = []

  walls[x][y][k] = False
  
  p = movePointK(p)
  x, y, k = p

  walls[x][y][(k + 2) % 4] = False
  chosen[x][y] = True
  addWall1(p)

def seek(m = 2):
  if m >= 4:
    return False

  xp = random.randint(0, WIDTH - 1)
  yp = random.randint(0, HEIGHT - 1)

  x = xp
  y = yp

  if not chosen[x][y]:
    if x > 0 and chosen[x - 1][y]:
      addWall2([x - 1, y, 1], m)
    
    if y > 0 and chosen[x][y -1]:
      addWall2([x, y - 1, 2], m)

    if not len(kPoints) == 0:
      return True

    if x < WIDTH - 1 and chosen[x + 1][y]:
      addWall2([x + 1, y, 3], m)

    if y < HEIGHT - 1 and chosen[x][y + 1]:
      addWall2([x, y + 1, 0], m)

    if not len(kPoints) == 0:
      return True

  x += 1
  if x == WIDTH:
    x = 0
    y += 1
    if y == HEIGHT:
      y = 0
  
  while not x == xp or not y == yp:
    if not chosen[x][y]:
      if x > 0 and chosen[x - 1][y]:
        addWall2([x - 1, y, 1], m)
    
      if y > 0 and chosen[x][y -1]:
        addWall2([x, y - 1, 2], m)

      if not len(kPoints) == 0:
        return True

      if x < WIDTH - 1 and chosen[x + 1][y]:
        addWall2([x + 1, y, 3], m)

      if y < HEIGHT - 1 and chosen[x][y + 1]:
        addWall2([x, y + 1, 0], m)

      if not len(kPoints) == 0:
        return True

    x += 1
    if x == WIDTH:
      x = 0
      y += 1
      if y == HEIGHT:
        y = 0

  return seek(m + 1)


def genNewLab(w, h):
  global chosen, walls
  chosen = np.full((w, h), False)
  walls = np.full((w, h, 4), True)

  chosen[0][0] = True
  
  while seek():
    op = random.randint(0, len(kPoints) - 1)
    updateWalls(kPoints[op])

  return walls


def parse2lab(lab):
  a = ""
  for y in range(HEIGHT):
    for x in range(WIDTH):
      if lab[x, y, 0]:
        a += "##"
      else:
        a += "# "
    a += "#@"
    for x in range(WIDTH):
      if lab[x, y, 3]:
        a += "# "
      else:
        a += "  "
    a += "#@"
  for x in range(WIDTH):
    if lab[x, HEIGHT - 1, 2]:
      a += "##"
    else:
      a += " #"
  a += "#@"

  i = 0
  j = 0
  row = []
  labirynth = []
  w = 0

  for c in a:
    if c == "#":
      row.append(1)
      i += 1
    elif c == " ":
      row.append(0)
      i += 1
    elif c == "@":
      labirynth.append(row)
      row = []
      j += 1
      w = i
      i = 0

  return labirynth, w, j

class Lab:
  def __init__(self, w, h):
    lab = genNewLab(w, h)
    labirynth, width, height = parse2lab(lab)
    self.map = labirynth
    self.width = width
    self.height = height
  
  def save2file(self, filePath):
    with open(filePath, "w+") as file:
      file.write(json.dumps({
        "width": self.width,
        "height": self.height, 
        "map": self.map
      }))
      file.close()


def main():
  lab = Lab(WIDTH, HEIGHT)
  lab.save2file('data/lab1.json')

if __name__ == "__main__":
  main()