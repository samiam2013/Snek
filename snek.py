import time, pygame
from random import randint

#for some reason you have to start modules? whatever. 
pygame.init()

#can't make the numbers unequal? TODO: FIX THIS
blocks_square = 30

#height and width based on num blocks
blocks_height = blocks_square
blocks_width = blocks_square

#block width and padding in pixels
block_size = 15
padding = 0

#canvas size calculation
c_height = (blocks_height * (block_size + padding)) + padding
c_width = (blocks_width * (block_size + padding)) + padding

#speed settings
speed = 50 # -infinity to +133
full_speed = 0.05
crawl_speed = .2

#Wait time computation
speed = float(speed)
speed_width = -1 * (full_speed - crawl_speed)
#print "speed_width: ",speed_width
speed_coef = speed / 100
#print "speed coefficient:",speed_coef
speed_dif = speed_width * speed_coef
#print "speed difference:",speed_dif
wait_time = crawl_speed - speed_dif

screen = pygame.display.set_mode((c_width, c_height))


def reset_bg(color=(255,255,255)):
	screen.fill(color)
	
def make_grid(height,width,block_size,padding):
	grid = [[None for x in range(blocks_width)] for y in range(blocks_height)]
	for h_pos in range(blocks_height):
		y_pos = (h_pos * (block_size + padding)) + padding
		top = y_pos
		for w_pos in range(blocks_height):
			x_pos = (w_pos * (block_size + padding)) + padding
			left = x_pos
			grid[h_pos][w_pos] = pygame.Rect(left,top,block_size,block_size)
	return grid

# pygame.Rect(left,top,width,height)
def draw_grid(grid,screen):
	bg_block_color = (0,255,0)
	for row in grid: #h_pos
		for rect_obj in row:
			pygame.draw.rect(screen,bg_block_color,rect_obj)

def make_goal(grid, snek):
	max_x = len(grid[0]) - 1
	max_y = len(grid) - 1
	while True:
		x = randint(0,max_x)
		y = randint(0,max_y)
		if((x,y) in snek):
			print "cannot make goal there, in snek!"
			continue
		else:
			print "new goal!:",x,",",y
			return (x,y)

def move_snek(grid,snek,dir_key_code,old_key_code):
	#print "snek recieved in move_snek:",snek
	#get the pop for when the snake eats an egg
	head_val = snek[len(snek)-1]
	pop = snek.pop(0)
	if dir_key_code == 273: #up
		new_val = (head_val[0]-1,head_val[1])
	elif dir_key_code == 274: #down
		new_val = (head_val[0]+1,head_val[1])
	elif dir_key_code == 276: #left
		new_val = (head_val[0],head_val[1]-1)
	elif dir_key_code == 275: #right
		new_val = (head_val[0],head_val[1]+1)
	else:
		print "NOT A VALID dir_key_code in move_snek():",dir_key_code
		return False,False
	#make sure the new value is still on the grid
	on_grid = False
	if 0 <= new_val[0] <= len(grid)-1:
		if 0 <= new_val[1] <= len(grid[0])-1:
			on_grid = True
		else: 
			print "new_val[1]:",new_val[1]," INVALID!"
	else:
		print "new_val[0]:",new_val[0]," INVALID!"
	#make sure the new value isn't already part of the snek
	if on_grid and (new_val not in snek):
		snek.append(new_val)
		#print "new snek in move_snek:",snek
		return snek,pop
	else: 
		return False

def draw_snek(snek,grid,screen):
	snek_color = (0,128,0)
	#print "SNEK IN draw_snek:",snek
	for tup in snek:
		pygame.draw.rect(screen,snek_color,grid[tup[0]][tup[1]])

def draw_goal(goal,grid,screen):
	goal_color = (176,0,0)
	pygame.draw.rect(screen,goal_color,grid[goal[0]][goal[1]])

#make grid for this to go on
grid = make_grid(blocks_height,blocks_width,block_size,padding)
#snek is list where pop() and append() drive movement
snek = [make_goal(grid,[])]
#make random goal (snake position excluded)
goal = make_goal(grid,snek)
print "goal x:",goal[0],",y:",goal[1]
#set the initial direction

#set up the initial window before starting with an initial direction
reset_bg()
draw_snek(snek,grid,screen)
draw_goal(goal,grid,screen)
pygame.display.update()

#get an initial direction from the user
# up == key 273, down == 274, left == 276, right == 275
got_direction = False
while True:
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.KEYDOWN and 276 >= event.key >= 273:
			dir_key_code = event.key
			got_direction = True
			break
	if got_direction:
		break

#have to know the last direction so we can ignore the opposite key
old_key_code = dir_key_code

#have to instantiate goal_hit
goal_hit = False
done = False

#while true keep game running
while True:
	#hesitate here for input
	time.sleep(wait_time)
	#check direction change
	old_key_code = dir_key_code
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.KEYDOWN and 276 >= event.key >= 273:
			dir_key_code = event.key
			break
		if event.type == pygame.QUIT:
			done = True
	if done == True: 
		break
	#reset the background
	reset_bg()
	#draw the grid on
	#draw_grid(grid,screen)
	
	#move the snek in direction (make sure to hold onto pop() value)
	snek,pop = move_snek(grid,snek,dir_key_code,old_key_code)
	#if snek out of bounds or eats self (as rpsnt by False, end game
	if snek == False:
		print "INVALID MOVEMENT"
		time.sleep(10)
		break
	#if goal in snake, 
	if goal in snek:
		if goal_hit == False:
			# add 1 to end of snake (pop() value from earlier)
			snek = [pop] + snek[:]
			#snek = snek[:] + [pop]
			#  set a new goal
			goal = make_goal(grid,snek)
			goal_hit = True
	elif goal_hit == True:
		goal_hit = False
	#draw snek
	draw_snek(snek,grid,screen)
	#draw goal
	draw_goal(goal,grid,screen)
	#render, bro.
	pygame.display.update()
