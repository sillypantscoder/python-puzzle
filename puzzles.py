import pygame
class Puzzle:
	def __init__(self): pass
	def getFrame(self, width, height): pass
	def handleclick(self, x, y): pass






class Level1:
	def __init__(self):
		self.grid = [[0 for x in range(10)] for y in range(10)]
		self.lastsize = [0, 0]
	def getFrame(self, width, height):
		# Return a pygame surface
		r = pygame.Surface((width, height))
		r.fill((255, 255, 255))
		cellsize = [width / 10, height / 10]
		for x in range(10):
			for y in range(10):
				cellrect = pygame.Rect(x * cellsize[0], y * cellsize[1], cellsize[0], cellsize[1])
				c = (0, 0, 0) if self.grid[x][y] else (255, 255, 255)
				pygame.draw.rect(r, c, cellrect)
		self.lastsize = [width, height]
		return r
	def handleclick(self, x, y):
		percent = [x / self.lastsize[0], y / self.lastsize[1]]
		gridx = int(percent[0] * 10)
		gridy = int(percent[1] * 10)
		self.grid[gridx][gridy] = 1 if self.grid[gridx][gridy] == 0 else 0