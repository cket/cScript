import sys

keywords = {}
stack = []

class SyntaxError(RuntimeError):
	pass

def printFn():
	print stack.pop()


def plusFn():
	stack.append(stack.pop() + stack.pop())


def dupFn():
	stack.append(stack[-1])


def dropFn():
	stack.pop()


def swapFn():
	tos = stack.pop()
	stack.insert(-2, tos)


def overFn():
	stack.append(stack[-2])


def rotateFn():
	tos = stack.pop()
	second = stack.pop()
	stack.insert(-2, second)
	stack.insert(-2, tos)

def populateKeyWords():
	Print = {"print": printFn}
	Math = {"+": plusFn}
	Stack = {"dup": dupFn, # copy TOS
			 "drop": dropFn, # pop
			 "swap": swapFn, # swap TOS and 2OS
			 "over": overFn, # Copy 2OS to TOS
			 "rotate": rotateFn, # Move 3OS to TOS
			 }
	keywords.update(Print)
	keywords.update(Math)
	keywords.update(Stack)

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

