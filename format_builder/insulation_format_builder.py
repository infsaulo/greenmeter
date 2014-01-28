# Implements the insulation format builder
from insulation.insulation import insulation
from format_builder.xml_format_builder import build_xml_format
from settings import *
from format_builder.unstemmer import Unstemmer
from format_builder.dictionary import Dictionary
from crawler.stop_words_vocabularies import EN_STOP_WORDS
from mapper.PorterStemmer import PorterStemmer
import string
import types

TOP_RANK = 0.5
CLOUD_THRESHOULD = 0.4

class insulation_format_builder(insulation):
	def __init__(self, input_set, output_set):
		insulation.__init__(self, input_set, output_set)

	def execute(self):
		 # Loads the vocabulary to convert back the number into their strings. 
		inv_vocabulary = dict()
		with open(self.input_set['vocabulary_filename'], 'r') as file:
			for entry in file:
				splits = entry.strip().split(" ")
				inv_vocabulary[int(splits[-1])] = reduce(lambda a, b: a + ' ' + b, splits[0:-1])
		
		for index in xrange(len(self.input_set['tag_rec_tag_filename_list'])):
			info_files_tuple = self.input_set['tag_rec_tag_filename_list'][index]
			unstemmized_tags_file = self.input_set['unstemm_filename_list'][index]
			unstemmer = Unstemmer(unstemmized_tags_file)
			name_object = info_files_tuple[0].split('/')[len(info_files_tuple[0].split('/')) - 1].strip()
			tags = []
			with open(info_files_tuple[0], 'r') as tags_file:
				for line in tags_file:
					tags.append((int(line.split(' ')[0].strip()), float(line.split(' ')[1].strip())))

			# Create average metric of topx%
			tags.sort(key=lambda x:x[1], reverse=True)
			number_tags = int(len(tags) * TOP_RANK)
			gauge_metric = 0.0
			for index in xrange(number_tags):
				gauge_metric += float(tags[index][1])
			gauge_metric /= float(number_tags)

			str_tags = []
			for tag in tags:
				str_tags.append((inv_vocabulary[tag[0]], tag[1]))
			
			filtered_tags = self.filter_evaluated_tags(str_tags)
			filtered_tags = self.unstemmize_tags_evaluated(unstemmer, filtered_tags)
			cloud_tags = map(lambda x:x[0], filtered_tags)
			rec_tags = []
			with open(info_files_tuple[1], 'r') as rec_tags_file:
				for line in rec_tags_file:
					rec_tags.append((int(line.split(' ')[0].strip()),float(line.split(' ')[1].strip())))
			str_rec_tags = []
			for tag in rec_tags:
				str_rec_tags.append((inv_vocabulary[tag[0]], tag[1]))
			rec_unstemmer = Unstemmer(self.input_set['language_unstemm_filename'])
			# INSERIR CHEKER AQUI
			(unstemmized_rec_tags, cheker_tuples) = self.unstemmize_rec_tags_evaluated(rec_unstemmer, unstemmer, str_rec_tags, cloud_tags)
			
			#filtered_rec_tags = self.filter_terms(unstemmized_rec_tags, cloud_tags, name_object.replace('+', ' '))
			filtered_rec_tags = self.filter_terms(unstemmized_rec_tags, filtered_tags, name_object.replace('+', ' '))
			doc_xml = build_xml_format(name_object, filtered_tags, filtered_rec_tags, gauge_metric)
			output_filename = self.input_set['output_dir'] + '/' + name_object
			self.output_set['output_files_list'].append(output_filename)
			with open(output_filename, 'w') as output_file:
				output_file.write(doc_xml.toprettyxml())
			with open(output_filename + '.cheker_rec_tags', 'w') as cheker_file:
				for tuple in cheker_tuples:
					cheker_file.write(tuple[0].strip() + ',' + str(tuple[1]).strip() + ',' + tuple[2].strip() + '\n');

	#def filter_terms(self, term_tuple_list, list_cloud_tags, artist_name):
	def filter_terms(self, term_tuple_list, cloud_tags_tuple, artist_name):
		list_cloud_tags = map(lambda x:x[0], cloud_tags_tuple)
		dict_cloud_tags = dict(cloud_tags_tuple)
		dirty_words_dict = Dictionary(self.input_set['black_list_filename'])
		language_dictionary = Dictionary(self.input_set['dictionary_filename'])
		
		filtered_tuple_list = []
		for tuple in term_tuple_list:
			if(tuple[0].strip() in list_cloud_tags) and (tuple[0].strip() not in artist_name):
				# NEW
				if dict_cloud_tags[tuple[0].strip()] > CLOUD_THRESHOULD:
					filtered_tuple_list.append((tuple[0].strip(), tuple[1]))
			elif (tuple[0].strip() not in artist_name) and (not dirty_words_dict.belongs_to(tuple[0].strip())) and language_dictionary.belongs_to(tuple[0].strip()):
				if(len(tuple[0].strip()) > 1) and (tuple[0].strip() not in EN_STOP_WORDS):
					filtered_tuple_list.append((tuple[0].strip(), tuple[1]))
			if len(filtered_tuple_list) >= self.input_set['num_recommends']:
				break
		
		return filtered_tuple_list

	def filter_evaluated_tags(self, tags_tuple_list):
		dirty_words_dict = Dictionary(self.input_set['black_list_filename'])
		stemm_dict = dict()
		for k,v in dirty_words_dict.dictionary.items():
			stemm_dict[self.change_field(k)] = v
		dirty_words_dict.dictionary = stemm_dict

		filtered_tuple_list = []
		for tuple in tags_tuple_list:
			if dirty_words_dict.belongs_to(tuple[0].strip()):
				filtered_tuple_list.append((tuple[0].strip(), -1.0))
			else:
				filtered_tuple_list.append((tuple[0].strip(), tuple[1]))
				
		return filtered_tuple_list

	def unstemmize_tags_evaluated(self, unstemmer, tag_tuple_list):
		new_tag_tuple_list = []
		for tuple in tag_tuple_list:
			unstemmized_tag_list = unstemmer.unstem(tuple[0])
			for unstemmized_tag in unstemmized_tag_list:
				new_tag_tuple_list.append((unstemmized_tag.strip(), tuple[1]))
		return new_tag_tuple_list	

	# PONTO DE MODIFICACAO PARA ESCOLHER TAG RECOMENDADA QUE SEJA A MAIS POPULAR. EXIGE TREINO SEM STEMMIZACAO
	def unstemmize_rec_tags_evaluated(self, static_unstemmer, dynamic_unstemmer, tag_tuple_list, cloud_tag_tuples):
		new_tag_tuple_list = []
		cheker_tag_list = []
		for tuple in tag_tuple_list:
			dynamic_tag_list = dynamic_unstemmer.unstem(tuple[0])
			if dynamic_tag_list[0].strip() in cloud_tag_tuples:
				new_tag_tuple_list.append((dynamic_tag_list[0].strip(), tuple[1]))
				if(float(tuple[1] > 0.0)):
					cheker_tag_list.append((dynamic_tag_list[0].strip(), tuple[1], 'CLOUD'))
			else:
				unstemmized_tag_list = static_unstemmer.unstem(tuple[0])
				new_tag_tuple_list.append((unstemmized_tag_list[0].strip(), tuple[1]))
				if(float(tuple[1]) > 0.0):
					cheker_tag_list.append((unstemmized_tag_list[0].strip(), tuple[1], ''))
					
#			print "STEMMED TAG: " + tuple[0]
#			print unstemmized_tag_list
			# COLOCAR AQUI UMA FUNCAO QUE RECEBE O TREINO NAO STEMMIZADO E A LISTA DE TAGS RECOMENDADAS E ESCOLHER AQUELA
			# DA LISTA MAIS FREQUENTE
#			new_tag_tuple_list.append((unstemmized_tag_list[0].strip(), tuple[1]))
#			if(float(tuple[1]) > 0.0):
#				if unstemmized_tag_list[0].strip() in cloud_tag_tuples:
#					cheker_tag_list.append((unstemmized_tag_list[0].strip(), tuple[1], 'CLOUD'))
#				else:
#					cheker_tag_list.append((unstemmized_tag_list[0].strip(), tuple[1], ''))
		return (new_tag_tuple_list, cheker_tag_list)	
	
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
				num = float(term[0])
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
