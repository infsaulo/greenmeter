#!/usr/bin/python
#-*-coding:utf-8-*-

from collections import deque

#Aho-Corasick string matching implementation
#How to use:
#	Create a new instance of AhoCorasickAutomata
#	Insert all the patterns using the method add
#	Construct the automata using the method make
#	Use the method match

#Warning: To use strings as symbols, use tuples as patterns and text. Be careful about tuples composed of just one item.	

class Node:
	def __init__(self):
		self.transitions = {}
		self.failure_transition = None
		self.output = set()

class AhoCorasickAutomata:
	def __init__(self):
		self.root = Node()
		self.automata_ready = False
	
	#Inserts a new pattern to be matched
	def add(self, pattern, key):
		assert not self.automata_ready

		last_node = self.root
		for c in pattern:
			if not c in last_node.transitions:
				last_node.transitions[c] = Node()
			last_node = last_node.transitions[c]

		last_node.output = set([key])
	
	#Transition function (internal use)
	def go(self, node, symbol):
		if symbol in node.transitions:
			return node.transitions[symbol]
		else:
			if node == self.root:
				return node
			else:
				return None
	
	#Constructs the failure function
	def make(self):
		assert not self.automata_ready

		queue = deque()
		
		for node in self.root.transitions.values():
			queue.append(node)
			node.failure_transition = self.root

		while len(queue) > 0:
			node = queue.popleft()

			for symbol, destination in node.transitions.items():
				queue.append(destination)

				state = node.failure_transition
				while self.go(state, symbol) == None:
					state = state.failure_transition

				destination.failure_transition = self.go(state, symbol)
				destination.output |= destination.failure_transition.output
		
		self.automata_ready = True
	
	#Matches all the patterns. Each time a pattern is found, callback is called.
	def match(self, text, callback):
		assert self.automata_ready

		node = self.root
		for c in text:
			while self.go(node, c) == None:
				node = node.failure_transition

			node = self.go(node, c)

			for pattern in node.output:
				callback(pattern)

	
	def show_tree(self, node):
		print "{"
		
		for k, v in node.transitions.items():
			print k
			self.show_tree(v)

		print "}"
	
	#Stores the prefix tree
	def store(self, file_name):
		with open(file_name, 'w') as out:
			queue = deque()

			queue.append(self.root)

			while len(queue) > 0:
				node = queue.popleft()
				
				out.write(str(len(node.transitions)))
				out.write(' :')
				for item in node.output:
					out.write(' ')
					out.write(str(item))

				out.write('\n')

				for pattern, neighbor in node.transitions.items():
					out.write(pattern)
					out.write('\n')
					
					queue.append(neighbor)
	
	def load(self, file_name):
		with open(file_name, 'r') as fin:
			queue = deque()
			queue.append(self.root)

			while len(queue) > 0:
				node = queue.popleft()

				line = fin.readline().strip()
				sides = line.split(':')
				n_neighbors = int(sides[0].strip())
				outputs = []
				outputs_string = sides[1].split(' ')
				for output in outputs_string:
					striped_output = output.strip()
					if(striped_output != ''):
						outputs.append(int(striped_output))

				node.output = set(outputs)

				for i in xrange(n_neighbors):
					pattern = fin.readline().strip()
					new_node = Node()
					node.transitions[pattern] =  new_node
					queue.append(new_node)



#def achou(x):
#	for p in x:
#		print p, "*",
#	print ""
#	print len(x)

#t = AhoCorasickAutomata()
#t.add(("t1", "t2"))
#t.add(tuple(["t1"]))

#t.show_tree(t.root)

#t.make()

#t.match(("t3", "t4", "t6", "t2", "t1", "t2", "t3", "r3214", "fasdjk", "fadskjl", "afsdjlk", "fasd"), achou)
