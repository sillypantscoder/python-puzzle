"""
A puzzle game written with Python.
"""

import pygame
import puzzles

SCREENSIZE = [640, 480]
screen = pygame.display.set_mode(SCREENSIZE, pygame.RESIZABLE)

currentpuzzle = puzzles.Level1()

c = pygame.time.Clock()
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.VIDEORESIZE:
			SCREENSIZE = event.size
			screen = pygame.display.set_mode(SCREENSIZE, pygame.RESIZABLE)
		elif event.type == pygame.MOUSEDOWN:
			currentpuzzle.handleclick(event.pos[0], event.pos[1])
	screen.fill((255, 255, 255))
	screen.blit(currentpuzzle.getFrame(*SCREENSIZE), (0, 0))
	pygame.display.flip()
	c.tick(60)