#!/usr/bin/python
#-*-coding:utf-8-*-

#Builds an dictionary composed of the words listed in a file (each word in aline)

class Dictionary:
	def __init__(self, word_list_file):
		self.word_list_file = word_list_file
		self.dictionary = {}
		with open(word_list_file, 'r') as word_list:
			for line in word_list:
				self.dictionary[line.strip().lower()] = None
	
	#Checks if a word belongs to the dictionary
	def belongs_to(self, word):
		return word in self.dictionary
