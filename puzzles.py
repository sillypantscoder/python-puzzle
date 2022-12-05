from puzzle_base import *

class Level1(Puzzle):
	def __init__(self):
		self.gridsize = 10
		self.grid = [[0 for x in range(self.gridsize)] for y in range(self.gridsize)]
		self.lastsize = [0, 0]
		self.timer = 100
	def getFrame(self, width, height, getkey):
		# Return a pygame surface
		r = pygame.Surface((width, height))
		r.fill((255, 255, 255))
		s = pygame.font.SysFont(pygame.font.get_default_font(), (width + height) // 10).render("1", True, (0, 0, 0))
		r.blit(s, ((r.get_width() / 2) - (s.get_width() / 2), (r.get_height() / 2) - (s.get_height() / 2)))
		cellsize = [width / self.gridsize, height / self.gridsize]
		for x in range(self.gridsize):
			for y in range(self.gridsize):
				cellrect = pygame.Rect(x * cellsize[0], y * cellsize[1], cellsize[0], cellsize[1])
				if self.grid[x][y]:
					pygame.draw.rect(r, (0, 0, 0), cellrect)
					pygame.draw.rect(r, (0, 0, 0), cellrect, 5)
		self.lastsize = [width, height]
		return r
	def onmouseup(self, x, y):
		percent = [x / self.lastsize[0], y / self.lastsize[1]]
		gridx = int(percent[0] * self.gridsize)
		gridy = int(percent[1] * self.gridsize)
		for cx in range(gridx - 1, gridx + 2):
			for cy in range(gridy - 1, gridy + 2):
				if cx >= 0 and cy >= 0 and cx < self.gridsize and cy < self.gridsize:
					self.grid[cx][cy] = 1
	def getNew(self):
		for x in range(len(self.grid)):
			for y in range(len(self.grid[x])):
				if self.grid[x][y] == 0:
					return self
		self.timer -= 1
		if self.timer <= 0:
			return Level2()
		else:
			return self

class Level2(Puzzle):
	def __init__(self):
		self.gridsize = 5
		self.grid = [[0 for x in range(self.gridsize)] for y in range(self.gridsize)]
		self.lastsize = [0, 0]
		self.timer = 100
		self.timer2 = 50
	def getFrame(self, width, height, getkey):
		# Return a pygame surface
		r = pygame.Surface((width, height))
		r.fill((255, 255, 255))
		s = pygame.font.SysFont(pygame.font.get_default_font(), (width + height) // 10).render("2", True, (0, 0, 0))
		r.blit(s, ((r.get_width() / 2) - (s.get_width() / 2), (r.get_height() / 2) - (s.get_height() / 2)))
		cellsize = [width / self.gridsize, height / self.gridsize]
		for x in range(self.gridsize):
			for y in range(self.gridsize):
				cellrect = pygame.Rect(x * cellsize[0], y * cellsize[1], cellsize[0], cellsize[1])
				if self.grid[x][y]:
					pygame.draw.rect(r, (0, 0, 0), cellrect)
					pygame.draw.rect(r, (0, 0, 0), cellrect, 5)
					w = int((self.timer / 100) * 5)
					if w > 0:
						pygame.draw.rect(r, (255, 255, 255), cellrect, w)
		self.lastsize = [width, height]
		return r
	def onmouseup(self, x, y):
		percent = [x / self.lastsize[0], y / self.lastsize[1]]
		gridx = int(percent[0] * self.gridsize)
		gridy = int(percent[1] * self.gridsize)
		newcells = []
		for cx in range(gridx - 1, gridx + 2):
			for cy in range(gridy - 1, gridy + 2):
				if cx >= 0 and cy >= 0 and cx < self.gridsize and cy < self.gridsize:
					if cx == 0 or cy == 0 or (self.grid[cx - 1][cy] == 1 and self.grid[cx][cy - 1] == 1 and self.grid[cx - 1][cy - 1] == 1):
						newcells.append((cx, cy))
		for c in newcells:
			self.grid[c[0]][c[1]] = 1
	def getNew(self):
		for x in range(len(self.grid)):
			for y in range(len(self.grid[x])):
				if self.grid[x][y] == 0:
					return self
		self.timer -= 1
		if self.timer <= 0:
			self.timer2 -= 1
			if self.timer2 <= 0:
				return Level3()
			else:
				return self
		else:
			return self

class Level3(PlatformerPuzzle):
	def __init__(self):
		super().__init__();
		self.level = ["==========", "", "  =#", "   = ^   +", "=========="]
		self.levelno = 3
		self.next = Level4

class Level4(Puzzle):
	def __init__(self):
		self.pos = [0, 0]
		self.dragpos = None
		self.completed = False
	def getFrame(self, width, height, getkey):
		s = pygame.Surface((width, height))
		s.fill((0, 0, 0))
		pygame.draw.rect(s, (255, 255, 255), pygame.Rect(0, 0, width, height).move(self.pos))
		# Text
		t = pygame.font.SysFont(pygame.font.get_default_font(), (width + height) // 10).render("4", True, (0, 0, 0))
		s.blit(t, (((s.get_width() / 2) - (t.get_width() / 2)) + self.pos[0], ((s.get_height() / 2) - (t.get_height() / 2)) + self.pos[1]))
		# Completion
		r = pygame.Rect(0, 0, width, height)
		if r.colliderect(r.move(self.pos)):
			self.completed = False
		else:
			if self.dragpos:
				self.completed = False
			else:
				self.completed = True
		return s
	def onmousedown(self, x, y):
		self.dragpos = [x, y]
	def onmousemove(self, x, y, clicking):
		if clicking and self.dragpos:
			self.pos[0] -= self.dragpos[0] - x
			self.pos[1] -= self.dragpos[1] - y
			self.dragpos = [x, y]
	def onmouseup(self, x, y):
		self.dragpos = None
	def getNew(self):
		if self.completed:
			return Level5()
		else:
			return self

class Level5(PlatformerPuzzle):
	def __init__(self):
		super().__init__();
		self.level = [" =========", "  #  =   =", "====   ^", "^    ^ ^ =", "========", "       ^ ===", "", "", "        +"]
		self.levelno = 5
		self.next = Level6

class Level6(Puzzle):
	def __init__(self):
		self.gridsize = 7
		self.grid = [[0 for x in range(self.gridsize)] for y in range(self.gridsize)]
		self.lastsize = [0, 0]
		self.timer = 100
	def getFrame(self, width, height, getkey):
		# Return a pygame surface
		r = pygame.Surface((width, height))
		r.fill((255, 255, 255))
		s = pygame.font.SysFont(pygame.font.get_default_font(), (width + height) // 10).render("6", True, (0, 0, 0))
		r.blit(s, ((r.get_width() / 2) - (s.get_width() / 2), (r.get_height() / 2) - (s.get_height() / 2)))
		cellsize = [width / self.gridsize, height / self.gridsize]
		for x in range(self.gridsize):
			for y in range(self.gridsize):
				cellrect = pygame.Rect(x * cellsize[0], y * cellsize[1], cellsize[0], cellsize[1])
				if self.grid[x][y]:
					pygame.draw.rect(r, (0, 0, 0), cellrect)
				pygame.draw.rect(r, (0, 0, 0), cellrect, 5)
		self.lastsize = [width, height]
		return r
	def onmouseup(self, x, y):
		percent = [x / self.lastsize[0], y / self.lastsize[1]]
		gridx = int(percent[0] * self.gridsize)
		gridy = int(percent[1] * self.gridsize)
		newcells = []
		if gridx >= 0 and gridy >= 0 and gridx < self.gridsize and gridy < self.gridsize:
			noitems = sum([sum(self.grid[x]) for x in range(len(self.grid))]) == 0
			if noitems:
				newcells.append((gridx, gridy))
			othercells = [
				# Knight jump
				(gridx - 2, gridy - 1), (gridx - 2, gridy + 1),
				(gridx + 2, gridy - 1), (gridx + 2, gridy + 1),
				(gridx - 1, gridy - 2), (gridx - 1, gridy + 2),
				(gridx + 1, gridy - 2), (gridx + 1, gridy + 2)
			]
			othercells = [p for p in othercells if p[0] >= 0 and p[1] >= 0 and p[0] < self.gridsize and p[1] < self.gridsize]
			othercells = [self.grid[p[0]][p[1]] for p in othercells]
			if 1 in othercells:
				newcells.append((gridx, gridy))
		for c in newcells:
			self.grid[c[0]][c[1]] = 1
	def getNew(self):
		for x in range(len(self.grid)):
			for y in range(len(self.grid[x])):
				if self.grid[x][y] == 0:
					return self
		self.timer -= 1
		if self.timer <= 0:
			return Level7()
		else:
			return self

class Level7(Puzzle):
	def __init__(self):
		f = open("stuff.txt", "w")
		f.write("Please delete all of this text!")
		f.close()
		self.timer = 50
	def getFrame(self, width, height, getkey):
		texts = ["Look at the file:", "stuff.txt"]
		font = pygame.font.SysFont(pygame.font.get_default_font(), (width + height) // 10)
		texts = [font.render(t, True, (0, 0, 0)) for t in texts]
		r = pygame.Surface((width, height))
		r.fill((255, 255, 255))
		cum_y = 0
		for t in texts:
			r.blit(t, ((r.get_width() / 2) - (t.get_width() / 2), cum_y))
			cum_y += t.get_height()
		return r
	def getNew(self):
		import os
		if os.path.exists("stuff.txt"):
			f = open("stuff.txt", "r")
			t = f.read()
			f.close()
			if t == "":
				self.timer -= 1
				if self.timer <= 0:
					os.remove("stuff.txt")
					return Puzzle()
				else:
					return self
			else:
				return self
		else:
			f = open("stuff.txt", "w")
			f.write("Please delete all of this text!\n(But don't delete the file itself)")
			f.close()
			return self