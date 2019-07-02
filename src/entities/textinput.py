import pygame as pg
from pygame.locals import *

from src.entities.alert import Alert
from src.gfx.font import Font
from src.constants import stop
from src.gfx.spritesheet import SpriteSheet

import json
import datetime


class TextInput(Alert):

	def __init__(self, x, y, w, h, sprites, newColors, msgColor, msg, score):
		super().__init__(x, y, w, h, sprites, newColors, msgColor, msg)
		sheet = SpriteSheet("res/sheet.png")
		self.font = Font(sheet)
		self.result = ""
		self.done = False
		self.running = False
		self.score = score

		with open("cfg/data.json", "r") as f:
			self.scores = json.load(f)

		with open("cfg/gameconfig.json", "r") as f:
			self.gameConfig = json.load(f)

		self.dif = self.gameConfig["Difficulty"]
		self.density = self.gameConfig["Density"]
		self.size = self.gameConfig["Size"]
		self.timer = self.gameConfig["Time limit"]

	def eventHandler(self):
		for event in pg.event.get():
			if event.type == QUIT:
				stop()

			if event.type == KEYDOWN:
				if len(self.result) < 8:
					if event.unicode in self.font.legalChars:
						self.result += event.unicode

				if event.key == K_RETURN:
					self.done = True
					if len(self.result) != 0:
						valid = self.result.isspace()
						if not valid:
							with open("cfg/data.json", "w") as f:
								scoreInput = {}
								
								scoreInput["Name"] = self.result
								scoreInput["Score"] = self.score
								scoreInput["Difficulty"] = self.dif
								scoreInput["Density"] = self.density
								scoreInput["Size"] = self.size
								scoreInput["Time limit"] = self.timer

								current = datetime.datetime.now()
								date = current.strftime("%Y-%m-%d")
								time = current.strftime("%H:%M:%S")

								scoreInput["Date"] = date
								scoreInput["Time"] = time
								self.scores.append(scoreInput)

								json.dump(self.scores, f, indent=4)

				if event.key == K_ESCAPE:
					self.done = True

				if event.key == K_BACKSPACE:
					if len(self.result) != 0:
						self.result = self.result[:-1]

	def render(self, surface):
		self.tick()
		self.running = True

		self.drawOutline()

		tempSurf = pg.Surface((self.w-16, 8)).convert()
		tempSurf.fill(self.msgColor)
		tempSurf.blit(self.font.render(self.msg, self.msgColor, pg.Color("white") if self.ticks < 30 else pg.Color("dimgray")),
			(tempSurf.get_width()/2 - len(self.msg)*4, 0))
		self.area.blit(tempSurf, (8, 8))

		textSurf = pg.Surface((self.w-16, 8)).convert()
		textSurf.fill(self.msgColor)
		textSurf.blit(self.font.render(self.result, self.msgColor, pg.Color("white")), (0, 0))
		self.area.blit(textSurf, (8, 16))

		self.eventHandler()

		surface.blit(self.area, (self.x, self.y))

