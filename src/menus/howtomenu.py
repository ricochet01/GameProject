import pygame as pg

from src.menus.menu import Menu


class HowToPlayMenu(Menu):

	def __init__(self):
		super().__init__()
		self.currentMenu = "How to play"
		self.center = self.display.get_width() / 2 - len(self.currentMenu) * 4

	def menuUpdate(self):
		self.display.blit(self.font.render(self.currentMenu, None, pg.Color("white")), (self.center, 4))

		self.display.blit(self.font.render("Move with the arrow", None, pg.Color("gray")), (4, 14))
		self.display.blit(self.font.render("keys or the WASD", None, pg.Color("gray")), (4, 22))
		self.display.blit(self.font.render("keys. The goal of", None, pg.Color("gray")), (4, 30))
		self.display.blit(self.font.render("this game is to", None, pg.Color("gray")), (4, 38))
		self.display.blit(self.font.render("collect green", None, pg.Color("gray")), (4, 46))
		self.display.blit(self.font.render("mines and avoid", None, pg.Color("gray")), (4, 54))
		self.display.blit(self.font.render("the red mines.", None, pg.Color("gray")), (4, 62))
		self.display.blit(self.font.render("Press F12 to take", None, pg.Color("gray")), (4, 70))
		self.display.blit(self.font.render("a screenshot.", None, pg.Color("gray")), (4, 78))

			