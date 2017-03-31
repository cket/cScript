import sys


class SyntaxError(RuntimeError):
	pass

class Compiler(object):
	def __init__(self, code_file):
		self.keywords = self.populateKeyWords()
		self.tokens = self.parseTokens(code_file)
		self.stack = []

	def run(self):
		for token in self.tokens:
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
		keywords.update(Print)
		keywords.update(Math)
		keywords.update(Stack)
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



