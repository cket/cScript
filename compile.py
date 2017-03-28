import sys

code_file = sys.argv[1]

if not code_file.endswith(".ck"):
	raise SyntaxError("File extension must be '.ck'")

with open(code_file) as f:
	tokens = f.read()

tokens = tokens.split()

keywords = {}
stack = []

for token in tokens:
	if token in keywords:
		pass
	try:
		token = float(token)
		stack.append(token)
	except ValueError:
		raise SyntaxError(token)


class SyntaxError(RuntimeError):
	pass
