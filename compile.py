import sys

keywords = {}
stack = []

class SyntaxError(RuntimeError):
	pass

def printFn():
	print stack.pop()

def plusFn():
	stack.append(stack.pop() + stack.pop())

def populateKeyWords():
	Print = {"print": printFn}
	Math = {"+": plusFn}
	keywords.update(Print)
	keywords.update(Math)

def parseTokens():
	code_file = sys.argv[1]

	if not code_file.endswith(".ck"):
		raise SyntaxError("File extension must be '.ck'")

	with open(code_file) as f:
		tokens = f.read()
	return tokens.split()

if __name__ == "__main__":
	populateKeyWords()
	tokens = parseTokens()

	for token in tokens:
		if token in keywords:
			keywords[token]()
		else:
			try:
				token = float(token)
				stack.append(token)
			except ValueError:
				raise SyntaxError(token)

