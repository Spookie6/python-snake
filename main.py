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

resizeFactor = resolution[1] / 720

spritesheet = pg.image.load("spritesheet.png").convert_alpha()

class Constants:
	def __init__(self) -> None:
		self.font = pg.font.Font("RetroFont.ttf", 32)

		self.gridSize = 16 * resizeFactor
		self.gameBoardSize = 40 # n^2 * gridsize
		
		self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # left, right, up, down
		self.keys = [97, 100, 119, 115]	# A D W S
 
		self.colors = ["gray3", "darkred", "darkblue", "purple", "pink"]
						# 0: empty, 1: fruit, 2: body, 3: head, 4: tail

constants = Constants()

# class Sprites():
# 	vertical = (128, 64)
# 	horizontal = (64, 0)
	
# 	corner_br = (0, 0)
# 	corner_bl = (128, 0)
# 	corner_tr = (0, 64)
# 	corner_tl = (128, 128)
	
# 	head = [(192, 64),(256, 0),(256, 64),(192, 0)]
	
# tails = [(192, 192), (256, 128),(192, 128),(256, 192)]
# 	tail_l = 
# 	tail_r = 
# 	tail_t = 
# 	tail_b = 
	
# 	fruit = (0, 192)
	
# 	def __init__(self):
# 		keys = list(filter(lambda x : not x.startswith("__"), Sprites.__dict__.keys()))

# 		for key in keys:
# 			value = Sprites.__dict__[key]
# 			# self[key.split("_")[0]][key.split("_")[1]] = 

def getImg(coords) -> pg.Surface:
	img = pg.Surface((64, 64))
	img.blit(spritesheet, (0, 0), (coords[0], coords[1], 64, 64))
	img = pg.transform.scale(img, (constants.gridSize, constants.gridSize))
	img.set_colorkey((0, 0, 0))
	return img

heads = [(192, 64),(256, 0),(192, 0),(256, 64),(0, 0)]
tails = [(256, 128),(192, 192),(256, 192),(192, 128)]

corners = [[(128, 128),(128, 0)], [(0, 64),]]

sprites = dict({"head": [], "tail": [], "corner": []})

sprites["fruit"] = getImg((0, 192))
sprites["vertical"] = getImg((128, 64))
sprites["horizontal"] = getImg((64, 0))

for head in heads:
	img = getImg(head)
	sprites["head"].append(img)
 
for tail in tails:
	img = getImg(tail)
	sprites["tail"].append(img)

class Tile():
	def __init__(self) -> None:
		self.update(0)
  
	def update(self, id) -> None:
		self.id = id # empty, 1: fruit, 2: body, 3: head, 4: tail
		self.color = constants.colors[id]
		self.sprite = None
		if id == 2:
			coords = None
			for y, row in enumerate(game.grid):
				if self in row:
					coords = [row.index(self), y]
			index = game.snake.body.index(coords)

			current = game.snake.body[index]
			prev = game.snake.body[index -1]
			next = game.snake.body[index +1]
			
			prevDir = [current[0] - prev[0], current[1] - prev[1]]
			nextDir = [next[0] - current[0], next[1] - current[1]]
	
			print(prevDir, nextDir)
   
			prevDirIndex = constants.directions.index(tuple(prevDir))
			nextDirIndex = constants.directions.index(tuple(nextDir))
   
			if prevDirIndex == nextDirIndex:
				if prevDirIndex == 0 or prevDir == 1:
					self.sprite = sprites["horizontal"]
		if id == 3:
			index = constants.directions.index(tuple(game.snake.direction))
			self.sprite = sprites["head"][index]
		if id == 4:
			lastInd = len(game.snake.body) - 1
			direction = [game.snake.body[lastInd][0] - game.snake.body[lastInd - 1][0], game.snake.body[lastInd][1] - game.snake.body[lastInd - 1][1]]
			index = constants.directions.index(tuple(direction))
			self.sprite = sprites["tail"][index]
	
		if id == 1:
			self.sprite = sprites["fruit"]

class Game:
	def __init__(self, screen:pg.Surface, snake) -> None:
		self.grid = ([[Tile() for i in range(constants.gameBoardSize)] for j in range(constants.gameBoardSize)])
		w = h = constants.gameBoardSize*constants.gridSize
		self.rect = pg.Rect(resolution[0]/2 - w/2, resolution[1]/2 - h/2, w, h)
		self.screen = screen

		self.hasStarted = False
		self.gameOver = False
  
		self.snake:Snake = snake
		self.newHead = None
		self.fruit = [20, 6]
		self.score = 0
  
		self.lastUpdate = 0
		self.keyBuffer = list()

	def update(self):
		now = datetime.datetime.now().timestamp() * 1000
		if now - self.lastUpdate >= 200:
			self.lastUpdate = now
			for row in self.grid:
				for tile in row:
					tile.update(0)

			self.snake.move()
			self.grid[self.fruit[0]][self.fruit[1]].update(1)
			for index, coord in enumerate(self.snake.body):
				if index == 0: self.grid[coord[1]][coord[0]].update(3)
				elif index == len(self.snake.body) - 1: self.grid[coord[1]][coord[0]].update(4)
				else: self.grid[coord[1]][coord[0]].update(2)
			# print(self.snake.body)
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
				if tile.sprite:
					self.screen.blit(tile.sprite, (game.rect[0] + j*gs, game.rect[1] + i*gs))
				else:
					rect = pg.Rect(game.rect[0] + j*gs, game.rect[1] + i*gs, gs, gs)
					pg.draw.rect(self.screen, tile.color, rect)

		# Draw some lines around the gameboard
		x, y, w, h, = self.rect
		pg.draw.lines(self.screen, pg.Color("azure2"), True, [(x, y),(x + w, y),(x + w, y + h),(x, y + h)])
  
		scoreTItle = constants.font.render(f"{self.score:02d}", False, pg.Color("azure2"))
		_, __, w, h = scoreTItle.get_rect()
		screen.blit(scoreTItle, (resolution[0] * resizeFactor * .85, resolution[1]/2 - h/2))
  
		# Game over message
		if self.gameOver:
			gameOverTitle = constants.font.render("GAME OVER", False, pg.Color("azure2"))
			_, __, w, h = gameOverTitle.get_rect()
			screen.blit(gameOverTitle, (resolution[0]/2 - w/2, resolution[1]/2 - h/2))
   
			playAgainTitle = constants.font.render("Press R to restart", False, pg.Color("azure2"))
			_, __, w, h = playAgainTitle.get_rect()
			screen.blit(playAgainTitle, (resolution[0]/2 - w/2, resolution[1]/2 - h/2 + h + 20 * resizeFactor))

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
			game.score += 1

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
			if keys[pg.K_r] and game.gameOver:
				game = Game(screen, Snake())
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
