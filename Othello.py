
import random

# this class stores an othello board state
# the state is handled as a 1d list that stores a 10x10 board.  1 and -1 are the two colors, 0 are empty squares
class Board:
        # make a starting board.  There are four pieces in the center
	def __init__(self):
		self.state=[0]*100
		self.state[44]=1
		self.state[45]=-1
		self.state[54]=-1
		self.state[55]=1

        # returns the score as the difference between the number of 1s and the number of -1s
	def evaluate(self):
		value=0
		for i in range(100):
			if self.state[i]==1:
				value=value+1
			elif self.state[i]==-1:
				value=value-1
		return value

        # returns a new board that is a copy of the current board
	def copy(self):
		board=Board()
		for i in range(100):
			board.state[i]=self.state[i]
		return board

	# given a x,y position, returns the tile within the 1d list
	def index(self,x,y):
		if x>=0 and x<10 and y>=0 and y<10:
			return self.state[x+y*10]
		else:
                        #out of bounds, return -2 for error
			return -2

	# given an x,y coordinate, and an id of 1 or -1, returns true if this is a valid move
	def canplace(self,x,y,id):
                # square is not empty? return false
		if self.index(x,y)!=0:
			return False
		# these functions compute the 8 different directions
		dirs=[(lambda x: x, lambda y: y-1),(lambda x: x, lambda y: y+1),(lambda x: x-1, lambda y: y-1),(lambda x: x-1, lambda y: y),(lambda x: x-1, lambda y: y+1),(lambda x: x+1, lambda y: y-1),(lambda x: x+1, lambda y: y),(lambda x: x+1, lambda y: y+1)]
		# for each direction...
		for xop,yop in dirs:
                        # move one space.  is the piece the opponent's color?
			i,j=xop(x),yop(y)
			if self.index(i,j)!=-id:
                                # no, then we'll move on to the next direction
				continue
			# keep going until we hit our own piece
			i,j=xop(i),yop(j)
			while self.index(i,j)==-id:
				i,j=xop(i),yop(j)
			# if we found a piece of our own color, then this is a valid move
			if self.index(i,j)==id:
				return True
                # if I can't capture in any direction, I can't place here
		return False

        # given an x,y coordinate, and an id of 1 or -1, place a tile (if valid) at x,y, and modify the state accordingly 
	def place(self,x,y,id):
                # don't bother if it isn't a valid move
		if not self.canplace(x,y,id):
			return
		# place your piece at x,y
		self.state[x+y*10]=id
		dirs=[(lambda x: x, lambda y: y-1),(lambda x: x, lambda y: y+1),(lambda x: x-1, lambda y: y-1),(lambda x: x-1, lambda y: y),(lambda x: x-1, lambda y: y+1),(lambda x: x+1, lambda y: y-1),(lambda x: x+1, lambda y: y),(lambda x: x+1, lambda y: y+1)]
		# go through each direction
		for xop,yop in dirs:
			i,j=xop(x),yop(y)
                        # move one space.  is the piece the opponent's color?
			if self.index(i,j)!=-id:
                                # no, then we can't capture in this direction.  we'll move on to the next one
				continue
			# keep going until we hit our own piece
			while self.index(i,j)==-id:
				i,j=xop(i),yop(j)
			# if we found a piece of our own color, then this is a valid move
			if self.index(i,j)==id:
				k,l=xop(x),yop(y)
                                # go back and flip all the pieces to my color
				while k!=i or l!=j:
					self.state[k+l*10]=id
					k,l=xop(k),yop(l)

	# returns a list of all valid x,y moves for a given id



        #print out the board.  1 is X, -1 is O
	def printboard(self):
		for y in range(10):
			line=""
			for x in range(10):
				if self.index(x,y)==1:
					line=line+"X"
				elif self.index(x,y)==-1:
					line=line+"O"
				else:
					line=line+"."
			print(line)

        #state is an end game if there are no empty places
	def end(self):
		return not 0 in self.state

	def validmoves(self,id):
		moves=[]
		for x in range(10):
			for y in range(10):
				if self.canplace(x,y,id):
					moves=moves+[(x,y)]
		return moves
	
	def greedy(self,board, turn):
			moves = board.validmoves(turn)

			for m in range(len(moves)):
				moves[m] = (self.greedyScore(turn), moves[m])
			moves.sort(reverse=True)
			topscore = moves[0][0]
			# move forward until stop seeing that score
			index = 0
			while index < len(moves) and moves[index][0] == topscore:
				index += 1
			moves = moves[:index]
			# pick one randomly from the best moves
			move = moves[random.randrange(0, len(moves))]
			# remove the score
			move = move[1]
			return move

	def greedyScore(self, turn):
			values = 0
			for i in range(100):
				if turn == 1:
					values+=1
				else:
					values-=1
	

def allMoves(board,player):
		children = []
		for move in board.validmoves(player):
			child = board.copy()
			child.place(move[0],move[1],player)
			children.append(child)
		return child

def allmoves(brd,player):
    moves=[]
    # search through for " "
    for i in brd.validmoves(player):
        if brd[i]==' ':
            # every time I find a space, I replace it with player's token, and add it to list
            child = list(brd[:i]) + [player] + list(brd[i+1:])
            child=tuple(child)
            moves=moves+[child]
    return moves

def nextBestMove(board,turn):
		bestMove = None;
		bestValue = None;
		moves = allMoves(board,turn)

		if turn == 1:
			for move in moves:
				newBoard = board.copy();
				newBoard.place(move[0],move[1],turn)
			if bestValue == max(bestValue, minimax(board,2,turn)):
				bestMove = move

		if turn == -1:
			for move in moves:
				newBoard.copy()
				newBoard.place(move[0],move[1],turn)
			if bestValue == min(bestValue, minimax(board,2,turn)):
				bestMove = move
		return bestMove

#score that calls evaluate  
def score(board,turn):
	if turn == 1:
		return board.evaluate()
	else:
		return -board.evaluate()

def minimax(board,depth,turn): #ndepth
		moves = board.validmoves(turn)

	
		bestScore = -10000	
		bestMove = None
		for move in moves:
				newBoard = board.copy()
				newBoard.place(move[0],move[1],turn)
				countermoves = newBoard.validmoves(-turn)
				worstScore = 10000		
				for counter in countermoves:
					counterBoard = newBoard.copy()
					counterBoard.place(counter[0],counter[1],-turn)
					if depth == 0 or counterBoard.end():
						tryscore = score(counterBoard,turn)
						
						#call score function passing it counterboard, and turn ^
					else: 
						tryscore = minimax(counterBoard,depth-1,turn)[0]
					
					if tryscore < worstScore:
						worstScore = tryscore
				if worstScore > bestScore:
					bestScore = worstScore
					bestMove = move
				

				
		return (bestScore, bestMove)
								





	

def game():	
	board = Board()
	print("starting board:")
	board.printboard()
	# start with player 1
	turn = 1
	while True:
		if turn == 1:
			print("X's turn")
		if turn != 1:
			print("O's turn")
		#movelist = minimax_ndepth(board, 2, turn)
		if turn == 1:
			movelist = minimax(board, 1, turn)[1]
			#movelist = board.greedy(board, turn)
		else: 
			#movelist = minimax(board, 2, turn)[1]
			movelist = board.greedy(board, turn)
		#movelist = board.greedy(board, turn)
		#movelist = board.validmoves(turn)
		#movelist = board.minimax_onedepth(board,turn)
		#movelist = nextBestMove(board,turn)
		print("current moves : ", movelist)
		if len(movelist) == 0:
			turn = -turn
			continue
		# pick a move totally at random

		# i = random.randint(0, len(movelist) - 1)
		# make a new board
		board = board.copy()
		# make the move
		#movelist is a tuple, using it as [0], [1]
		board.place(movelist[0], movelist[1], turn)
		# board.place(movelist[i][1], movelist[0][i], turn)
		# swap players
		turn = -turn
		# print
		board.printboard()
		# wait for user to press a key
		input()
		# game over? stop.
		if board.end():
			break
		print("Score is", board.evaluate())
game()

