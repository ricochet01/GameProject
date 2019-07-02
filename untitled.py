from src.menus.mainmenu import MainMenu
import os

os.environ["SDL_VIDEO_CENTERED"] = "1"

l = True

while l:
	titleMenu = MainMenu()
	titleMenu.main()