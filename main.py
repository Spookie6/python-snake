# Example file showing a basic pg "game loop"
import pygame as pg
import datetime

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
		self.colors = ["darkgreen", "darkred", "darkblue", "purple"]

constants = Constants()

class Pos:
	def __init__(self, x, y) -> None:
		self.x = x
		self.y = y

	def getTuple(self) -> tuple:
		return (self.x, self.y)

class Tile():
	def __init__(self) -> None:
		self.id = 0 # 0: empty, 1: fruit, 2: body, 3: head
		self.color = constants.colors[self.id]
  
	def update(self, id) -> None:
		self.id = id
		self.color = constants.colors[id]

class Game:
	def __init__(self, screen:pg.Surface, snake) -> None:
		self.grid = ([[Tile() for i in range(constants.gameBoardSize)] for i in range(constants.gameBoardSize)])
		w = h = constants.gameBoardSize*constants.gridSize
		self.rect = pg.Rect(resolution[0]/2 - w/2, resolution[1]/2 - h/2, w, h)
		self.player = None
		self.hasStarted = False
		self.gameOver = False
  
		self.screen = screen
		self.snake = snake
  
		self.lastUpdate = 0
		self.keyBuffer = []

	def draw(self) -> None:
		start = (self.rect[0], self.grid[1])
		for i, row in enumerate(self.grid):
			for j, tile in enumerate(row):
				gs = constants.gridSize
				rect = pg.Rect(game.rect[0] + j*gs, game.rect[1] + i*gs, gs-1, gs-1)
				pg.draw.rect(self.screen, tile.color, rect)
	
		# Draw some lines around the gameboard
		x, y, w, h, = self.rect
		pg.draw.lines(screen, pg.Color("azure2"), True, [(x, y),(x + w, y),(x + w, y + h),(x, y + h)])

	def update(self):
		# Update key buffer
		now = datetime.datetime.now().timestamp() * 1000
		if now - self.lastUpdate >= 200:
			self.lastUpdate = now
			for row in self.grid:
				for tile in row:
					tile.update(0)
			print(self.snake.body)
			self.snake.move(self.keyBuffer)
			for index, coord in enumerate(self.snake.body):
				if index == 0: self.grid[coord[0]][coord[1]].update(3)
				else: self.grid[coord[0]][coord[1]].update(2)
		self.draw()

class Snake:
	def	__init__(self,keys) -> None:
		self.body = [[2, 20], [1, 20], [0, 20]] # Head is at index = 0
		self.direction = constants.directions[3]

	def move(self) -> None:
		if (len(keys)): pass
		
		self.body.pop()
		newHead = (self.body[0][0] + self.direction[0],self.body[0][1] + self.direction[1])
		self.body.insert(0, newHead)

	def checkCollisions(self) -> None:
		pass

game = Game(screen, Snake())
keys = dict()

while running:
	# poll for events
	# pg.QUIT event means the user clicked X to close your window
	for event in pg.event.get():
		keys = pg.key.get_pressed()
		if event.type == pg.QUIT:
			running = False
		if event.type == pg.KEYDOWN:
			if keys[pg.K_ESCAPE]:
				pg.quit()
	# fill the screen with a color to wipe away anything from last frame
	screen.fill("black")
 
	# RENDER YOUR GAME HERE
	# Render floor
	
	pg.draw.rect(screen, pg.Color("gray3"), game.rect)
	game.update()
 
	# flip() the display to put your work on screen
	pg.display.flip()

	dt = clock.tick(60) / 1000  # limits FPS to 60

pg.quit()
