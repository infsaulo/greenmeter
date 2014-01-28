# Implements the insulation evaluator
from insulation.insulation import insulation
from evaluator.evaluator_by_ts import evaluate_ts
from evaluator.evaluator_by_sum_ts_combined import evaluate_sum_ts_combined
from settings import *
from object import *
import json
import math
from collections import defaultdict
from rec.recommender.sum_plus_descriptive_power import *

class insulation_evaluator(insulation):
	def __init__(self, input_set, output_set):
		insulation.__init__(self, input_set, output_set)

	def execute(self):
		# Parameters
		minsup = float(self.input_set['min_support'])
		minconf = float(self.input_set['min_confidence'])
		k_ant = float(self.input_set['k_ant'])
		k_cons = float(self.input_set['k_cons'])
		k_r = float(self.input_set['k_r'])
		alpha = float(self.input_set['alpha'])
		num_rec = int(self.input_set['num_recommends'])
		metric_number = int(self.input_set['metric_number'])
		confidences_filename = self.input_set['confidences_filename']
		fs_filename = self.input_set['fs_filename']
		ff_filename = self.input_set['ff_filename']
		threshold = self.input_set['threshold']
		
		ff = defaultdict() 
		with open(ff_filename, 'r')  as file:
			ff = json.loads(file.read())
		new_ff = self.convert_to_math(ff)

		fs = defaultdict()
		with open(fs_filename, 'r') as file:
			fs = json.loads(file.read())
		new_fs = self.convert_to_math(fs)

		confidences = defaultdict()
	
		with open(confidences_filename, 'r') as file:
			confidences = json.loads(file.read())
		new_confidences = self.convert_to_math(confidences)

		for test_filename in self.input_set['test_filename_list']:
			print 'Evaluating ' + test_filename
			tags = []
			fields_list = []
			test_object = None
			stabilities = {}
			with open(test_filename, 'r') as input_file:
				
				test_objects = get_all_concats_TF_weighted(input_file)
				test_object = test_objects[test_filename.split('/')[len(test_filename.split('/')) - 1].split('.')[1].strip()]
			
			with open(test_filename, 'r') as input_file:
				read_string = input_file.read().strip()
				fields = [field.strip() for field in read_string.split('|')]
				tags = self.get_all_derivated_tags(self.convert_math([term for term in fields[1].split(' ')[1:]]))

				fields_list.append(self.convert_math([term.strip() for term in fields[2].strip().split(' ')[1:]]))
				fields_list.append(self.convert_math([term.strip() for term in fields[3].strip().split(' ')[1:]]))
			

			#tags_evaluated = evaluate_ts(tags, fields_list, new_ff)
	
			tags_evaluated = evaluate_sum_ts_combined(tags, fields_list, test_object, new_fs, new_confidences, new_ff["TAG"], k_ant, k_cons, k_r, stabilities, alpha, metric_number, num_rec, threshold, new_ff)
			
			output_filename = self.input_set['output_dir'] + '/' + test_filename.split('/')[len(test_filename.split('/')) - 1].split('.')[1].strip()
			with open(output_filename, 'w') as out_file:
				for tuple in tags_evaluated:
					out_file.write(str(tuple[0]) + " " + str(tuple[1]) + "\n")
			self.output_set['output_files_list'].append(output_filename);

	def get_all_derivated_tags(self, tags):
		tags = list(set(tags))
		vocabulary = self.get_vocabulary(self.input_set['vocabulary_filename'])
		inv_vocabulary = dict()
		for k,v in vocabulary.items():
			inv_vocabulary[v] = k

		keys_voc = vocabulary.keys()
		keys_voc.sort()

		set_tags = set()
		for tag in tags:
			str_tag = inv_vocabulary[tag]
			str_term_list = self.get_term_list(str_tag)
			for str_term in str_term_list:
				if binary_search(str_term, keys_voc):
					set_tags.add(vocabulary[str_term])
		
		return list(set_tags)

	def get_term_list(self, words):
		word_list = [words]
		for word in words.split(" "):
			if word == word_list[0]:
				return word_list

			if word != "" and word != " ":
				word_list.append(word.strip())

		return word_list

	def convert_math(self, term_list):
		math_list = []
		for term in term_list:
			try:
				converted_term = int(term)
				math_list.append(converted_term)
			except ValueError:
				pass
		
		return math_list	

	def convert_to_math(self, dict_object):
		converted_dict = defaultdict()

		# Outter loop
		for (key, object) in dict_object.items():
			new_key = None
			# The key type is a integer
			try:
				new_key = int(key)
			except ValueError:
				new_key = key
		
			new_object = None
			if object.__class__ in types.StringTypes:
				if '.' not in object:
					new_object = int(object)
				else:
					new_object = float(object)
			elif object.__class__ == types.IntType:
				new_object = object
			elif object.__class__ == types.FloatType:
				new_object = object

			# object is a dictionary, then go to inner loop
			else:
				new_object = defaultdict()
				for (inner_key, inner_object) in object.items():
					new_inner_key = None
					try:
						new_inner_key = int(inner_key)
					except ValueError:
						new_inner_key = inner_key
				
					new_inner_object = None
					if inner_object.__class__ == types.FloatType:
						new_inner_object = inner_object
					elif inner_object.__class__ == types.IntType:
						new_inner_object = inner_object
					elif '.' not in inner_object:
						new_inner_object = int(inner_object)
					else:
						new_inner_object = float(inner_object)
					new_object[new_inner_key] = new_inner_object

			converted_dict[new_key] = new_object
	
		return converted_dict

	def get_vocabulary(self, voc_filename):
		with open(voc_filename, 'r') as voc_file:
			dict_terms = dict()
			for line in voc_file:
				splited_terms = [term + ' ' for term in line.strip().split(' ')]
				dict_terms[''.join(splited_terms[:len(splited_terms) - 1]).strip()] = int(splited_terms[len(splited_terms) - 1].strip())

		return dict_terms	
	
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
