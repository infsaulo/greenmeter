# Description: insulation_crawler.py implements a crawler that be insulted.
# Colaborators: Saulo Ricci
# Date: 2010/08/23
import commands
from insulation.insulation import insulation
from settings import *
from xml.dom.minidom import Document
from stop_words_vocabularies import *
import lastfm
import re
import urllib2
import string as string_mod

import sys
sys.path.append('/home/vod/saulomrr/Documents/Projeto/db_recommender_builder/nltk')
import nltk

class insulation_crawler(insulation):
	def __init__(self, input_set, output_set):
		insulation.__init__(self, input_set, output_set)

	def execute(self):
		# Now is ready to executes the crawling
		self.safety_crawling()	

	def safety_crawling(self):
		self.check_seeds(self.input_set['seeds_filename'])
		
		# Crawling
		self.crawls_artist_info()

	def crawls_artist_info(self):
		lastfm_api = lastfm.Api(self.input_set['lastfm_api_key'])
		list_artist = []
		with open(self.input_set['seeds_filename'], 'r') as file:
			for artist in file:
				artist_name = artist.replace("Ar:", "").replace("+", " ").lower().strip()
				artist_api = lastfm_api.get_artist(artist_name)
				artist_name = artist_api.name
				print artist_name
				artist_tags = []

				# Get tags by +tags page
				artist_tag_page = urllib2.Request(url = 'http://www.last.fm/music/' + artist.replace("Ar:", "").strip() + '/+tags')
				artist_tag_info = urllib2.urlopen(artist_tag_page)
				artist_info = artist_tag_info.read()
				compile_line = re.compile('<.*a.*href="/tag/.*".*class="cloudItem".*rel="tag".*>(.*).*<.*/a.*>')
				result_match = compile_line.findall(artist_info)
				punctuation = string_mod.punctuation.replace('-','')
				for tag in result_match:
					tag_buffer = ""
					for car in tag:
						try:
							if(car not in punctuation):
							 	tag_buffer += car.encode('ascii')
						except UnicodeEncodeError:
							pass
						except UnicodeDecodeError:
							pass
					tag_buffer = tag_buffer.strip()
					if tag_buffer != "":
						artist_tags.append(tag_buffer)

				# Get tags by api
				#artist_tags_api = []
				#for tag in artist_api.top_tags:
				#	tag_buffer = ""
				#	for car in tag.name:
				#		try:
				#			if(car not in punctuation):
				#				tag_buffer += car.encode('ascii')
				#		except UnicodeEncodeError:
				#			pass
				#	tag_buffer = tag_buffer.strip()
				#	if tag_buffer != "":
				#		artist_tags_api.append(tag_buffer)

				# Union of tags gotten by api and +tags page
				result_tags = list(set(artist_tags))

				artist_description_buffer = ""
				desc_artist = nltk.clean_html(artist_api.bio.content)
				for car in desc_artist:
					try:
						artist_description_buffer += car.encode('ascii')
					except UnicodeEncodeError:
						pass
					except UnicodeDecodeError:
						pass

				artist_description_buffer = artist_description_buffer.strip()
				if artist_description_buffer != "":
					artist_description = artist_description_buffer

#				artist_shouts = []
#				index = 0
#				for shout in artist_api.shouts:
#					shout_buffer = ""
#					for car in shout.body:
#						try:
#							shout_buffer += car.encode('ascii')
#						except UnicodeEncodeError:
#							pass
#					shout_buffer = shout_buffer.strip()
#					if (shout_buffer != "") and self.is_english_vocabulary(shout_buffer):
#						artist_shouts.append(shout_buffer)
#						index = index + 1

#					if index > 100:
#						break

				# Create a XML file related to current artist in the auxiliary dir. The name
				with open(self.input_set['output_dir'] + '/' + artist.replace('Ar:', 'lastfm.ar.').strip(), 'w') as xml_file:
					doc_xml = Document()
					lastfm_object = doc_xml.createElement("lastfm-object")
					doc_xml.appendChild(lastfm_object)
					t = doc_xml.createElement("t")
					t_str = doc_xml.createTextNode("ARTIST")
					t.appendChild(t_str)
					lastfm_object.appendChild(t)
					name = doc_xml.createElement("name")
					name_str = doc_xml.createTextNode(artist_name)
					name.appendChild(name_str)
					lastfm_object.appendChild(name)
					wikiText = doc_xml.createElement("wikiText")
					wikiText_str = doc_xml.createTextNode(artist_description)
					wikiText.appendChild(wikiText_str)
					lastfm_object.appendChild(wikiText)
					tags = doc_xml.createElement("tags")
					tags.setAttribute("class", "list")
					for tag in result_tags:
						string = doc_xml.createElement("string")
						string_str = doc_xml.createTextNode(tag.strip())
						string.appendChild(string_str)
						tags.appendChild(string)
					lastfm_object.appendChild(tags)
#					comments = doc_xml.createElement("comments")
#					comments.setAttribute("class", "list")
#					for comment in artist_shouts:
#						string = doc_xml.createElement("string")
#						string_str = doc_xml.createTextNode(comment.strip())
#						string.appendChild(string_str)
#						comments.appendChild(string)
#					lastfm_object.appendChild(comments)
					#print "Gotcha!"	
					xml_file.write(doc_xml.toprettyxml())
					self.output_set['output_files_list'].append(self.input_set['output_dir'] + '/' + artist.replace('Ar:', 'lastfm.ar.').strip())
	
	def is_english_vocabulary(self, entry):
		english_stop_words_vocabulary = EN_STOP_WORDS
		entry_words = entry.split(" ")
		number_en_stop_words = 0
		for word in entry_words:
			if self.binary_search(word, english_stop_words_vocabulary):
				number_en_stop_words += 1
			if number_en_stop_words == 3:
				return True
		return False
			
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

	def check_seeds(self, seeds_filename):
		seeds_crawled = commands.getoutput("ls " + self.input_set['output_dir'])
		if seeds_crawled != "":
			seeds_crawled_list = seeds_crawled.split('\n')
			seeds_requested = commands.getoutput("cat " + seeds_filename)
			seeds_requested = seeds_requested.replace("Ar:", "lastfm.ar.")
			seeds_requested_list = seeds_requested.split('\n')
			seeds_gonna_crawl_list = []
			for seed in seeds_requested_list:
				if seed not in seeds_crawled_list:
					seeds_gonna_crawl_list.append(seed)
				# Seeds are crawled, so append in output_set to mapper transform the crawled seed
				else:
					self.output_set['output_files_list'].append(self.input_set['output_dir'] + "/" + seed.strip())
			# Update seeds
			with open(seeds_filename, 'w') as seeds_file:
				for updated_seed in seeds_gonna_crawl_list:
					seeds_file.write(updated_seed.replace("lastfm.ar.", "Ar:") + '\n')	

	def get_list_crawled(self):
		result = commands.getoutput("ls " + self.input_set['auxiliary_dir'])
		if result != "":
			return result.split('\n')
		
		return []
