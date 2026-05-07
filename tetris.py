import sys
import random
import pygame

# Tetris - simple clone using Pygame
# Controls:
# Left  - move left
# Right - move right
# Up    - rotate
# Space - hard drop
# P     - pause / resume
# R     - restart

CELL_SIZE = 30
COLUMNS = 10
ROWS = 20
WIDTH = CELL_SIZE * COLUMNS
HEIGHT = CELL_SIZE * ROWS
FPS = 60

# Colors
BLACK = (0, 0, 0)
GRAY = (40, 40, 40)
WHITE = (255, 255, 255)
BASE_COLORS = [
	(0, 240, 240),  # I
	(0, 0, 240),    # J
	(240, 160, 0),  # L
	(240, 240, 0),  # O
	(0, 240, 0),    # S
	(160, 0, 240),  # T
	(240, 0, 0),    # Z
]


def darken(color, factor=0.45):
	return tuple(max(0, int(c * factor)) for c in color)


# Theme definitions
THEMES = {
	'dark': {
		'bg': (0, 0, 0),
		'grid': (40, 40, 40),
		'colors': BASE_COLORS,
	},
	'light': {
		'bg': (245, 245, 245),
		'grid': (200, 200, 200),
		# use darker variants of base colors for contrast on light background
		'colors': [darken(c, 0.35) for c in BASE_COLORS],
	},
}

# Default theme
DEFAULT_THEME = 'dark'

# Shapes (matrices)
SHAPES = [
	[[1, 1, 1, 1]],
	[[1, 0, 0], [1, 1, 1]],
	[[0, 0, 1], [1, 1, 1]],
	[[1, 1], [1, 1]],
	[[0, 1, 1], [1, 1, 0]],
	[[0, 1, 0], [1, 1, 1]],
	[[1, 1, 0], [0, 1, 1]],
]


def rotate(shape):
	# rotate clockwise
	return [list(row) for row in zip(*shape[::-1])]


class Piece:
	def __init__(self, shape, color_index):
		self.shape = shape
		self.color_index = color_index
		self.x = COLUMNS // 2 - len(shape[0]) // 2
		self.y = 0

	def rotate(self):
		self.shape = rotate(self.shape)


class Tetris:
	def __init__(self):
		# grid stores None for empty, or an integer color index for filled cells
		self.grid = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
		self.score = 0
		self.level = 1
		self.lines = 0
		self.current = self.next_piece()
		self.next = self.next_piece()
		self.game_over = False
		self.paused = False
		self.theme = DEFAULT_THEME

	def next_piece(self):
		idx = random.randrange(len(SHAPES))
		return Piece([row[:] for row in SHAPES[idx]], idx)

	def valid_position(self, piece, adj_x=0, adj_y=0):
		for r, row in enumerate(piece.shape):
			for c, cell in enumerate(row):
				if not cell:
					continue
				x = piece.x + c + adj_x
				y = piece.y + r + adj_y
				if x < 0 or x >= COLUMNS or y >= ROWS:
					return False
				if y >= 0 and self.grid[y][x] is not None:
					return False
		return True

	def lock_piece(self):
		p = self.current
		for r, row in enumerate(p.shape):
			for c, cell in enumerate(row):
				if not cell:
					continue
				x = p.x + c
				y = p.y + r
				if 0 <= y < ROWS and 0 <= x < COLUMNS:
					self.grid[y][x] = p.color_index
		self.clear_lines()
		self.current = self.next
		self.next = self.next_piece()
		if not self.valid_position(self.current):
			self.game_over = True

	def clear_lines(self):
		new_grid = []
		removed = 0
		for row in self.grid:
			if all(cell is not None for cell in row):
				removed += 1
			else:
				new_grid.append(row)
		for _ in range(removed):
			new_grid.insert(0, [None for _ in range(COLUMNS)])
		self.grid = new_grid
		if removed > 0:
			self.lines += removed
			self.score += (removed * 100) * self.level
			self.level = 1 + self.lines // 10

	def toggle_theme(self):
		self.theme = 'light' if self.theme == 'dark' else 'dark'

	def toggle_pause(self):
		if not self.game_over:
			self.paused = not self.paused


def draw_grid(surface, grid, theme):
	theme_data = THEMES[theme]
	bg = theme_data['bg']
	grid_color = theme_data['grid']
	colors = theme_data['colors']
	for y in range(ROWS):
		for x in range(COLUMNS):
			rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
			cell = grid[y][x]
			if cell is None:
				pygame.draw.rect(surface, bg, rect)
			else:
				pygame.draw.rect(surface, colors[cell], rect)
			pygame.draw.rect(surface, grid_color, rect, 1)


def draw_piece(surface, piece, theme):
	colors = THEMES[theme]['colors']
	grid_color = THEMES[theme]['grid']
	for r, row in enumerate(piece.shape):
		for c, cell in enumerate(row):
			if not cell:
				continue
			x = (piece.x + c) * CELL_SIZE
			y = (piece.y + r) * CELL_SIZE
			rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
			pygame.draw.rect(surface, colors[piece.color_index], rect)
			pygame.draw.rect(surface, grid_color, rect, 1)


def main():
	try:
		pygame.init()
	except Exception:
		print("Pygame is required to run this game. Install with: pip install pygame")
		sys.exit(1)

	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Tetris')
	clock = pygame.time.Clock()

	game = Tetris()

	fall_speed = 700  # milliseconds per cell at level 1
	fall_timer = 0

	running = True
	while running:
		dt = clock.tick(FPS)
		fall_timer += dt

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					game = Tetris()
					fall_timer = 0
					continue
				if game.game_over:
					continue
				if event.key == pygame.K_p:
					game.toggle_pause()
					continue
				if game.paused:
					continue
				if event.key == pygame.K_m:
					game.toggle_theme()
					continue
				if event.key == pygame.K_LEFT:
					if game.valid_position(game.current, adj_x=-1):
						game.current.x -= 1
				elif event.key == pygame.K_RIGHT:
					if game.valid_position(game.current, adj_x=1):
						game.current.x += 1
				elif event.key == pygame.K_UP:
					# rotate with wall kick attempt
					old_shape = game.current.shape
					game.current.rotate()
					if not game.valid_position(game.current):
						# try kicks
						if game.valid_position(game.current, adj_x=-1):
							game.current.x -= 1
						elif game.valid_position(game.current, adj_x=1):
							game.current.x += 1
						else:
							game.current.shape = old_shape
				elif event.key == pygame.K_SPACE:
					# hard drop
					while game.valid_position(game.current, adj_y=1):
						game.current.y += 1
					game.lock_piece()

		if not game.game_over and not game.paused:
			# gravity based on level
			level_speed = max(100, fall_speed - (game.level - 1) * 50)
			if fall_timer >= level_speed:
				fall_timer = 0
				if game.valid_position(game.current, adj_y=1):
					game.current.y += 1
				else:
					game.lock_piece()

		# draw according to current theme
		theme_data = THEMES[game.theme]
		screen.fill(theme_data['bg'])
		draw_grid(screen, game.grid, game.theme)
		if not game.game_over:
			draw_piece(screen, game.current, game.theme)

		# UI: score only
		font = pygame.font.SysFont('Consolas', 18)
		ui_color = WHITE if game.theme == 'dark' else (30, 30, 30)
		score_surf = font.render(f'Score: {game.score}', True, ui_color)
		screen.blit(score_surf, (5, 5))

		if game.game_over:
			go_font = pygame.font.SysFont('Consolas', 48)
			go_surf = go_font.render('GAME OVER', True, WHITE)
			rect = go_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
			screen.blit(go_surf, rect)
			restart_font = pygame.font.SysFont('Consolas', 22)
			restart_surf = restart_font.render('Press R to Restart', True, WHITE)
			restart_rect = restart_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
			screen.blit(restart_surf, restart_rect)

		if game.paused:
			pause_font = pygame.font.SysFont('Consolas', 48)
			pause_surf = pause_font.render('PAUSED', True, WHITE)
			pause_rect = pause_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
			screen.blit(pause_surf, pause_rect)

		pygame.display.flip()

	pygame.quit()


if __name__ == '__main__':
	main()

