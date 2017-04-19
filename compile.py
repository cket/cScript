import sys


class SyntaxError(RuntimeError):
	pass

class String(object):
	pass

class Number(object):
	pass

class Keyword(object):
	pass

types = [String, Number, Keyword]

class Compiler(object):
	def __init__(self, code_file):
		self.keywords = self.populateKeyWords()
		self.tokens = self.parseTokens(code_file)
		self.stack = []
		self.current_pos = -1

	@property
	def end(self):
		return len(self.tokens)

	def eof(self):
		return self.end == (self.current_pos + 1)

	def run(self):
		while not self.eof():
			# can't use a for loop since we may want to parse multiple words per loop (variable definitions)
			t, token = self.next_token
			if t is Keyword:
				self.keywords[token]()
			else:
				self.stack.append(token)

	def synWrapper(self, m):
		try:
			m()
		except:
			raise SyntaxError("Problem occured during execution of %s" % m.__name__)

	@property
	def next_token(self):
		def _nextWord():
			pointer = 0
			builder = ''
			while pointer < len(self.tokens) and not self.tokens[pointer].isspace():
				builder += self.tokens[pointer]
				pointer += 1
			self.tokens = self.tokens[pointer:]
			return builder

		def _nextString():
			# we know first char is " - skip it
			pointer = 1
			builder = '\"'
			while pointer < len(self.tokens) and self.tokens[pointer] != '\"':
				builder += self.tokens[pointer]
				pointer += 1
			builder += self.tokens[pointer]
			self.tokens = self.tokens[pointer + 1:]
			return builder

		def _removeWhiteSpace():
			pointer = 0
			while pointer < len(self.tokens) and self.tokens[pointer].isspace():
				pointer += 1
			self.tokens = self.tokens[pointer:]

		_removeWhiteSpace()
		t_type = None
		try:
			tokenChar = self.tokens[0]
		except IndexError:
			exit(0)

		if tokenChar == '\"':
			# found a string
			t_type = String
			token = _nextString()
		else:
			token = _nextWord()

		if t_type is not None:
			pass
		elif token in self.keywords:
			t_type = Keyword
		else:
			try:
				token = float(token)
			except ValueError:
				t_type = None
			else:
				t_type = Number
		return t_type, token

	def varFn(self):
		# get the next word, define it as a keyword with value 0
		_, token = self.next_token
		self.keywords[token] = self.initialFn

	def initialFn(self):
		self.stack.append(0)

	def storeFn(self):
		def innerstore(v):
			self.stack.append(v)
		# value store variable
		val = self.stack.pop()
		t, variable_name = self.next_token
		assert variable_name in self.keywords # var must be initialized first
		self.keywords[variable_name] = lambda : innerstore(val)

	def printFn(self):
		print self.stack.pop()

	def plusFn(self):
		self.stack.append(self.stack.pop() + self.stack.pop())

	def dupFn(self):
		self.stack.append(self.stack[-1])

	def dropFn(self):
		self.stack.pop()

	def swapFn(self):
		tos = self.stack.pop()
		self.stack.insert(-2, tos)

	def overFn(self):
		self.stack.append(stack[-2])

	def rotateFn(self):
		tos = self.stack.pop()
		second = self.stack.pop()
		self.stack.insert(-2, second)
		self.stack.insert(-2, tos)


	def populateKeyWords(self):
		keywords = {}
		Print = {"print": self.printFn}
		Math = {"+": self.plusFn}
		Stack = {"dup": self.dupFn, # copy TOS
				 "drop": self.dropFn, # pop
				 "swap": self.swapFn, # swap TOS and 2OS
				 "over": self.overFn, # Copy 2OS to TOS
				 "rotate": self.rotateFn, # Move 3OS to TOS
				 }
		Variable = {"var" : self.varFn,
					"store" : self.storeFn,
					#"assert" : self.assertFn,
					}
		keywords.update(Print)
		keywords.update(Math)
		keywords.update(Stack)
		keywords.update(Variable)
		return keywords

	def parseTokens(self, code_file):
		if not code_file.endswith(".ck"):
			raise SyntaxError("File extension must be '.ck'")

		with open(code_file) as f:
			tokens = f.read()
		return tokens


if __name__ == "__main__":
	c = Compiler(sys.argv[1])
	c.run()
