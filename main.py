"""
A puzzle game written with Python.
"""

import pygame
import puzzles

SCREENSIZE = [640, 480]
screen = pygame.display.set_mode(SCREENSIZE, pygame.RESIZABLE)

currentpuzzle = puzzles.Level1()
def getkey(k):
	n = getattr(pygame, "K_" + k)
	return False or (pygame.key.get_pressed()[n])

c = pygame.time.Clock()
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.VIDEORESIZE:
			SCREENSIZE = event.size
			screen = pygame.display.set_mode(SCREENSIZE, pygame.RESIZABLE)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			currentpuzzle.onmousedown(event.pos[0], event.pos[1])
		elif event.type == pygame.MOUSEBUTTONUP:
			currentpuzzle.onmouseup(event.pos[0], event.pos[1])
		elif event.type == pygame.MOUSEMOTION:
			currentpuzzle.onmousemove(event.pos[0], event.pos[1], False or pygame.mouse.get_pressed()[0])
	screen.fill((255, 255, 255))
	screen.blit(currentpuzzle.getFrame(*SCREENSIZE, getkey), (0, 0))
	currentpuzzle = currentpuzzle.getNew()
	pygame.display.flip()
	c.tick(60)