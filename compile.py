import sys


class SyntaxError(RuntimeError):
	pass

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
			token = self.next_token
			if token in self.keywords:
				self.keywords[token]()
			else:
				try:
					token = float(token)
					self.stack.append(token)
				except ValueError:
					raise SyntaxError(token)

	def synWrapper(self, m):
		try:
			m()
		except:
			raise SyntaxError("Problem occured during execution of %s" % m.__name__)

	@property
	def next_token(self):
		self.current_pos += 1
		token = self.tokens[self.current_pos]
		return token

	def varFn(self):
		# get the next word, define it as a keyword with value 0
		token = self.next_token
		self.keywords[token] = self.initialFn

	def initialFn(self):
		self.stack.append(0)

	def storeFn(self):
		def innerstore(v):
			self.stack.append(v)
		# value store variable
		val = self.stack.pop()
		variable_name = self.next_token
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
		return tokens.split()


if __name__ == "__main__":
	c = Compiler(sys.argv[1])
	c.run()
