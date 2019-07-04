import pygame as pg
from pygame.locals import *

import random
import datetime
import json
import numpy as np

from src.constants import *
from src.keyinput import KeyInput
from src.gfx.spritesheet import SpriteSheet
from src.gfx.font import Font
from src.gfx.color import Color
from src.entities.entity import Entity
from src.entities.mob import Mob
from src.entities.alert import Alert
from src.level.level import Level
from src.level.tiles.tile import Tile
from src.level.tiles.flowertile import FlowerTile
from src.menus.pausemenu import PauseMenu
from src.entities.gameoverscreen import GameOverPrompt
from src.entities.textinput import TextInput
# from src.network.network import Network


class Game:

	def __init__(self):
		self.display = pg.Surface((Const.WIDTH, Const.HEIGHT), DOUBLEBUF | HWSURFACE).convert()

		self.movement = [0, 0]

		self.input = KeyInput()
		self.sheet = SpriteSheet("res/sheet.png")
		self.font = Font(self.sheet)

		self.inGame = True
		self.new = False

		self.setup()

	def loadingScreenSetup(self):
		self.loadingScreen = pg.Surface((Const.WIDTH, Const.HEIGHT), DOUBLEBUF | HWSURFACE).convert()
		msg = "Loading..."
		self.loadingScreen.blit(self.font.render(msg, pg.Color("black"), pg.Color("white")), (40, 56))

		Const.win.blit(pg.transform.scale(self.loadingScreen, Const.WINDOW_SIZE), (0, 0))
		pg.display.flip()

	def setup(self):
		self.xOffset = 0
		self.yOffset = 0
		self.solidTiles = []

		self.seconds = 0
		self.isOver = False

		with open("cfg/gameconfig.json", "r") as f:
			self.configData = json.load(f)

		self.dif = self.configData["Difficulty"]
		self.timeLimit = self.configData["Time limit"]
		self.levelW, self.levelH = self.configData["Size"]
		self.density = self.configData["Density"]

		self.soundSetup()
		self.loadingScreenSetup()
		self.guiSetup()
		self.levelSetup()
		self.playerSetup()
		self.cameraApply()
		self.gfxSetup()

	def soundSetup(self):
		self.goBack = pg.mixer.Sound("res/goback.wav")
		self.select = pg.mixer.Sound("res/select.wav")
		self.sfx = [self.goBack, self.select]

		for s in self.sfx:
			s.set_volume(Const.volume/100)
		
	def playerSetup(self):
		numOfPlayers = 1
		playerImg = {}

		for i in range(numOfPlayers+1):
			playerImg["player" + str(i)] = [self.sheet.get(0, 5, 16, 16, pg.Color("black")).copy(),
											self.sheet.get(0, 5, 16, 16, pg.Color("black"), 1, 0).copy(),
											self.sheet.get(2, 5, 16, 16, pg.Color("black")).copy(),
											self.sheet.get(2, 5, 16, 16, pg.Color("black"), 1, 0).copy(),
											self.sheet.get(4, 5, 16, 16, pg.Color("black")).copy(),
											self.sheet.get(6, 5, 16, 16, pg.Color("black")).copy(),
											self.sheet.get(4, 5, 16, 16, pg.Color("black"), 1, 0).copy(),
											self.sheet.get(6, 5, 16, 16, pg.Color("black"), 1, 0).copy()]

		rndTile = random.choice(self.tiles)
		while rndTile.type != "grass":
			rndTile = random.choice(self.tiles)

		playerX = rndTile.x
		playerY = rndTile.y

		playerColors = [pg.Color("red"), pg.Color("blue"), pg.Color("green"),
							pg.Color("magenta"), pg.Color("orangered"), pg.Color("white"),
							pg.Color("orange"), pg.Color("yellow"), pg.Color("purple"),
							pg.Color("darkred"), pg.Color("gray")]

		self.player = Mob(playerX, playerY, 16, 16, playerImg["player0"], [(28, 16, 0), playerColors[Const.playerColor], (255, 178, 127)])
		# self.player2 = Mob(16, 16, 16, 16, playerImg["player1"], [(28, 16, 0), playerColors[0], (255, 178, 127)])

	def guiSetup(self):
		self.score = 0
		self.seconds = 0

		alertMsg = "Click to play!"
		alertWidth = (16 + len(alertMsg) * 8)
		alertColor = pg.Color("darkred")
		self.alert = Alert(self.display.get_width()/2 - alertWidth/2, self.display.get_height()/2 - 12, 16 + len(alertMsg)*8, 24,
							[self.sheet.get(0, 1, 8, 8, pg.Color("black")).copy(), self.sheet.get(1, 1, 8, 8, pg.Color("black")).copy()],
							[(64, 64, 64), (128, 128, 128), alertColor], alertColor, alertMsg)

		m = "Your name:"
		self.nameInput = TextInput(32, 44, 96, 32, [self.sheet.get(0, 1, 8, 8, pg.Color("black")).copy(),
										self.sheet.get(1, 1, 8, 8, pg.Color("black")).copy()],
										[(64, 64, 64), (128, 128, 128), pg.Color("blue")], pg.Color("blue"), m, self.score)

	def gfxSetup(self):
		self.crtEffect = False

		self.scanlines = pg.Surface((160, 120), DOUBLEBUF | HWSURFACE | SRCALPHA, 32).convert_alpha()
		for y in range(0, 160, 2):
			line = pg.Surface((160, 1), DOUBLEBUF | HWSURFACE | SRCALPHA, 32).convert_alpha()
			line.fill(pg.Color(0, 0, 0))
			self.scanlines.blit(line, (0, y))

	def levelSetup(self):
		self.level = Level.generateLevel(self.levelW, self.levelH, self.density)

		self.levelWidth = len(self.level[0]) << 3
		self.levelHeight = len(self.level) << 3
		self.screenRect = pg.Rect(0, 0, self.levelWidth, self.levelHeight)

		self.tiles = []

		self.flowerObjects = []
		flowerColors = ["red", "yellow", "green"]

		i = 0
		for y, layer in enumerate(self.level):
			for x, t in enumerate(layer):
				if t == "1":
					self.tiles.append(Tile(x << 3, y << 3, 8, 8, self.sheet.get(random.randint(0, 3), 0, 8, 8, pg.Color("black")),
						[pg.Color(49, 127, 52), pg.Color("green")], "grass", False, i))
				elif t == "2":
					flower = FlowerTile(x << 3, y << 3, 8, 8, self.sheet.get(4, 0, 8, 8),
						[pg.Color(49, 127, 52), pg.Color(0, 112, 0), pg.Color("red"), pg.Color(200, 200, 200)],
						"flower", False, i, random.choice(flowerColors), self.dif)
					self.tiles.append(flower)
					self.flowerObjects.append(flower)
				elif t == "3":
					self.tiles.append(Tile(x << 3, y << 3, 8, 8, self.sheet.get(random.randint(0, 3), 0, 8, 8, pg.Color("black")),
						[pg.Color(85, 0, 0), pg.Color("gray")], "dirt", False, i))
				
				i += 1

	def start(self):
		self.running = True
		self.dt = clock.tick(fps) / 1000.0

		# self.n = Network()
		# self.player = n.getPlayer()

		self.setup()

	def tick(self):
		self.dt = clock.tick(fps) / 1000.0

		self.input.tick()
		self.alert.tick()

		# self.p2 = n.send(self.p)

		if self.input.hasFocus() and not self.isOver:
			if self.timeLimit - (self.seconds//60) > 0 and any(isinstance(i, FlowerTile) for i in self.tiles):
				self.seconds += 1
			else:
				self.isOver = True

			self.tiles, self.score, self.solidTiles = Level.render(self.display, self.tiles, Const.WIDTH, Const.HEIGHT,
										self.xOffset, self.yOffset, self.player, self.sheet, self.score)

			self.playerUpdate()


	def takeScreenshot(self):
		screenshot = pg.transform.scale(pg.surfarray.make_surface(self.pixels), Const.WINDOW_SIZE)
		current = datetime.datetime.now()
		imgname = "screenshot-" + current.strftime("%Y-%m-%d-%H-%M-%S") + ".png"
		scrnsht_file = pg.image.save(screenshot, "screenshots/" + imgname)

	def cameraApply(self):
		if self.player.hitbox.x <= (Const.WIDTH / 2 - 8) + 4:
			self.xOffset = 0
		elif self.player.hitbox.x >= self.levelWidth - (Const.WIDTH / 2) - 4:
			self.xOffset = self.levelWidth - Const.WIDTH
		else:
			self.xOffset = int(self.player.hitbox.x - (Const.WIDTH / 2 - 8)) - 4

		if self.player.hitbox.y <= (Const.HEIGHT / 2 - 8) + 9:
			self.yOffset = 0
		elif self.player.hitbox.y >= self.levelHeight - (Const.HEIGHT / 2) + 2:
			self.yOffset = self.levelHeight - Const.HEIGHT
		else:
			self.yOffset = int(self.player.hitbox.y - (Const.HEIGHT / 2 - 8)) - 9

	def renderGameOverScreen(self):
		if self.isOver:
			self.input.releaseAll()

			self.nameInput.score = self.score

			if self.nameInput.done:
				self.nameInput.running = False
				messages = ["Game over!", "Score: " + str(self.score), "ESC to return", "ENTER to restart"]

				gameOverScreen = GameOverPrompt(self.display.get_width()/2 - len(messages[3])*4 - 8, self.display.get_height()/2 - len(messages)*8+8,
												len(messages[3])*8 + 16, len(messages)*8 + 16, [self.sheet.get(0, 1, 8, 8, pg.Color("black")).copy(),
												self.sheet.get(1, 1, 8, 8, pg.Color("black")).copy()],
												[(64, 64, 64), (128, 128, 128), pg.Color("blue")], pg.Color("blue"), messages)

				gameOverScreen.render(self.display, self.font)
			else:
				self.nameInput.render(self.display)

	def playerUpdate(self):
		# self.p2.draw(self.display, self.xOffset, self.yOffset, self.font)
		self.player.draw(self.display, self.xOffset, self.yOffset, self.font)
		self.player.move(self.solidTiles, self.screenRect, self.input)

	def renderAlert(self):
		if not self.input.hasFocus():
			self.input.releaseAll()
			self.alert.render(self.display, self.font)

	def eventHandler(self):
		if not self.nameInput.running:
			for event in pg.event.get():
				if event.type == QUIT:
					stop()

				if event.type == KEYDOWN:
					if event.key == K_F12:
						self.takeScreenshot()

					if event.key == K_ESCAPE and self.isOver:
						self.goBack.play()
						self.new = False
						self.running = False

					if event.key == K_RETURN and self.isOver:
						self.select.play()
						self.new = True
						self.running = False

					if event.key == K_ESCAPE and not self.isOver:
						self.goBack.play()
						self.input.releaseAll()
						pauseScreen = PauseMenu()
						pauseScreen.main()
						self.soundSetup()
						FlowerTile.soundSetup()
						if pauseScreen.parentVal:
							self.input.releaseAll()
							self.inGame = False
							self.new = False
							self.running = False

	def render(self):
		# Draw the hud; contains the time left and the score
		self.renderGameOverScreen()
		
		self.display.blit(self.font.render("Time left: " + str(self.timeLimit - self.seconds//60), None, pg.Color("white")), (28, Const.HEIGHT - 16))

		if self.score == 0:
			self.scoreLabel = self.font.render("Score: " + str(self.score), None, pg.Color("yellow"))
		elif self.score > 0:
			self.scoreLabel = self.font.render("Score: " + str(self.score), None, pg.Color("green"))
		else:
			self.scoreLabel = self.font.render("Score: " + str(self.score), None, pg.Color("red"))

		self.display.blit(self.scoreLabel, (self.display.get_width()/2 - self.scoreLabel.get_width()/2, Const.HEIGHT - 8))

		self.renderAlert()

		if Const.crtEffect and Const.filters:
			self.display.blit(self.scanlines, (0, 0))
			self.scanlines.set_alpha(64)

		self.filter = pg.surfarray.array3d(self.display)
		self.pixels = np.array(self.filter)

		if Const.filters:
			if Const.redChannel:
				self.pixels[:,:,0] += Const.redChannel
			if Const.greenChannel:
				self.pixels[:,:,1] += Const.greenChannel
			if Const.blueChannel:
				self.pixels[:,:,2] += Const.blueChannel
			if Const.inversion:
				self.pixels ^= Const.inversion

		Const.win.blit(pg.transform.scale(pg.surfarray.make_surface(self.pixels), Const.WINDOW_SIZE), (0, 0))

		# if self.crtEffect:
		# 	self.scanlines.set_alpha(64)

		pg.display.flip()

	def main(self):
		while self.inGame:
			self.start()
			while self.running:
				self.tick()

				self.cameraApply()

				self.render()
				self.eventHandler()

			if self.new: continue
			else: break


