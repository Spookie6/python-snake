# Example file showing a basic pg "game loop"
import pygame as pg
import datetime, random

resolution = (1280,720)

# pygame setup
pg.init()
screen = pg.display.set_mode(resolution, pg.NOFRAME)
clock = pg.time.Clock()
running = True
dt = 0

resizeScale = resolution[1] / 720

class Constants:
	def __init__(self) -> None:
		self.font = pg.font.Font("RetroFont.ttf", 32)

		self.gridSize = 16 * resizeScale
		self.gameBoardSize = 40 # n^2 * gridsize
		
		self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # left, right, up, down
		self.keys = [97, 100, 119, 115]	# A D W S
 
		self.colors = ["gray3", "darkred", "darkblue", "purple"]
						# 0: empty, 1: fruit, 2: body, 3: head

constants = Constants()

class Tile():
	def __init__(self) -> None:
		self.id = 0 # 0: empty, 1: fruit, 2: body, 3: head
		self.color = constants.colors[self.id]
  
	def update(self, id) -> None:
		self.id = id
		self.color = constants.colors[id]

class Game:
	def __init__(self, screen:pg.Surface, snake) -> None:
		self.grid = ([[Tile() for i in range(constants.gameBoardSize)] for j in range(constants.gameBoardSize)])
		w = h = constants.gameBoardSize*constants.gridSize
		self.rect = pg.Rect(resolution[0]/2 - w/2, resolution[1]/2 - h/2, w, h)

		self.hasStarted = False
		self.gameOver = False
  
		self.screen = screen
		self.snake:Snake = snake
		self.newHead = None
		self.fruit = [20, 6]
  
		self.lastUpdate = 0
		self.keyBuffer = list()

	def update(self):
		now = datetime.datetime.now().timestamp() * 1000
		if now - self.lastUpdate >= 50:
			self.lastUpdate = now
			for row in self.grid:
				for tile in row:
					tile.update(0)

			self.snake.move()
			self.grid[self.fruit[0]][self.fruit[1]].update(1)
			for index, coord in enumerate(self.snake.body):
				if index == 0: self.grid[coord[1]][coord[0]].update(3)
				else: self.grid[coord[1]][coord[0]].update(2)

		self.draw()
  
	def generateFruit(self):
		while True:
			rand = random.choice(random.choice(self.grid))
			coords = None
			for y, row in enumerate(self.grid):
				if rand in row:
					coords = [row.index(rand), y]
			if coords not in self.snake.body:
				coords.reverse()
				self.fruit = coords
				break

	def draw(self) -> None:
		pg.draw.rect(self.screen, pg.Color("gray6"), self.rect)
		for i, row in enumerate(self.grid):
			for j, tile in enumerate(row):
				gs = constants.gridSize
				rect = pg.Rect(game.rect[0] + j*gs, game.rect[1] + i*gs, gs-1, gs-1)
				pg.draw.rect(self.screen, tile.color, rect)

		# Draw some lines around the gameboard
		x, y, w, h, = self.rect
		pg.draw.lines(self.screen, pg.Color("azure2"), True, [(x, y),(x + w, y),(x + w, y + h),(x, y + h)])
  
		# Game over message
		if self.gameOver:
			gameOverTitle = constants.font.render("GAME OVER", False, pg.Color("azure2"))
			_, __, w, h = gameOverTitle.get_rect()
			screen.blit(gameOverTitle, (resolution[0]/2 - w/2, resolution[1]/2 - h/2))	

class Snake:
	def	__init__(self) -> None:
		self.body = [[2, 20], [1, 20], [0, 20]] # Head is at index = 0
		self.direction = constants.directions[1]

	def move(self) -> None:
		if len(game.keyBuffer):
			index = constants.keys.index(game.keyBuffer[0])
			newdir = constants.directions[index]
			if newdir[0] + self.direction[0] != 0 and newdir[1] + self.direction[1] != 0: self.direction = newdir
  
		game.keyBuffer = []
		self.newHead = [self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1]]
		nextIsFruit = self.checkCollisions()
		if game.gameOver: return
		self.body.insert(0, self.newHead)

		if not nextIsFruit:
			self.body.pop()
		else:
			game.generateFruit()


	def checkCollisions(self) -> None|bool:
		if self.newHead[0] < 0: self.newHead[0] = constants.gameBoardSize-1
		if self.newHead[0] > constants.gameBoardSize-1: self.newHead[0] = 0
		if self.newHead[1] < 0: self.newHead[1] = constants.gameBoardSize-1
		if self.newHead[1] > constants.gameBoardSize-1: self.newHead[1] = 0

		if game.fruit == [self.newHead[1], self.newHead[0]]: return True
		if self.newHead in self.body: 
			game.gameOver = True
			return
		return False

game = Game(screen, Snake())


while running:
	# poll for events
	# pg.QUIT event means the user clicked X to close your window
	for event in pg.event.get():
		keys = pg.key.get_pressed()
		if event.type == pg.QUIT:
			running = False
		if event.type == pg.KEYDOWN:
			if event.key in constants.keys: game.keyBuffer.insert(0, event.key)
			if keys[pg.K_ESCAPE]:
				pg.quit()
	# fill the screen with a color to wipe away anything from last frame
	screen.fill("black")
 
	# RENDER YOUR GAME HERE
	# Render floor

	if not game.gameOver:
		game.update()
	else: game.draw()
 
	# flip() the display to put your work on screen
	pg.display.flip()

	dt = clock.tick(60) / 1000  # limits FPS to 60

pg.quit()
