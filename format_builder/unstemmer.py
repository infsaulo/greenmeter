#!/usr/bin/python
#-*-coding:utf-8-*-
import sys

class Unstemmer:
	def __init__(self, unstem_dictionary):
		self.dictionary = {}
		with open(unstem_dictionary, 'r') as unstem_file:
			count = 0
			state = 0
			stemmed_word = ''
			for line in unstem_file:
				word = line.strip()
				if state == 0:
					self.dictionary[word] = list()
					stemmed_word = word
					state = 1
				elif state == 1:
					count = int(word)
					state = 2
				else:
					self.dictionary[stemmed_word].append(word)
					count -= 1
					if count == 0: state = 0
	
	def unstem(self, stemmed_word):
		if stemmed_word in self.dictionary:
			return self.dictionary[stemmed_word]
		else:
			return list([stemmed_word])


if __name__ == '__main__':
	us = Unstemmer(sys.argv[1])
	print us.unstem(sys.argv[2])			
