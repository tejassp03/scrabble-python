import sys, re
from word import Word

class Player:
	def __init__(self, inp=sys.stdin, outp=sys.stdout, name=None):
		self.input = inp
		self.output = outp
		self.name = name
		self.score = 0
		self.letters = []
		self.wild_tile = None
		self.is_passing = False
		self.is_rejected = False

	def _pick_from(self, bag):
		if bag:
			return bag.draw()

	def _pass_letters(self, bag, board):
		self.output.write('\nEnter the letter(s) you want to pass: ')
		player_input = self.input.readline()[:-1].upper()
		passed_letters = list(re.sub('[^A-Z@]', '', player_input))

		if self._valid_letters(passed_letters):
			for l in passed_letters:
				self.letters.remove(l)

			bag.put_back(passed_letters)
			self.draw_letters(bag, len(passed_letters))
		else:
			self.display_message("One or more letters are not on your rack...")
			self.get_move(bag, board)

	def _replace_wild_tile(self):
		self.output.write("\nWhat letter will you use the wild tile for? ")
		self.wild_tile = self.input.readline()[:-1].upper()
		self.word.word = re.sub('@', self.wild_tile, self.word.word)

	def _valid_letters(self, word=None):
		if '@' in (word or self.word.word):
			self._replace_wild_tile()

		if self.wild_tile:
			self.letters[self.letters.index('@')] = self.wild_tile

		for l in (word or self.word.word):
			if self.word.aob_list and l not in self.word.aob_list and l not in self.letters:
				if not self._letter_on_rack(word, l):
					return False
			else:
				if not self._letter_on_rack(word, l):
					return False

		self.wild_tile = None
		return True

	def _letter_on_rack(self, word, l):
		if l not in self.letters or (word or self.word.word).count(l) > self.letters.count(l):
			if self.wild_tile:
				self.letters[self.letters.index(self.wild_tile)] = '@'
				self.wild_tile = None
			return False
		return True

	def draw_letters(self, bag, amount=7):
		for i in range(amount):
			self.letters.append(self._pick_from(bag))

	def update_rack(self, bag):
		for l in self.word.word:
			if l not in self.word.aob_list:
				self.letters.remove(l)

		self.draw_letters(bag, len(self.word.word) - len(self.word.aob_list))

	def get_move(self, bag, board):
		self.wild_tile = None
		self.is_passing = False

		self.output.write('\nEnter your move (e.g. h8 r money): ')
		player_input = self.input.readline()[:-1].lower().split()

		if len(player_input) < 3 or len(player_input) > 3:
			if player_input[0] == 'pass':
				self._pass_letters(bag, board)
				self.is_passing = True
			elif player_input[0] == 'save':
				pass
			else:
				self.display_message('Make sure your input is correct (e.g. h8 r money)')
				self.get_move(bag, board)
		else:
			start, direction, word = player_input
			self.word = Word(start, direction, word.upper(), board.board)

			if direction not in ['r', 'd']:
				self.display_message('Your direction should be either \'r\' for right or \'d\' for down...')
				self.get_move(bag, board)
			elif not self._valid_letters():
				self.display_message('One or more letters are not on your rack...')
				self.get_move(bag, board)

	def display_message(self, message):
		self.output.write('\n==================================================================\n')
		self.output.write(message.center(70))
		self.output.write('\n==================================================================\n')

	def __str__(self):
		return '{} has got {} points.'.format(self.name, self.score).center(70)