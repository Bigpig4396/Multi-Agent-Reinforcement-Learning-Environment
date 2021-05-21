#! /usr/bin/env python3

'''
Random Maze Generator
Makes use of a radomized version of Kruskal's Minimum Spanning Tree (MST) 
algorithm to generate a randomized mazes!
	@author: Paul Miller (github.com/138paulmiller)
'''
import numpy as np
import os, sys, random, time, threading
# defined in disjointSet.py
import disjointSet as ds

class Maze:
	# static variables
	# Directions to move the player. 
	# Note, up and down are reversed (visual up and down not grid coordinates)	
	UP = (0, -1)
	DOWN = (0, 1)
	LEFT = (-1, 0)
	RIGHT = (1,0)

	def __init__(self, width, height, seed, symbols, scaling):
		'''
		Default constructor to create an widthXheight maze
		@params 
			width(int)	: number of columns
			height(int)	: number of rows
			seed(float)	: number to seed RNG
			symbols(dict)	: used to modify maze symbols and colors
							settings{
								start, end, start_color, end_color, : start and end symbols and colors
								wall_v, wall_h, wall_c, wall_color, : vertical,horizontal and corner wall symbols and colors 
								head, tail, head_color, tail_color   : player head and trail symbols and colors
								*_bg_color, : substitute _color with bg_color to set background colors 
		@return												
			Maze	: constructed object
		'''
		assert width > 0; assert height > 0
		self.init_symbols(symbols)
		self.time_taken = False
		self.timer_thread = None
		self.is_moving = True # used as a semaphore for the update time thread
		self.width = width
		self.height = height
		self.seed = seed
		self.scaling = scaling
		self.path = [] # current path taken
		self.player = (0,0) # players position
		# self.items = [(x,y)] #TODO?? Add a list of possible items to collect for points?
        # Creates 2-D array of cells(unique keys)
		# Grid is 2-D, and the unique ids are sequential, i
		# so uses a 2-D to 1-D mapping
		# to get the key since row+col is not unique for all rows and columns
		#	E.g.
		#	width = 5
		#			1-D Mapping	vs  	Naive
		#	grid[2][3] = 	5*2+3 = 13 	vs  	2+3 = 6
		#	grid[3][2] =	5*3+2 = 17	vs 	3+2 = 6 X Not unique! 
		# use 2D list comprehensions to avoid iterating twice
		self.grid = [[(width*row + col) \
			for row in range(0,height)]\
				for col in range(0, width)]
		# portals[key] = {keys of neighbors}
		self.portals = {}
		# generate the maze by using a kruskals algorithm 
		self.kruskalize()	
	

	def __repr__(self):
		'''
		Allows for print(maze)
		@params
			None
		@return
			String : Ascii representation of the Maze
		'''
		return self.to_str()

	def to_str(self):
		'''
		Defines the string representation of the maze.
		@return
			Maze	: constructed object
		'''	
		s=''
		for col in range(0, self.width):
			s+=self.wall_c + self.wall_h
		
		s+=self.wall_c+'\n'
		# wall if region not the same	
		for row in range(0,self.height):	
			# draw S for start if at (0,0)
			if row == 0:
				s+=self.wall_v + self.start
			else:
				s+=self.wall_v + self.empty	
	
			# draw | if no portal between [row][col] and [row][col-1]	
			for col in range(1, self.width): 	
				# if  theres a portal between cell and left cell
				if self.grid[col-1][row] in self.portals[self.grid[col][row]]:
					# if portal remove wall
					c = self.empty
				else:
					# if not portal draw vertical wall
					c = self.wall_v
				# if at [width-1][height-1] draw end marker or cell
				if row == self.height-1 and col == self.width-1:
					c += self.end	
				else: # draw cell
					c += self.empty				
				s += c 	
			s+=self.wall_v +'\n'
			# draw - if not portal between [row][col] and [row+1][col]
			for col in range(0, self.width):
				# if edge above (visually below)
				c =self.wall_h
				key = self.grid[col][row]	
				# if not at last row, and theres a portal between cell and above cell
				if row+1 < self.height and self.grid[col][row+1] in self.portals[key]:
						c = self.empty
				s+=self.wall_c + c
			s+=self.wall_c +'\n'
		s+=self.empty
		return s

	def to_np(self):
		s = np.zeros((2*self.height+1, 2*self.width+1), dtype=np.int)
		print(s.shape)
		for col in range(0, 2*self.width+1):
			s[0][col] = 1
		for row in range(0, self.height):
			s[2*row + 1][0] = 1
			s[2*row + 1][1] = 0
			for col in range(1, self.width):
				if self.grid[col-1][row] in self.portals[self.grid[col][row]]:
					# if portal remove wall
					s[2*row+1][2*col] = 0
				else:
					# if not portal draw vertical wall
					s[2*row+1][2*col] = 1
				# if at [width-1][height-1] draw end marker or cell
				if row == self.height-1 and col == self.width-1:
					s[2*row+1][2*col+1] = 0
			s[2*row+1][2*self.width] = 1
			for col in range(0, self.width):
				# if edge above (visually below)
				c = 1
				key = self.grid[col][row]
				# if not at last row, and theres a portal between cell and above cell
				if row+1 < self.height and self.grid[col][row+1] in self.portals[key]:
						c = 0
				s[2*row+2][2*col] = 1
				if c == 1:
					s[2 * row + 2][2 * col + 1] = 1
				else:
					s[2 * row + 2][2 * col + 1] = 0
			s[2*row+2][-1] = 1
		return s

	def scale(self, map_np):
		new_map_np = np.zeros((self.scaling * map_np.shape[0], self.scaling * map_np.shape[1]))
		for i in range(map_np.shape[0]):
			for j in range(map_np.shape[1]):
				if map_np[i][j] == 1:
					for k in range(self.scaling):
						for l in range(self.scaling):
							new_map_np[self.scaling * i + k][self.scaling * j + l] = 1
				else:
					for k in range(self.scaling):
						for l in range(self.scaling):
							new_map_np[self.scaling * i + k][self.scaling * j + l] = 0
		return new_map_np


	def portals_str(self):
		'''
		Returns a string containing a list of all portal coordinates
		'''
		i = 1
		s = 'Portal Coordinates\n'
		for key, portals in self.portals.items():
			for near in portals.keys():
		                        # print the cell ids
				s += '%-015s' % (str((key, near)))
				# draw 5 portals coordinates per line
				if i % 5 == 0:
					s+='\n'
				i+=1
		return s

	def init_symbols(self, symbols):
		#get symbol colors _color + bg_color
		
		start_color = symbols['start_color'] if 'start_color' in symbols else ''
		start_bg_color = symbols['start_bg_color'] if 'start_bg_color' in symbols else ''

		end_color = symbols['end_color'] if 'end_color' in symbols else ''
		end_bg_color = symbols['end_bg_color'] if 'end_bg_color' in symbols else ''

		wall_color = symbols['wall_color'] if 'wall_color' in symbols else ''
		wall_bg_color=symbols['wall_bg_color'] if 'wall_bg_color' in symbols else''
		
		head_color = symbols['head_color'] if 'head_color' in symbols else ''
		head_bg_color=symbols['head_bg_color'] if 'head_bg_color' in symbols else ''

		tail_color = symbols['tail_color'] if 'tail_color' in symbols else ''
		tail_bg_color = symbols['tail_bg_color'] if 'tail_bg_color' in symbols else ''

		empty_color = symbols['empty_color'] if 'empty_color' in symbols else ''

		# symbol colors
		self.start = start_bg_color	+ start_color 	+ symbols['start'] 
		self.end =  end_bg_color 	+ end_color 	+ symbols['end']    + empty_color
		self.wall_h = wall_bg_color	+ wall_color 	+ symbols['wall_h'] 
		self.wall_v = wall_bg_color	+ wall_color 	+ symbols['wall_v'] 
		self.wall_c = wall_bg_color	+ wall_color 	+ symbols['wall_c'] 
		self.head = head_bg_color 	+ head_color 	+ symbols['head']   
		self.tail = tail_bg_color 	+ tail_color 	+ symbols['tail']   
		self.empty = empty_color+' '
	
	def kruskalize(self):
		'''
		Kruskal's algorithm, except when grabbing the next available edge, 
		order is randomized. 
		Uses a disjoint set to create a set of keys. 
		Then for each edge seen, the key for each cell is used to determine 
		whether or not the the keys are in the same set.
		If they are not, then the two sets each key belongs to are unioned.
		Each set represents a region on the maze, this finishes until all
		keys are reachable (MST definition) or rather all keys are unioned into 
		single set. 
		@params
			None 
		@return
			None
		'''
		# edge = ((row1, col1), (row2, col2)) such that grid[row][col] = key
		edges_ordered = [ ]
		# First add all neighboring edges into a list
		for row in range(0, self.height):
			for col in range(0, self.width):	
				cell = (col, row)
				left_cell = (col-1, row)
				down_cell = (col, row-1)
				near = []
				# if not a boundary cell, add edge, else ignore
				if col > 0:
					near.append((left_cell, cell))
				if row > 0:
					near.append( (down_cell, cell))
				edges_ordered.extend(near)
				
		# seed the random value
		random.seed(self.seed)
		edges = []
		# shuffle the ordered edges randomly into a new list 
		while len(edges_ordered) > 0:
			# randomly pop an edge
			edges.append(edges_ordered.pop(random.randint(0,len(edges_ordered))-1))
		disjoint_set = ds.DisjointSet()
		for row in range(0, self.height):
			for col  in range(0,self.width):
				# the key is the cells unique id
				key = self.grid[col][row]
				# create the singleton 
				disjoint_set.make_set(key)
				# intialize the keys portal dict
				self.portals[key] = {}
		edge_count = 0
		# eulers formula e = v-1, so the
		# minimum required edges is v for a connected graph!
		# each cell is identified by its key, and each key is a vertex on the MST
		key_count = self.grid[self.width-1][self.height-1] # last key	
		while edge_count < key_count:
			# get next edge ((row1, col1), (row2,col2))
			edge = edges.pop()
			# get the sets for each vertex in the edge
			key_a = self.grid[edge[0][0]][edge[0][1]]
			key_b = self.grid[edge[1][0]][edge[1][1]]
			set_a = disjoint_set.find(key_a)
			set_b = disjoint_set.find(key_b)
			# if they are not in the same set they are not in the 
			# same region in the maze
			if set_a != set_b:
				# add the portal between the cells, 
				# graph is undirected and will search
				# [a][b] or [b][a]
				edge_count+=1	
				self.portals[key_a][key_b] = True 
				self.portals[key_b][key_a] = True 
				disjoint_set.union(set_a, set_b)

	def move(self, direction):
		'''
		Used to indicate of the player has completed the maze
		@params
			direction((int, int)) : Direction to move player
									  
		@return
			None
		'''
		assert(direction in [self.LEFT, self.RIGHT, self.UP, self.DOWN])
		# if new move is the same as last move pop from path onto player 
		new_move = (self.player[0]+direction[0],\
					self.player[1]+direction[1]) 
		valid = False
		# if new move is not within grid
		if new_move[0] < 0 or new_move[0] >= self.width or\
			new_move[1] < 0 or new_move[1] >= self.height:
			return valid
		player_key = self.width*self.player[1] + self.player[0]		
		move_key = self.width*new_move[1] + new_move[0]	
 		#if theres a portal between player and newmove
		if move_key in self.portals[player_key]:
			self.is_moving = True
			#'\033[%d;%dH' % (y x)# move cursor to y, x
			head = '\033[%d;%dH' % (new_move[1]*2+2, new_move[0]*2+2)  + self.head
			# uncolor edge between (edge is between newmove and player)
			edge = '\033[%d;%dH' %  (self.player[1]*2+(new_move[1]-self.player[1])+2,\
									self.player[0]*2+(new_move[0]-self.player[0])+2)
			tail = '\033[%d;%dH' % (self.player[1]*2+2, self.player[0]*2+2) 
			end = '\033[%d;%dH' % ((self.height)*2+2, 0) +self.empty
			# if new move is backtracking to last move then sets player pos to top of path and remove path top
			if len(self.path) > 0 and new_move == self.path[-1]:
				# move cursor to player and color tail, move cursor to player and color empty
				self.player = self.path.pop()
				# move cursor to player and color tail, move cursor to player and color empty
				# uncolor edge between and remove tail
				edge += self.empty
				tail += self.empty
				valid = False # moved back
			# else move progresses path, draws forward and adds move to path
			else:
				self.path.append(self.player)
				self.player = new_move
				#move cursor to position to draw if ANSI
				# color edge between and color tail
				edge += self.tail
				tail += self.tail					
				valid = True # successfully moved forward between portals

			# use write and flush to ensure buffer is emptied completely to avoid flicker
			sys.stdout.write(head+edge+tail+end)
			sys.stdout.flush()
			self.is_moving = False 
		return valid
	


	def solve(self, position=(0,0)):
		''' Uses backtracking to solve maze'''
		if self.is_done():
			return  True
		for direction in [self.LEFT, self.RIGHT, self.UP, self.DOWN]:
				# try a move, move will return false if no portal of backward progress			
				if self.move(direction):
					# after move, set new test position to be current player position
					if self.solve(self.player):
						return True
				# if position changed 
				if position != self.player: 
					# move back from towards previos position
					self.move((position[0]-self.player[0], position[1]-self.player[1]))

		return False


	def heuristic_solve(self, position=(0,0), depth=0, lookahead=10):
		''' Use backtracking with iterative deepening to solve maze with a distance or randomized choice heuristic'''
		if self.is_done():
			return  True
		if depth > 0:
			directions = [self.LEFT, self.RIGHT, self.UP, self.DOWN]
			# sort by distance towards the end dist 0 is closest so ascending order
			#heuristic
			directions.sort(
				#get manhatten distance
				#key=lambda direction: (self.width-self.player[0]+direction[0]-1+self.height-self.player[1]+direction[1]-1)/2.0
				#random
				key=lambda direction: random.random()
				)
			for direction in directions:
					# try a move, move will return false if no portal of backward progress			
					if self.move(direction):
						# after move, set new test position to be current player position
						if self.heuristic_solve(self.player, depth-1,lookahead):
							return True
					# if position changed 
					if position != self.player: 
						# move back from towards previos position
						self.move((position[0]-self.player[0], position[1]-self.player[1]))
			return False
		else:
			return self.heuristic_solve(self.player, lookahead, lookahead+1)



	def start_timer(self):
		self.is_moving = False
		self.timer_thread = threading.Thread(target=self.timer_job)
		self.timer_thread.start() 

	def kill_timer(self):
		self.player = (self.width-1, self.height-1)
		if self.timer_thread != None:
			self.timer_thread.join()

	def end_timer(self):
		self.kill_timer()
		return self.time_taken

	def timer_job(self):
		start_time = time.time()
		# your code
		# prints the current time at the bottom of the maze 
		while not self.is_done():
			# if not currently writing move, print time at bottom
			if not self.is_moving: 
				time_elapsed = time.time() - start_time
				# delay on the update rate (only update every 10th of a second)
				if time_elapsed -self.time_taken > 0.01: 
					self.time_taken = time_elapsed 
					# use write and flush to ensure buffer is emptied completely to avoid flicker
					sys.stdout.write('\033[%d;%dHTime:%.2f' % (self.height*2+2, 0, self.time_taken))
					sys.stdout.flush()
			
		self.time_taken = time.time() - start_time

	def is_done(self):
		'''
		Used to indicate of the player has completed the maze
		@params
			None 
		@return
			True if player has reached the end
		'''
		return self.player == (self.width-1, self.height-1)
