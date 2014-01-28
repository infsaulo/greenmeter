#! /usr/bin/env python

# Description: mapper_lfm_artist.py implements class that retrieve all attributes in artist Last.FM document.
# Author: Saulo Marques Ribeiro Ricci
# Date: 2010/08/26

from threading import Thread
from collections import defaultdict
import xml.dom.minidom
import types
import string
import random

from object import *

from crawler.stop_words_vocabularies import *
from mapper.PorterStemmer import PorterStemmer
from mapper.translator import Translator 
 
class mapper_lfm_artist:
	def __init__(self, xml_filename_list, output_dir, aho_corasick_filename, vocabulary_filename):
		self.output_dir= output_dir
		self.output_file_list = []
		self.xml_file_list = []
		for xml_filename in xml_filename_list:
			self.xml_file_list.append(xml.dom.minidom.parse(xml_filename))
		
		# Loads dict that contains lastfm vocabulary
		self.vocabulary = self.get_vocabulary(vocabulary_filename)

		# Structure to deal with Aho-Corasick
		print aho_corasick_filename
		self.translator = Translator(aho_corasick_filename)

#		self.vocabulary = dict()
#		with open(vocabulary_filename, 'r') as file:
#			for entry in file:
#				splits = entry.strip().split(" ")
#				self.vocabulary[splits[0].strip()] = splits[1].strip()
		self.keys_voc = self.vocabulary.keys()
		self.keys_voc.sort()
		
		self.name_list = []
		self.tags_list = []
		self.unstemming_tags_dict_list = []
		self.wikiText_list = []
		for xml_file_object in self.xml_file_list:
			name_element = self.get_node_element("name", xml_file_object)
			name = None
			if name_element.__class__ != types.NoneType:
				if len(name_element) > 0:
					name = name_element[0].nodeValue
			self.name_list.append(name)
		
			tags = []
			tags_element = self.get_node_element("tags", xml_file_object)
			if tags_element.__class__ != types.NoneType:
				for element in tags_element:
					if element.nodeType == element.ELEMENT_NODE and element.localName == "string":
						tags.append(element.childNodes[0].nodeValue)
			self.tags_list.append(tags)

			wikiText_element = self.get_node_element("wikiText", xml_file_object)
			wikiText = None
			if wikiText_element.__class__ != types.NoneType:
				if len(wikiText_element) > 0:
					wikiText = wikiText_element[0].nodeValue
			self.wikiText_list.append(wikiText)
		
		self.make_modifications()
		self.output_data()

	def get_vocabulary(self, voc_filename):
		with open(voc_filename, 'r') as voc_file:
			dict_terms = dict()
			for line in voc_file:
				splited_terms = [term + ' ' for term in line.strip().split(' ')]
				dict_terms[''.join(splited_terms[:len(splited_terms) - 1]).strip()] = int(splited_terms[len(splited_terms) - 1].strip())

		return dict_terms	

	def get_node_element(self, att_name, xml_file_object):
		element = None
		found = False
		for parent_element in xml_file_object.childNodes:
			for inner_element in parent_element.childNodes:
				if inner_element.nodeType == inner_element.ELEMENT_NODE and inner_element.localName == att_name:
					element = inner_element
					found = True
					break
			if found == True:
				break
		if found == True:
			return element.childNodes
		else:
			return element

	def change_field(self, field):
		new_field = ""
		for term in field.split(' '):
			if term.lower().strip() not in EN_STOP_WORDS:
				clean_term = self.change_term(term)
				if clean_term.__class__ != types.NoneType:
					clean_term = self.get_stemmed_term(clean_term)
					new_field += clean_term + ' ' if((clean_term != "") and (clean_term != " ")) else "" 

		new_field = new_field.strip()
		return new_field

	def change_term(self, term):
		term = term.replace('&amp;quot;', "")
		term = term.replace('&amp;amp;', " ")

		for c in string.punctuation:
			if len(term) == 0:
				return ""
			try:
				num = int(term[0])
				term = term.replace(c, "") if c != '-' else term.replace(c, ' ')
			except ValueError:
				term = term.replace(c, "") if ((c != '-') and (c != '\'') and (c != '\\') and (c != '_')) else term.replace(c, ' ')
		
		return term

	def get_stemmed_term(self, term):
		splited_terms = [word.lower().strip() for word in term.split(' ')]
		stemmizer = PorterStemmer()
		new_splited_terms = [filter(lambda x: x.isalnum(), term) for term in splited_terms]
		stemmed_term = ''.join([stemmizer.stem(word) + ' ' for word in new_splited_terms]).strip()
		return stemmed_term
		
	def make_modifications(self):
		for index in range(len(self.name_list)):
			if self.name_list[index].__class__ != types.NoneType:
				self.name_list[index] = self.name_list[index].lower().strip()
#				self.name_list[index] = self.change_field(self.name_list[index])

		for index in range(len(self.tags_list)):
			self.unstemming_tags_dict_list.append(defaultdict(list))
			for i in range(len(self.tags_list[index])):
				filtered_tag = self.change_term(self.tags_list[index][i].strip())
				filtered_tag_list = self.get_term_list(filtered_tag)

				# Adding terms of the unstemmized-tag dictionary
				for tag in filtered_tag_list:
					self.unstemming_tags_dict_list[index][self.change_field(tag)].append(tag.strip())
				
				self.tags_list[index][i] = self.change_field(filtered_tag_list[0])

		for index in range(len(self.wikiText_list)):
			if self.wikiText_list[index].__class__ != types.NoneType:
				self.wikiText_list[index] = self.change_field(self.wikiText_list[index])

	def get_term_list(self, words):
		word_list = [words]
		for word in words.split(" "):
			if word == word_list[0]:
				return word_list

			if word != "" and word != " ":
				word_list.append(word.strip())

		return word_list

	def output_unstemm_file(self, dict_tags, artist_name):
		with open(self.output_dir + "/unstemmtag." + artist_name, 'w') as unstemm_tag_file:
			for (k, v) in dict_tags.items():
				unique_list = list(set(v))
				unstemm_tag_file.write(k.strip() + "\n" + str(len(unique_list)).strip() + "\n")
				for derivated_tag in unique_list:
					unstemm_tag_file.write(derivated_tag.strip() + "\n")

	def output_data(self):
		for index in range(len(self.xml_file_list)):
			# ID
			id = self.map_id(self.name_list[index])
			with open(self.output_dir + "/test." + id.strip(), 'w') as test_file:
				with open(self.output_dir + "/inputtag." + id.strip(), 'w') as input_tag_file:
					self.output_file_list.append((self.output_dir + "/test." + id.strip() ,self.output_dir + "/inputtag." + id.strip(), self.output_dir + "/unstemmtag." + id.strip()))
					self.output_unstemm_file(self.unstemming_tags_dict_list[index], id.strip())
					# PONTO DE MODIFICACAO
					tags = self.map_tags(self.tags_list[index])
					
					if self.wikiText_list[index].__class__ != types.NoneType:
#						description_parts = self.split_description(self.wikiText_list[index])
	
#						description_threaded_mappers = []
#						for i in range(len(description_parts)):
#							description_threaded_mappers.append(threaded_mapper_description(description_parts[i], self.vocabulary, self.keys_voc))
#						for j in range(len(description_threaded_mappers)):
#							description_threaded_mappers[j].start()
#						description = ""
#						for k in range(len(description_threaded_mappers)):
#							description_threaded_mappers[k].join()
#							description += description_threaded_mappers[k].mapped_description + " "
#						description = description.strip()
						description = self.map_description(self.wikiText_list[index])

					else:
						description = ""
					# PONTO DE MODIFICACAO
					title = self.map_title(self.change_field(self.name_list[index]))	
					test_file.write("ID " + id + " | TAG" + tags + " | DESCRIPTION " + description + " | TITLE " + title + "\n")
					input_tag_file.write("ID " + id + tags + "\n")
						
	def split_description(self, description):
		description_parts = []
		description_splits = description.split(" ")
		while True:
			description_part = ""
			for index in range(200):
				if len(description_splits) > 0:
					description_part += description_splits.pop(0) + " "
				else:
					break
			if description_part != "":
				description_parts.append(description_part.strip())
			else:
				break

		return description_parts		

	def binary_search(self, value, seq):
		final_index = len(seq) - 1
		start_index = 0
		current_index = (final_index - start_index)/2
		while (final_index != start_index) and ((final_index - start_index) > 1):
			if seq[current_index] == value: 
				return True
			elif seq[current_index] < value:
				start_index = current_index + 1
				current_index = ((final_index - start_index)/2) + start_index
			else:
				final_index = current_index - 1
				current_index = ((final_index - start_index)/2) + start_index

		if seq[current_index] == value:
			return True
		elif (seq[start_index] == value) or (seq[final_index] == value):
			return True
		return False

	def map_id(self, id):
		id_str = ""
		if id.__class__ != types.NoneType:
			id_str += id.strip().replace(" ", "+")
		return id_str

	def map_description(self, description):
		description_str = ''.join([str(int_str) + " " for int_str in self.translator.translate(description.split(' '))]).strip()
#		description_splits = description.split(" ")
#		for description_word in description_splits:
#			if self.binary_search(description_word.strip(), self.keys_voc):
#				description_str += " " + self.vocabulary[description_word.strip()].strip()
		
		return description_str

	def map_tags(self, tags):
		tags_str = ""
		tag_set = set()
		for tag in tags:
			if self.binary_search(tag, self.keys_voc):
				tag_set.add(tag)
#				tags_str += " " + str(self.vocabulary[tag]).strip()
			else:
				splited_tags = tag.split(' ')
				for splited_tag in splited_tags:
					if self.binary_search(splited_tag.strip(), self.keys_voc):
						tag_set.add(splited_tag.strip())
				
		for final_tag in list(tag_set):
			tags_str += " " + str(self.vocabulary[final_tag]).strip()
			# If tag contains '-' try to split into more tags
#			elif '-' in tag:
#				splits = tag.split('-')
#				split_set = set()
#				for splited_tag in splits:
#					if self.binary_search(splited_tag.strip(), self.keys_voc) and (splited_tag.strip not in tags):
#						split_set.add(splited_tag.strip())
#				split_list = list(split_set)
#				for entry in split_list:
#					tags_str += " " + self.vocabulary[entry].strip()
		return tags_str

	def map_title(self, title):
		title_str = ''.join([str(int_str) + " " for int_str in self.translator.translate(title.split(' '))]).strip()
		return title_str

#class threaded_mapper_description(Thread):
	
#	def __init__(self, description, vocabulary, keys_voc):
#		Thread.__init__(self)
#		self.description = description
#		self.vocabulary = vocabulary
#		self.keys_voc = keys_voc
#		self.mapped_description = ""
	
#	def run(self):
#		self.mapped_description = self.map_description()

	# PONTO DE MODIFICACAO
#	def map_description(self):
#		description_str = ""
#		description_splits = self.description.split(" ")
#		for description_word in description_splits:
#			if self.binary_search(description_word.strip(), self.keys_voc):
#				description_str += " " + self.vocabulary[description_word.strip()].strip()
#		return description_str

#	def binary_search(self, value, seq):
#		final_index = len(seq) - 1
#		start_index = 0
#		current_index = (final_index - start_index)/2
#		while (final_index != start_index) and ((final_index - start_index) > 1):
#			if seq[current_index] == value: 
#				return True
#			elif seq[current_index] < value:
#				start_index = current_index + 1
#				current_index = ((final_index - start_index)/2) + start_index
#			else:
#				final_index = current_index - 1
#				current_index = ((final_index - start_index)/2) + start_index

#		if seq[current_index] == value:
#			return True
#		elif (seq[start_index] == value) or (seq[final_index] == value):
#			return True
#		return False
