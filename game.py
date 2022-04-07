# https://inventwithpython.com/pygame/chapter3.html

from pickle import NONE
import pygame, sys, random
from pygame.locals import *
from pygame.sprite import LayeredUpdates
from word_check import *
from setting import *
import colors
from alphabets import alph_cards
from win_images import win_images
from card import Card
from cell import *


# Rects #
# center pane (Surface)
cp_width, cp_height = 400, 200
cp_topleft = (200, 200)
pane_color = (255,248,220)

# 3 plates (Surface)
plate0_topleft = (220, 450)
plate1_topleft = (440, 60)
plate2_topleft = (80, 60)
plate0_width, plate0_height = 360, 100
plate12_width, plate12_height = 280, 80
plate_color = (255,228,181)

# "Complete" / "Word doesn't exist" msg: Player0, Player2, Player1
msg_sign_rects = [
		(plate0_topleft[0]+plate0_width+5, plate0_topleft[1]+plate0_height),
		(plate1_topleft[0]+plate12_width+5, plate1_topleft[1]+plate12_height),
		(plate2_topleft[0]+plate12_width+5, plate2_topleft[1]+plate12_height)
	]

# 'TURN' & 'PASS', 'PLEASE', 'SUGGEST' signs
turn_sign_rects = [(400, 570), (580, 40), (220, 40)]
option_sign_rects = [
		(WINDOWWIDTH - (WINDOWWIDTH-cp_width)//4, WINDOWHEIGHT//2),			# 'PASS'
		(WINDOWWIDTH - (WINDOWWIDTH-cp_width)//4, plate0_topleft[1] + 20),	# 'PLEASE'
		(WINDOWWIDTH - (WINDOWWIDTH-cp_width)//4, plate0_topleft[1] + 50)	# 'SUGGEST'
	]


# create Surface objects
center_pane = pygame.Surface((cp_width, cp_height), 2)
center_pane.fill(pane_color)

plate0 = pygame.Surface((plate0_width, plate0_height))
plate0.fill(plate_color)
plate1 = pygame.Surface((plate12_width, plate12_height))
plate1.fill(plate_color)
plate2 = pygame.Surface((plate12_width, plate12_height))
plate2.fill(plate_color)

# PLATES #
# min & max number of cells placed in each plate

min_cell = 3
max_cell = 5

# draw a random number of cells in each player's plate
def draw_cells():
	global all_cell_group, cell_group0, cell_group1, cell_group2, cell_groups

	cell_bdcolor = (184,134,11)
	all_cell_group = pygame.sprite.Group()

	# plate0
	# draw_cells_on_plate(min_cell, max_cell, plate0_topleft, plate0_width, DISPLAYSURF, bdcolor=cell_bdcolor, parent_group=all_cell_group)

	cell_group0 = pygame.sprite.LayeredUpdates()
	number = random.randint(min_cell, max_cell)
	print("number of cells in plate0: ", number)
	total_width = 40*number + 5*(number-1)
	x, y = plate0_topleft[0]+(plate0_width - total_width)//2, plate0_topleft[1]+30
	for _ in range(number):
		c = Cell(DISPLAYSURF, cell_bdcolor, Rect(x, y, CELLSIZE, CELLSIZE))
		cell_group0.add(c)
		all_cell_group.add(c)
		x += 45

	# plate1
	cell_group1 = pygame.sprite.LayeredUpdates()
	number = random.randint(min_cell, max_cell)
	print("number of cells in plate1: ", number)
	total_width = 40*number + 3*(number-1)
	x, y = plate1_topleft[0]+(plate12_width - total_width)//2, plate1_topleft[1]+(plate12_height-CELLSIZE)//2
	for _ in range(number):
		c = Cell(DISPLAYSURF, cell_bdcolor, Rect(x, y, CELLSIZE, CELLSIZE))
		cell_group1.add(c)
		all_cell_group.add(c)		
		c.draw()
		x += 43

	# plate2
	cell_group2 = pygame.sprite.LayeredUpdates()
	number = random.randint(min_cell, max_cell)
	print("number of cells in plate2: ", number)
	total_width = 40*number + 3*(number-1)
	x, y = plate2_topleft[0]+(plate12_width - total_width)//2, plate1_topleft[1]+(plate12_height-CELLSIZE)//2
	for _ in range(number):
		c = Cell(DISPLAYSURF, cell_bdcolor, Rect(x, y, CELLSIZE, CELLSIZE))
		cell_group2.add(c)
		all_cell_group.add(c)		
		c.draw()
		x += 43

	# used to determine the cell group the cards can go to in each turn
	cell_groups = [cell_group0, cell_group1, cell_group2]


# CARDS IN THE CENTER PANE #
# position of each card (3 x 8) in the center pane
cp_card_rects = [
	(40, 35), (80, 35), (120, 35), (160, 35), (200, 35), (240, 35), (280, 35), (320, 35), 
	(40, 85), (80, 85), (120, 85), (160, 85), (200, 85), (240, 85), (280, 85), (320, 85), 
	(40, 135), (80, 135), (120, 135), (160, 135), (200, 135), (240, 135), (280, 135), (320, 135)
	]

# position of each card in DISPLAYSURF
card_rects = [(x + cp_topleft[0], y + cp_topleft[1]) for (x, y) in cp_card_rects] 

# places the initial set of the alphabet cads in center pane
def initial_cards(cards):
	global card_group
	card_group = pygame.sprite.LayeredUpdates()
	i = 0

	# print(card_rects)
	for alphabet, card in cards:
		# make each card image into a Card object
		obj = Card(card, card_rects[i])
		obj.alphabet = alphabet
		card_group.add(obj)
		obj.draw(DISPLAYSURF)
		i += 1

	# print("card_group:", card_group)

# create the Surface and Rect objects for a text
def make_text(text, color, rect, fsize=BASICFONTSIZE, align="center", bgcolor=None):
	text_surf = pygame.font.Font(BASICFONT, fsize).render(text, True, color, bgcolor)
	text_rect = text_surf.get_rect()
	if align == "left":
		text_rect.topleft = (rect)
	elif align == "right":
		text_rect.topright = (rect)
	else:
		text_rect.center = (rect)
	return (text_surf, text_rect)


# check if the current plate is complete
def is_plate_complete(turn):
	global msg_sign_surf, msg_sign_rect
	word = []
	for cell in cell_groups[turn%3]:
		if cell.card:
			word.append(cell.card.alphabet)
		else:
			print("Word not complete yet")
			break

	# check if the completed word exists in the dictionary
	if len(word) == len(cell_groups[turn%3].sprites()):
		word = "".join(word)
		if check_word(word):
			print(word, "--> Complete!")						
			plate_completed[turn%3] = 1
		else:
			msg_sign_surf, msg_sign_rect = make_text("The word does not exist.", TEXTCOLOR_NG, msg_sign_rects[turn%3], fsize=15, align="right")
			print(word, "--> The word does not exist.")
			print(msg_sign_surf)
			plate_completed[turn%3] = 0


# ===== MAIN ========================

def main():
	global FPSCLOCK, DISPLAYSURF, plate_completed, running, moving, msg_sign_surf, msg_sign_rect

	# initializing imported module
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	DISPLAYSURF.fill(BGCOLOR)
	pygame.display.set_caption(TITLE)

	# draws a random number of cells in each plate
	draw_cells()

	# places initial cards
	initial_cards(alph_cards)

	# Whose turn
	turn = 0
	
	# if plates are complete
	plate_completed = [0, 0, 0]	# plate0, plate1, plate2

	# Surface for the message shown when cells are filled
	msg_sign_surf = None
	
	game_completed = False
	running = True
	moving = False	# no the mouse, but the card

	while running:

		# Check for event if user has pushed any event in queue
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				running = False
				pygame.quit()

			elif event.type == MOUSEBUTTONDOWN:
				for card in card_group:
					initial_posx = card.rect.left
					initial_posy = card.rect.top
					x, y = event.pos
					if card.rect.collidepoint((x, y)):
						# bring the selected card on top of other cards
						card_group.move_to_front(card)
							# cursor_layer = 2
							# card_group.change_layer(card, cursor_layer)
						print("Selected card is:", card.alphabet, "at layer:", card.layer, "at rect: ", card.rect)

						moving = True
						break

			elif event.type == MOUSEMOTION and moving:
				card.rect.move_ip(event.rel)

				# if the card center is inside a cell, switch the cell on
				for cell in cell_groups[turn%3]:
					if cell.rect.collidepoint(card.rect.center):
						cell.switch(1)
						card.is_in_cell = True
						break
					else:
						cell.switch(0)
						card.is_in_cell = False

			elif event.type == MOUSEBUTTONUP:
				if moving:
					if card.is_in_cell:

						for cell in cell_groups[turn%3]:
							# if the cell already has a card on it, replace it with the new one
							if cell.has_thecard:
								if cell.card:
									replaced_card = cell.card
									replaced_card.rect.update(initial_posx, initial_posy, CARDSIZE, CARDSIZE)
									card.rect.update(cell.rect.x +5, cell.rect.y +5, CARDSIZE, CARDSIZE)
									cell.card = card
									print(cell.card.alphabet, "replaced", replaced_card.alphabet)
								else:									
									cell.card = card
									card.rect.update(cell.rect.x +5, cell.rect.y +5, CARDSIZE, CARDSIZE)

						replaced_card = None

						# check if the plate is complete
						is_plate_complete(turn)

						turn += 1

					# if the card center is not inside a cell when MOUSEBUTTONUP, return the card to its original position
					else:
						card.rect.update(initial_posx, initial_posy, CARDSIZE, CARDSIZE)
					moving = False

				# 'PASS' when you don't want to change your completed plate
				elif plate_completed[turn%3]:
					if pass_sign_rect.collidepoint(event.pos):
						turn += 1
				else:
					pass

				pygame.time.delay(2)


		DISPLAYSURF.fill(BGCOLOR)
		DISPLAYSURF.blit(center_pane, cp_topleft)
		DISPLAYSURF.blit(plate0, plate0_topleft)
		DISPLAYSURF.blit(plate1, plate1_topleft)
		DISPLAYSURF.blit(plate2, plate2_topleft)

		for cell in cell_group0:
			cell.draw()

		for cell in cell_group1:
			cell.draw()

		for cell in cell_group2:
			cell.draw()

		for card in card_group:
			card.draw(DISPLAYSURF)

		# SHOW TEXTS #
		# if all the plate are complete, express congrats and pause the game
		if plate_completed == [1,1,1]:
			for image in win_images:
				image_rect = image.get_rect()
				image_rect.center = (WINDOWWIDTH//2, WINDOWHEIGHT//2)
				DISPLAYSURF.blit(image, image_rect)
				pygame.time.wait(FPS)
				pygame.display.update()

			# (for showing 'New Game' message)
			# newgame_surf, newgame_rect = make_text("New Game?", BUTTONTEXTCOLOR, (WINDOWWIDTH//2, WINDOWHEIGHT//2), fsize=30, bgcolor=BGCOLOR)
			# DISPLAYSURF.blit(newgame_surf, newgame_rect)

			game_completed = True

		else:
			for idx, plate in enumerate(plate_completed):
				if plate:
					complete_sign_surf, complete_sign_rect = make_text("Complete!", TEXTCOLOR_OK, msg_sign_rects[idx], fsize=15, align="right")
					DISPLAYSURF.blit(complete_sign_surf, complete_sign_rect)

					if idx == turn%3:
						# create 'PASS' sign Surface/Rect
						pass_sign_surf, pass_sign_rect = make_text("PASS", colors.WHITE, option_sign_rects[0], bgcolor=colors.GREEN)
						DISPLAYSURF.blit(pass_sign_surf, pass_sign_rect)
		
		# "Word doesn't exist" msg
		if msg_sign_surf:
			DISPLAYSURF.blit(msg_sign_surf, msg_sign_rect)

		# 'TURN' sign
		turn_sign_surf, turn_sign_rect = make_text("TURN", colors.RED, turn_sign_rects[turn%3])
		DISPLAYSURF.blit(turn_sign_surf, turn_sign_rect)

		# How many turns passed (omittable)
		turn_text = "Turn: " + str(turn)
		turn_number_surf, turn_number_rect = make_text(turn_text, colors.BLACK, (30,10), fsize=10)
		DISPLAYSURF.blit(turn_number_surf, turn_number_rect)

		# 'PLEASE'/'SUGGEST' sign for Player0's turn (ad hoc)
		if (turn > 2 and turn%3 == 0 and not plate_completed[0]):
			please_sign_surf, please_sign_rect = make_text("PLEASE", colors.WHITE, option_sign_rects[1], fsize=15, bgcolor=colors.ORANGE)
			DISPLAYSURF.blit(please_sign_surf, please_sign_rect)

		elif (turn > 3 and turn%3 != 0 and not plate_completed[turn%3]):
			suggest_sign_surf, suggest_sign_rect = make_text("SUGGEST", colors.WHITE, option_sign_rects[2], fsize=15, bgcolor=colors.ORANGE)
			DISPLAYSURF.blit(suggest_sign_surf, suggest_sign_rect)
		
		pygame.display.update()

	pygame.quit()
	quit()


if __name__ == '__main__':
	main()
