#!/usr/bin/python
#-*-coding:utf-8-*-
from __future__ import division


from ahocorasick import *
import sys

class Translator:
	def __init__(self, vocabulary_file):
		self.automata = AhoCorasickAutomata()

		self.automata.load(vocabulary_file)

		self.automata.make()
	
	def translate(self, term_list):
		self.output = []

		self.automata.match(term_list, self.handle_match)

		return self.output
	
	def handle_match(self, pattern):
		self.output.append(pattern)
