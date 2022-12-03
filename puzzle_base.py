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
		playerrect = pygame.Rect(*self.pos, self.playersize * (self.getpercent(width, height) // 5.6), self.playersize * (self.getpercent(width, height) // 5.6))
		# draw level
		cellsize = self.getpercent(width, height) * self.playersize * 2
		font = pygame.font.SysFont(pygame.font.get_default_font(), int(self.getpercent(width, height) * 10))
		extra = 3
		for y in range(len(self.level)):
			for x in range(len(self.level[y])):
				cellrect = pygame.Rect((x * cellsize) - extra, (y * cellsize) - extra, cellsize + extra + extra, cellsize + extra + extra)
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
								playerrect = pygame.Rect(*self.pos, self.playersize * (self.getpercent(width, height) // 5.6), self.playersize * (self.getpercent(width, height) // 5.6))
						else:
							while playerrect.colliderect(cellrect):
								self.pos[1] += 0.1
								playerrect = pygame.Rect(*self.pos, self.playersize * (self.getpercent(width, height) // 5.6), self.playersize * (self.getpercent(width, height) // 5.6))
						self.v[1] = 0
						if getkey(pygame.K_w):
							self.v[1] -= 4 * (self.getpercent(width, height) // 5.6)
		# draw player
		pygame.draw.rect(s, (0, 0, 0), playerrect)
		self.v[1] += 0.05 * (self.getpercent(width, height) // 5.6)
		self.pos[0] += self.v[0]
		self.pos[1] += self.v[1]
		self.v[0] *= 0.8
		if self.pos[1] > len(self.level) * cellsize:
			self.pos = [0, 0]
			self.v = [0, 0]
		# arrow keys
		if getkey(pygame.K_a):
			self.v[0] -= 0.3 * (self.getpercent(width, height) // 5.6)
		if getkey(pygame.K_d):
			self.v[0] += 0.3 * (self.getpercent(width, height) // 5.6)
		return s
	def getNew(self):
		if self.completed:
			return self.next()
		else:
			return self