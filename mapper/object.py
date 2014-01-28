#!/usr/bin/python
#-*-coding:utf-8-*-

class Object:
	def __init__(self):
		self.id = ''
		self.title = ''
		self.tags = []
		self.description = []

class ObjectCollection:
	def __init__(self, fileName, mode):
		if mode == 'r':
			self.file = open(fileName, 'r')
		elif mode == 'w':
			self.file = open(fileName, 'w')
		else:
			raise Exception('Invalid mode.')

		self.mode = mode;
	
	def __del__(self):
		self.file.close()
	
	#Writes an object to the object collection file.
	def write(self, obj):
		assert(self.mode == 'w')

		self.file.write(obj.id)
		self.file.write('\n')
		self.file.write(obj.title)
		self.file.write('\n')
		self.file.write(str(len(obj.tags)))
		self.file.write('\n')
		for tag in obj.tags:
			self.file.write(tag)
			self.file.write('\n')
		self.file.write(str(len(obj.description)))
		self.file.write('\n')
		for word in obj.description:
			self.file.write(word)
			self.file.write('\n')
	
	#Reads the next object from the object collection file
	def read(self):
		assert(self.mode == 'r')

		obj = Object()
		obj.id = self.file.readline().replace('\n', '')
		
		if obj.id == '':
			return None
	
		obj.title = self.file.readline().replace('\n', '')
		n_tags = int(self.file.readline().replace('\n', ''))
		for i in xrange(n_tags):
			obj.tags.append(self.file.readline().replace('\n', ''))
		n_words_in_description = int(self.file.readline().replace('\n', ''))
		for i in xrange(n_words_in_description):
			obj.description.append(self.file.readline().replace('\n', ''))

		return obj

	#Returns a object collection iterator
	def __iter__(self):
		return self
	
	#Gets the next item from the collection
	def next(self):
		obj = self.read()

		if obj == None:
			raise StopIteration
		else:
			return obj
