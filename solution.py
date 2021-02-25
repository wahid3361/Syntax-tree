
class Node:
	"""Class to represent a tree node."""
	def __init__(self, data):
		"""Constructor"""
		self.data = data

		# left and right child node attributes
		self.left = None
		self.right = None


class ExpressionTree:
	"""Express Tree class"""

	def __init__(self, root):
		"""Constructor"""
		self.root = root

	def getPostFix(self):
		"""Returns the postfix form from the tree"""

		# calling the postorder function
		postFixExpression = self.postOrder(self.root)
		return postFixExpression.strip()

	def postOrder(self, node):
		"""Helper function that returns the post order as string from the node"""

		# if the node is not None (empty)
		if node is not None:
			# recursive calls
			return self.postOrder(node.left) + self.postOrder(node.right) + node.data + " "
		else: # otherwise return empty string
			return ""

	def evaluate(self):
		"""Evaluates the tree and returns the floating point value"""

		# getting the postfix of the tree for easier evaluation
		postfix = self.getPostFix()
		# breaking the postfix of spaces (because space separates numbers/values and operators)
		splitted = postfix.split()

		# stack used in the evaluation
		valueStack = []

		operatorList = ['(', ')', '+', '-', '*', '/', '^']

		try:
			# going through each item in the list
			for val in splitted:
				# if the value is an operator
				if val in operatorList:
					# pop the two values from the stack
					op2 = float(valueStack.pop())
					op1 = float(valueStack.pop())
					# perform evaluation on them based on operator and add to stack
					if val == '+':
						valueStack.append(op1 + op2)
					if val == '-':
						valueStack.append(op1 - op2)
					if val == '*':
						valueStack.append(op1 * op2)
					if val == '/':
						valueStack.append(op1 / op2)
					if val == '^':
						valueStack.append(op1 ** op2)
				else:
					# if not operator then add to stack
					valueStack.append(val)

			# after evaulation, if the length of stack is not 1, then the postfix was wrong
			if len(valueStack) != 1:
				raise Exception

			# otherwise return the evaluated value
			return valueStack[0]
		except ValueError as e: # in case the value couldn't be converted to float
			raise ValueError
		except ZeroDivisionError as e: # in case there's division by zero
			raise ZeroDivisionError
		except RuntimeError as e:
			raise RuntimeError
		except Exception as e:
			raise Exception



def buildTree(infixString):
	"""Function that bulds the free from the infix string list"""
	valueStack = []
	nodeStack = []

	# priority of each operation. higher value has more priority
	priority = {'+' : 1, '-' : 1, '/' : 2, '*' : 2, '^' : 3}
	# list of operators
	operatorList = ['(', ')', '+', '-', '*', '/', '^']

	for i in range(len(infixString)):

		# appending the opening parenthesis 
		if (infixString[i] == '('):
			valueStack.append(infixString[i])
		elif (infixString[i] == ')'): # if closing parenthesis

			# while the stack of values is not empty and the top value is not opening parenthesis
			while len(valueStack) != 0 and valueStack[-1] != '(':
				# pop top value from value stack
				t = Node(valueStack[-1])
				valueStack.pop()
				# pop two values from node stack
				t1 = nodeStack[-1]
				nodeStack.pop()
				t2 = nodeStack[-1]
				nodeStack.pop()

				# merge the two values popped from node stack into tree
				t.left = t2
				t.right = t1

				# append the tree to node stack
				nodeStack.append(t)

			valueStack.pop()

		# if value is not an operator, append it to node stack (as a node)
		elif infixString[i] not in operatorList:
			t = Node(infixString[i])
			nodeStack.append(t)
		else: # otherwise it's an operator

			while len(valueStack) != 0 and valueStack[-1] != '(' and (
				(infixString[i] != '^' and priority[valueStack[-1]] >= priority[infixString[i]]) or 
				(infixString[i] == '^' and priority[valueStack[-1]] > priority[infixString[i]])):

				# getting the value from value stack and create a node with it.
				t = Node(valueStack[-1])
				valueStack.pop()

				# popping two values from node stack
				t1 = nodeStack[-1]
				nodeStack.pop()

				t2 = nodeStack[-1]
				nodeStack.pop()

				# merging the popped values from node stack into the tree
				t.left = t2
				t.right = t1

				# adding the merged tree to node stack
				nodeStack.append(t)


			valueStack.append(infixString[i])

	# the top value on the node stack is the expression tree to return
	tree = nodeStack[-1]
	return tree


def getExpressList(expression):
	"""Helper function that breaks the expression into list of values/operators"""
	expressionList = []
	operatorList = ['(', ')', '+', '-', '*', '/']
	string = ""

	# looping through each character in expression
	for i in range(len(expression)):

		# if it's a digits or alphabet, then append to string
		if (expression[i] >= '0' and expression[i] <= '9') or (expression[i].isalpha()):
			string += expression[i]
		# if it's a operator
		elif expression[i] in operatorList:
			# append the current string to expressionList
			if (string != ""):
				expressionList.append(string)
			string = "" # reset the string
			# append the operator to expressionList
			expressionList.append(expression[i])

	if (string != ""):
		expressionList.append(string)

	# returning the list
	return expressionList


if __name__ == "__main__":

	# asking for input of expresison from user
	expression = input("Enter the infix express: ")
	expression = "(" + expression + ")"

	# breaking the string of expression into list
	expressionList = getExpressList(expression)

	# getting the root of the tree built (expression tree)
	root = buildTree(expressionList)
	
	# initializing the ExpressionTree object
	tree = ExpressionTree(root)

	# printing the postfix form
	print("PostFix form is:")
	print(tree.getPostFix())

	try:
		# printing the evaluation if possible
		print("Evaluation is: ")
		print(tree.evaluate())
	except ValueError as e:
		print("The expression doesn't have all floating/integer values. Check expression!")
	except ZeroDivisionError as e:
		print("Division by zero operation performed. Check expression!")
	except Exception as e:
		print("Invalid expression, could NOT be evaluated!")

