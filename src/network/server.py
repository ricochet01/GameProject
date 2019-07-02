import socket
from _thread import *
import pickle



class Server:

	def __init__(self):
		self.server = socket.gethostbyname(socket.gethostname())
		self.port = 5555
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# self.sheet = sheet

		# numOfPlayers = 1
		# playerImg = {}

		# playerColors = [pg.Color("red"), pg.Color("blue"), pg.Color("green"),
		# 					pg.Color("magenta"), pg.Color("orangered"), pg.Color("white"),
		# 					pg.Color("orange"), pg.Color("yellow"), pg.Color("purple"),
		# 					pg.Color("darkred"), pg.Color("gray")]

		# for i in range(numOfPlayers+1):
		# 	playerImg["player" + str(i)] = [self.sheet.get(0, 5, 16, 16, pg.Color("black")).copy(),
		# 									self.sheet.get(0, 5, 16, 16, pg.Color("black"), 1, 0).copy(),
		# 									self.sheet.get(2, 5, 16, 16, pg.Color("black")).copy(),
		# 									self.sheet.get(2, 5, 16, 16, pg.Color("black"), 1, 0).copy(),
		# 									self.sheet.get(4, 5, 16, 16, pg.Color("black")).copy(),
		# 									self.sheet.get(6, 5, 16, 16, pg.Color("black")).copy(),
		# 									self.sheet.get(4, 5, 16, 16, pg.Color("black"), 1, 0).copy(),
		# 									self.sheet.get(6, 5, 16, 16, pg.Color("black"), 1, 0).copy()]

		# self.players = [Mob(8, 8, 16, 16, playerImg["player0"], [(28, 16, 0), playerColors[0], (255, 178, 127)]),
		# 				Mob(24, 24, 16, 16, playerImg["player1"], [(28, 16, 0), playerColors[1], (255, 178, 127)])]

	def init(self):
		try:
			self.s.bind((self.server, self.port))
		except socket.error as e:
			print(e)

		self.s.listen(2)
		print("Waiting for a connection, Server Started")


	def threadedClient(self, conn, player):
		conn.send(pickle.dumps(self.players[player]))
		reply = ""
		while True:
			try:
				data = pickle.loads(conn.recv(2048))
				self.players[player] = data

				if not data:
					print("Disconnected")
					break
				else:
					print("Received: ", reply)
					print("Sending : ", reply)
					if player == 1:
						reply = self.players[0]
					else:
						reply = self.players[1]

				conn.sendall(pickle.dumps(reply))
			except:
				break

		print("Lost connection")
		conn.close()

	def run(self):
		self.init()
		currentPlayer = 0
		while True:
			conn, addr = self.s.accept()
			print("Connected to:", addr)

			start_new_thread(threaded_client, (conn, currentPlayer))
			currentPlayer += 1


# srv = Server(Spritesheet("res/sheet.png"))
# srv.run()