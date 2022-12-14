import pygame
pygame.font.init()
class Puzzle:
	def __init__(self):
		self.hints = []
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
						if getkey("w"):
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
		if getkey("a"):
			self.v[0] -= 0.3 * (self.getpercent(width, height) // 5.6)
		if getkey("d"):
			self.v[0] += 0.3 * (self.getpercent(width, height) // 5.6)
		return s
	def getNew(self):
		if self.completed:
			return self.next()
		else:
			return self

class FlowFreePuzzle(Puzzle):
	def __init__(self):
		self.gridsize = 5
		self.flows = [
			{"start": [0, 0], "end": [2, 2], "color": (255,   0,   0), "path": []},
			{"start": [4, 0], "end": [2, 3], "color": (  0, 255,   0), "path": []},
			{"start": [4, 1], "end": [0, 4], "color": (255, 255,   0), "path": []},
			{"start": [0, 1], "end": [0, 3], "color": (255, 100,   0), "path": []},
			{"start": [1, 1], "end": [1, 3], "color": (255,   0, 255), "path": []}
		]
		self.flowdrag = None
		self.lastsize = [500, 500]
		self.timer = 100
	def getFrame(self, width, height, getkey):
		self.lastsize = [width, height]
		r = pygame.Surface((width, height))
		r.fill((0, 0, 0))
		# Draw grid
		cellsize = [width // self.gridsize, height // self.gridsize]
		for x in range(self.gridsize):
			for y in range(self.gridsize):
				cellrect = pygame.Rect(x * cellsize[0], y * cellsize[1], cellsize[0], cellsize[1])
				pygame.draw.rect(r, (255, 255, 255), cellrect, 1)
		# Draw flows
		for f in self.flows:
			pygame.draw.circle(r, f["color"], (
				# Position
				round((f["start"][0] + 0.5) * cellsize[0]),
				round((f["start"][1] + 0.5) * cellsize[1])
			), round(min(cellsize[0] / 2, cellsize[1] / 2) * 0.9))
			pygame.draw.circle(r, f["color"], (
				# Position
				round((f["end"][0] + 0.5) * cellsize[0]),
				round((f["end"][1] + 0.5) * cellsize[1])
			), round(min(cellsize[0] / 2, cellsize[1] / 2) * 0.9))
			# Draw path
			if len(f["path"]) > 0:
				paths = [f["start"], *f["path"]]
				for p in range(1, len(paths)):
					pygame.draw.line(r, f["color"],
						(round((paths[p - 1][0] + 0.5) * cellsize[0]), round((paths[p - 1][1] + 0.5) * cellsize[1])),
						(round((paths[p    ][0] + 0.5) * cellsize[0]), round((paths[p    ][1] + 0.5) * cellsize[1])),
					round(min(cellsize[0] / 2, cellsize[1] / 2) * 0.9))
					pygame.draw.circle(r, f["color"], (
						# Position
						round((paths[p    ][0] + 0.5) * cellsize[0]),
						round((paths[p    ][1] + 0.5) * cellsize[1])
					), round(min(cellsize[0] / 2, cellsize[1] / 2) * 0.45))
		return r
	def onmousedown(self, x, y):
		# 1. Figure out what cell they clicked on
		cellsize = [self.lastsize[0] // self.gridsize, self.lastsize[1] // self.gridsize]
		currentcell = None
		for cx in range(self.gridsize):
			for cy in range(self.gridsize):
				cellrect = pygame.Rect(cx * cellsize[0], cy * cellsize[1], cellsize[0], cellsize[1])
				if cellrect.collidepoint(x, y):
					currentcell = [cx, cy]
		if not currentcell: return
		# 2. Figure out if they clicked on a flow
		cflow = None
		for f in range(len(self.flows)):
			if self.flows[f]["start"] == currentcell:
				cflow = f + 0
				self.flows[f]["path"] = []
			elif self.flows[f]["end"] == currentcell:
				# reverse start & end
				revend = self.flows[f]["end"]
				self.flows[f]["end"] = self.flows[f]["start"]
				self.flows[f]["start"] = revend
				# continue normally
				cflow = f + 0
				self.flows[f]["path"] = []
		self.flowdrag = cflow
	def onmousemove(self, x, y, clicking):
		if clicking and self.flowdrag != None:
			# 1. Figure out what cell they are on
			cellsize = [self.lastsize[0] // self.gridsize, self.lastsize[1] // self.gridsize]
			currentcell = None
			for cx in range(self.gridsize):
				for cy in range(self.gridsize):
					cellrect = pygame.Rect(cx * cellsize[0], cy * cellsize[1], cellsize[0], cellsize[1])
					if cellrect.collidepoint(x, y):
						currentcell = [cx, cy]
			if currentcell:
				# 2. Figure out if we're already on a path
				for of in self.flows:
					if of["start"] == currentcell or of["end"] == currentcell:
						# Uh oh!
						if of != self.flows[self.flowdrag]:
							return
					for p in range(len(of["path"])):
						if of["path"][p] == currentcell:
							# Uh oh!
							of["path"] = of["path"][:p]
							break
				# 2. Figure out if we're next to the last path
				n = lambda ax, ay, bx, by: abs(ax - bx) + abs(ay - by)
				if n(*currentcell, *self.flows[self.flowdrag]["start"]) == 1:
					self.flows[self.flowdrag]["path"].append(currentcell)
				elif len(self.flows[self.flowdrag]["path"]) == 0:
					# Don't do anything because we don't want to break the below statement
					pass
				elif n(*currentcell, *self.flows[self.flowdrag]["path"][-1]) == 1:
					self.flows[self.flowdrag]["path"].append(currentcell)
	def onmouseup(self, x, y):
		self.flowdrag = None
	def getNew(self):
		# 1. Make sure that all the flows are completed
		for f in self.flows:
			if len(f["path"]) > 0:
				if f["path"][-1] != f["end"]:
					return self
			else:
				return self
		# 2. Make sure that every cell is filled
		grid = [[False for y in range(self.gridsize)] for x in range(self.gridsize)]
		for f in self.flows:
			grid[f["start"][0]][f["start"][1]] = True
			for p in f["path"]:
				grid[p[0]][p[1]] = True
			grid[f["end"][0]][f["end"][1]] = True
		for x in range(self.gridsize):
			for y in range(self.gridsize):
				if not grid[x][y]:
					return self
		# Done!
		self.timer -= 1
		if self.timer <= 0:
			return Puzzle()
		else:
			return self