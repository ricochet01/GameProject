import pygame as pg

from src.entities.entity import Entity


class Mob(Entity):

	def __init__(self, x, y, w, h, sprites, newColors, name=None):
		super().__init__(x, y, w, h, sprites, newColors)
		self.sprites = sprites
		self.newColors = newColors
		self.name = name
		self.ticks = 0
		self.dir = 0

		self.drawX = 0
		self.drawY = 0

		self.hitbox = pg.Rect(self.x + 4, self.y + 10, 8, 5)

		self.movement = [0, 0]
		self.speed = 1

	def draw(self, surface, xo, yo, font):
		surface.blit(self.sprites[(self.ticks//8) + self.dir * 2], (self.hitbox.x - xo - 4, self.hitbox.y - yo - 10))
		if self.name != None:
			surface.blit(font.render(self.name, None, pg.Color("gray")), (self.hitbox.x - 12 - xo, self.hitbox.y - 16 - yo))

	def collide(self, tiles):
		collisions = []
		for tile in tiles:
			if self.hitbox.colliderect(tile):
				collisions.append(tile)
		return collisions

	def applyDirection(self, movement):
		if movement[1] > 0: self.dir = 0
		if movement[1] < 0: self.dir = 1
		if movement[0] > 0 and movement[1] == 0: self.dir = 2
		if movement[0] < 0 and movement[1] == 0: self.dir = 3

	def tick(self):
		if not self.ticks > 14:
			self.ticks += 1
		else:
			self.ticks = 0

	def moveX(self, tiles, screenRect, input):
		if input.left and self.hitbox.x >= 0:
			self.hitbox.x -= self.speed
			self.movement[0] -= 1
		if input.right and self.hitbox.x + 10 <= screenRect.w:
			self.hitbox.x += self.speed
			self.movement[0] += 1

		collisions = self.collide(tiles)

		for tile in collisions:
			if self.movement[0] < 0:
				self.hitbox.left = tile.right
			if self.movement[0] > 0:
				self.hitbox.right = tile.left

	def moveY(self, tiles, screenRect, input):
		if input.up and self.hitbox.y >= 0:
			self.hitbox.y -= self.speed
			self.movement[1] -= 1
		if input.down and self.hitbox.y + 4 <= screenRect.h:
			self.hitbox.y += self.speed
			self.movement[1] += 1

		collisions = self.collide(tiles)

		for tile in collisions:
			if self.movement[1] < 0:
				self.hitbox.top = tile.bottom
			if self.movement[1] > 0:
				self.hitbox.bottom = tile.top

	def move(self, tiles, screenRect, input):
		self.colTypes = {
			"left": False,
			"right": False,
			"up": False,
			"down": False
		}
		self.movement = [0, 0]

		self.moveX(tiles, screenRect, input)
		self.moveY(tiles, screenRect, input)

		if self.movement[0] != 0 or self.movement[1] != 0:
			self.tick()

		self.applyDirection(self.movement)

		return self.colTypes




