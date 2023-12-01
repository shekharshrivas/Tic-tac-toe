import sys  # this is going to helps for quiting the application.
import pygame
import numpy as np
import random
import copy

from Constants import *

pygame.init()   # this for initializing model 

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAK TOE AI') 
screen.fill(Backgroundcolour)


class Board:

	def __init__(self):
		self.squares = np.zeros((ROWS, COLS))
		self.empty_sqrs = self.squares #[squares]
		self.marked_sqrs = 0

	def final_state(self, show = False):
		""" return 0 if there is no win yet it doesn't mean there is a draw;
			return 1 if player 1 is wins
			return 2 if player 2 is wins 
		"""
		# vertical wins
		for col in range(COLS):
			if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
				if show:
					color = (255, 0, 0)
					iPos = (col * SQsize + SQsize//2, 20)
					fPos = (col * SQsize + SQsize//2, HEIGHT - 20)
					pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
				return self.squares[0][col]

		# horizontal wins
		for row in range(ROWS):
			if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
				if show:
					color = (255, 0, 0)
					iPos = (20, row * SQsize + SQsize//2)
					fPos = (WIDTH - 20, row * SQsize + SQsize//2)
					pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
				return self.squares[row][0]

		# desc diagonal wins
		if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
			if show:
				color = (255, 0, 0)
				iPos = (20, 20)
				fPos = (WIDTH - 20, HEIGHT - 20)
				pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
			return self.squares[1][1]

		# asc diagonal wins
		if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
			if show:
				color = (255, 0, 0)
				iPos = (20, HEIGHT - 20)
				fPos = (WIDTH - 20, 20)
				pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
			return self.squares[1][1]

		# no win yet
		return 0


	def mark_sqr(self, row, col, player):
		self.squares[row][col] = player
		self.marked_sqrs += 1 # help in when our board is full


	def empty_sqr(self, row, col):
		return self.squares[row][col] == 0

	def get_empty_sqrs(self):
		empty_sqrs = []
		for row in range(ROWS):
			for col in range(COLS):
				if self.empty_sqr(row, col):
					empty_sqrs.append((row, col))
		return empty_sqrs

	def isfull(self):
		return self.marked_sqrs == 9

	def isempty(self):
		return self.marked_sqrs == 0


class AI:
	def __init__(self, level = 1, player = 2): # level 0 means random ai play or 1 means minimax ai play
		self.level = level
		self.player = player

	def rnd(self, board): # random choice
		empty_sqra = board.get_empty_sqrs()
		idx = random.randrange(0, len(empty_sqra))

		return empty_sqra[idx] # (row, col)

	def minimax(self,board, maximizing):
		# terminal case
		case = board.final_state()

		# player 1 wins
		if case == 1:
			return 1, None # eval, move

		# player 2 wins
		if case == 2:
			return -1, None

		# draw
		elif board.isfull():
			return 0, None

		if maximizing:
			max_eval = -100  # this can be any no greater than 1, -1, or 0
			best_move = None
			empty_sqrs = board.get_empty_sqrs()

			for (row, col) in empty_sqrs:
				temp_board = copy.deepcopy(board)
				temp_board.mark_sqr(row, col, 1)
				eval = self.minimax(temp_board, False)[0]
				if eval > max_eval:
					max_eval = eval
					best_move = (row, col)
			return max_eval, best_move

		elif not maximizing:  # this is for AI
			min_eval = 100  # this can be any no greater than 1, -1, or 0
			best_move = None
			empty_sqrs = board.get_empty_sqrs()

			for (row, col) in empty_sqrs:
				temp_board = copy.deepcopy(board)
				temp_board.mark_sqr(row, col, self.player)
				eval = self.minimax(temp_board, True)[0]
				if eval < min_eval:
					min_eval = eval
					best_move = (row, col)
			return min_eval, best_move



	def eval(self, main_board):
		if self.level == 0:
			# random choice
			eval = "random"
			move = self.rnd(main_board)

		else:
			# minimax algo choice
			eval, move = self.minimax(main_board, False) # in this case is going to minimize

		print(f"AI has chosen to mark the square in pos {move} with an eval of: {eval}")
		return move # (row, col)

class Game:

	def __init__(self):
		self.board = Board()
		self.ai = AI()
		self.player = 1			# 1 - cross # 2 - circle
		self.gamemode = "ai" # pvp or ai
		self.running = True  # if the game is running no one wins yet or not a draw
		self.show_lines()

	def make_move(self, row, col):
		self.board.mark_sqr(row, col, self.player)
		self.draw_fig(row, col)
		self.next_turn()


	def show_lines(self):
		# bg
		screen.fill(Backgroundcolour)
		# Vertical line
		pygame.draw.line(screen, LINE_COLOR, (SQsize, 0), (SQsize, HEIGHT), LINE_WIDTH)
		pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQsize, 0), (WIDTH - SQsize, HEIGHT), LINE_WIDTH)

		# Horizontal line
		pygame.draw.line(screen, LINE_COLOR, (0, SQsize), (WIDTH, SQsize), LINE_WIDTH)
		pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQsize), (WIDTH, HEIGHT - SQsize), LINE_WIDTH)


	def draw_fig(self, row, col):
		if self.player == 1:
			# draw cross
			# descending line
			start_desc = (col * SQsize + OFFSET, row * SQsize + OFFSET)
			end_desc = (col * SQsize + SQsize - OFFSET, row * SQsize + SQsize - OFFSET)
			pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
			# ascending line
			start_asc = (col * SQsize + OFFSET, row * SQsize + SQsize - OFFSET)
			end_asc = (col * SQsize + SQsize - OFFSET, row * SQsize + OFFSET)
			pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

		elif self.player == 2:
			#draw circle
			center = (col * SQsize + SQsize // 2, row * SQsize + SQsize // 2)
			pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)


	def next_turn(self):
		self.player = self.player % 2 + 1

	def change_gamemode(self):
		self.gamemode = "ai" if self.gamemode == "pvp" else "pvp"

	def reset(self):
		self.__init__()

	def isover(self):
		return self.board.final_state(show = True) != 0 or self.board.isfull()





def main():

	# game object
	game = Game()
	board = game.board
	ai = game.ai
	# mainloop
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			# if event.type == pygame.MOUSEBUTTONDOWN:
			# 	pos = event.pos
			# 	row = pos[1] // SQsize	# y-axis 
			# 	col = pos[0] // SQsize	# x-axis

			# 	if board.empty_sqr(row, col):
			# 		game.make_move(row, col)
			# 		# print(board.squares)

			if event.type == pygame.KEYDOWN:
				# g-gamemode
				if event.key == pygame.K_g:
					game.change_gamemode()

				# r-reset
				if event.key == pygame.K_r:
					game.reset()
					board = game.board
					ai = game.ai


				# 0-random ai
				if event.key == pygame.K_0:
					ai.level = 0

				# 1-minimax ai
				if event.key == pygame.K_1:
					ai.level = 1

			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = event.pos
				row = pos[1] // SQsize	# y-axis 
				col = pos[0] // SQsize	# x-axis

				if board.empty_sqr(row, col) and game.running:
					game.make_move(row, col)
					# print(board.squares)
					if game.isover():
						game.running = False

		if game.gamemode == "ai" and game.player == ai.player and game.running:
			# update the screen
			pygame.display.update()

			# ai methods
			row, col = ai.eval(board)
			game.make_move(row, col)
			if game.isover():
				game.running = False

		pygame.display.update()


main()