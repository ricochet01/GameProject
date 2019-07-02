import pygame as pg

from src.menus.menu import Menu


class AboutMenu(Menu):

	def __init__(self):
		super().__init__()
		self.currentMenu = "About"
		self.center = self.display.get_width() / 2 - len(self.currentMenu) * 4

	def menuUpdate(self):
		self.display.blit(self.font.render(self.currentMenu, None, pg.Color("white")), (self.center, 4))

		self.display.blit(self.font.render("This game was made", None, pg.Color("gray")), (4, 14))
		self.display.blit(self.font.render("by ric0chet in 3", None, pg.Color("gray")), (4, 22))
		self.display.blit(self.font.render("weeks. It was made", None, pg.Color("gray")), (4, 30))
		self.display.blit(self.font.render("as a side project.", None, pg.Color("gray")), (4, 38))
		self.display.blit(self.font.render("Created in pygame<3", None, pg.Color("gray")), (4, 70))
		self.display.blit(self.font.render("Copyright 2019.", None, pg.Color("gray")), (4, 104))
		self.display.blit(self.font.render("All rights reserved", None, pg.Color("gray")), (4, 112))

