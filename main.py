"""
A puzzle game written with Python.
"""

import pygame

SCREENSIZE = [640, 480]
screen = pygame.display.set_mode(SCREENSIZE, pygame.RESIZABLE)

c = pygame.time.Clock()
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.VIDEORESIZE:
			SCREENSIZE = event.size
			screen = pygame.display.set_mode(SCREENSIZE, pygame.RESIZABLE)
	screen.fill((255, 255, 255))
	pygame.display.flip()
	c.tick(60)