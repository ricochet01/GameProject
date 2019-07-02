import pygame as pg
import random

from src.level.tiles.tile import Tile
from src.constants import Const


class FlowerTile(Tile):

	redFlower = [pg.Color(49, 127, 52), pg.Color(0, 112, 0), pg.Color("red"), pg.Color(200, 200, 200)]
	yellowFlower = [pg.Color(49, 127, 52), pg.Color(0, 112, 0), pg.Color("yellow"), pg.Color(200, 200, 200)]
	greenFlower = [pg.Color(49, 127, 52), pg.Color(0, 112, 0), pg.Color("green"), pg.Color(200, 200, 200)]

	def __init__(self, x, y, w, h, sprite, newColors, type, solid, id, color, dif):
		super().__init__(x, y, w, h, sprite, newColors, type, solid, id)
		self.color = color

		if dif == "Easy":
			self.limit = 540
		elif dif == "Medium":
			self.limit = 360
		elif dif == "Hard":
			self.limit = 180

		if self.color == "red":
			self.ticks = random.randint(0, int(self.limit - (self.limit/1.5)))
		elif self.color == "yellow":
			self.ticks = random.randint(int(self.limit - (self.limit/1.5)), int(self.limit - (self.limit/3)))
		else:
			self.ticks = random.randint(int(self.limit - (self.limit/3)), self.limit)

		self.soundSetup()

		
	@classmethod
	def soundSetup(cls):
		# The sound effects for stepping on flowers
		cls.explosion = pg.mixer.Sound("res/explosion.wav")
		cls.greenPickup = pg.mixer.Sound("res/pickup.wav")
		cls.yellowPickup = pg.mixer.Sound("res/yellowpickup.wav")

		cls.sounds = [cls.explosion, cls.greenPickup, cls.yellowPickup]
		for sound in cls.sounds:
			sound.set_volume(Const.volume/100)



	def draw(self, surface, xo, yo, player, tiles, sheet, score):
		surface.blit(self.sprite, (self.hitbox.x - xo, self.hitbox.y - yo))

		tiles, score = self.checkCollision(player, tiles, sheet, score)
		self.setColor()
		self.tick()

		return tiles, score

	def tick(self):
		if not self.ticks > self.limit:
			self.ticks += 1
		else:
			self.ticks = 0

	def checkCollision(self, player, tiles, sheet, score):
		if player.hitbox.colliderect(self.hitbox) and self in tiles:
			if self.color == "red":
				score -= 10
				self.explosion.play()
			elif self.color == "yellow":
				self.yellowPickup.play()
			elif self.color == "green":
				score += 10
				self.greenPickup.play()
			tiles[self.id] = Tile(self.x, self.y, 8, 8, sheet.get(random.randint(0, 3), 0, 8, 8),
				[pg.Color(85, 0, 0), pg.Color("gray")], "dirt", False, self.id)

		return tiles, score

	def setColor(self):
		if self.ticks % self.limit < int(self.limit - (self.limit/1.5)):
			self.colorize(self.greenFlower, [pg.Color(49, 127, 52), pg.Color(0, 112, 0), pg.Color("red"), pg.Color(200, 200, 200)])
			self.color = "red"
		elif self.ticks % self.limit < int(self.limit - (self.limit/3)):
			self.colorize(self.redFlower, [pg.Color(49, 127, 52), pg.Color(0, 112, 0), pg.Color("yellow"), pg.Color(200, 200, 200)])
			self.color = "yellow"
		elif self.ticks % self.limit < self.limit:
			self.colorize(self.yellowFlower, [pg.Color(49, 127, 52), pg.Color(0, 112, 0), pg.Color("green"), pg.Color(200, 200, 200)])
			self.color = "green"



