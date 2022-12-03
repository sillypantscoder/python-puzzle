import pygame
pygame.font.init()
class Puzzle:
	def __init__(self): pass
	def getFrame(self, width, height, getkey):
		s = pygame.Surface((width, height))
		s.fill((255, 255, 255))
		return s
	def onmousemove(self, x, y, clicking): pass
	def onmousedown(self, x, y): pass
	def onmouseup(self, x, y): pass
	def getNew(self): return self

class PlatformerPuzzle(Puzzle):
	def __init__(self):
		self.level = ["", "  =#", "   = ^   +", "=========="]
		self.playersize = 5
		self.pos = [0, 0]
		self.v = [0, 0]
		self.levelno = -1
		self.completed = False
		self.next = Puzzle
	def getpercent(self, width, height):
		return (width + height) / 200
	def getFrame(self, width, height, getkey):
		s = pygame.Surface((width, height))
		s.fill((255, 255, 255))
		playerrect = pygame.Rect(*self.pos, self.playersize, self.playersize)
		# draw level
		cellsize = self.getpercent(width, height) * self.playersize * 2
		font = pygame.font.SysFont(pygame.font.get_default_font(), int(self.getpercent(width, height) * 10))
		for y in range(len(self.level)):
			for x in range(len(self.level[y])):
				cellrect = pygame.Rect(x * cellsize, y * cellsize, cellsize, cellsize)
				# Drawing
				if self.level[y][x] == "=":
					pygame.draw.rect(s, (0, 0, 0), cellrect)
				if self.level[y][x] == "#":
					pygame.draw.rect(s, (0, 0, 0), cellrect)
					n = font.render(str(self.levelno), True, (255, 255, 255))
					s.blit(n, (cellrect.centerx - (n.get_width() / 2), cellrect.centery - (n.get_height() / 2)))
				if self.level[y][x] == "^":
					pygame.draw.rect(s, (255, 0, 0), cellrect)
					if playerrect.colliderect(cellrect):
						self.pos = [0, 0]
						self.v = [0, 0]
				if self.level[y][x] == "+":
					pygame.draw.ellipse(s, (200, 200, 255), cellrect)
					padding = cellrect.width // 4
					pygame.draw.ellipse(s, (100, 100, 255), pygame.Rect(cellrect.left + padding, cellrect.top + padding, cellrect.width - (padding * 2), cellrect.height - (padding * 2)))
					if playerrect.colliderect(cellrect):
						self.completed = True
				# Collision
				if self.level[y][x] in "=#":
					if playerrect.colliderect(cellrect):
						if playerrect.top < cellrect.top:
							while playerrect.colliderect(cellrect):
								self.pos[1] -= 0.1
								playerrect = pygame.Rect(*self.pos, self.playersize, self.playersize)
						else:
							while playerrect.colliderect(cellrect):
								self.pos[1] += 0.1
								playerrect = pygame.Rect(*self.pos, self.playersize, self.playersize)
						self.v[1] = 0
						if getkey(pygame.K_w):
							self.v[1] -= 4
		# draw player
		pygame.draw.rect(s, (0, 0, 0), playerrect)
		self.v[1] += 0.05
		self.pos[0] += self.v[0]
		self.pos[1] += self.v[1]
		self.v[0] *= 0.8
		if self.pos[1] > len(self.level) * cellsize:
			self.pos = [0, 0]
			self.v = [0, 0]
		# arrow keys
		if getkey(pygame.K_a):
			self.v[0] -= 0.3
		if getkey(pygame.K_d):
			self.v[0] += 0.3
		return s
	def getNew(self):
		if self.completed:
			return self.next()
		else:
			return self





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