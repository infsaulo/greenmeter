import sys, os
import random
import time
import math
import json
import types
from collections import defaultdict
from operator import itemgetter

from ..object.textual_features_concat import get_all_concats_TF_weighted
from ..metrics.term_freq import *
from ..metrics.cooccur import compute_cooccur_and_entropy_field
from ..personalized.inout import load_list, print_list

from xml.dom.minidom import Document
from ..recommender.sum_plus import sum_plus_score
from util import *

# Computa metricas e recomenda
#
# Entrada: test_object: atributos textuais do objeto
#              intags: lista de tags de entrada
#                  fs: Feature Spread dos atributos textuais considerados
#         confidences: Confiancas das regras de associacao
#                ftag: frequencia em que uma palavra aparece como tag
#                  k*, alpha, beta: parametros de ajuste
#      metric_number: valor em [0,3] que identifica a metrica de poder descritivo utilizada
#
# Saida: Tags e seus valores de relevancia estimados

def convert_to_math(dict_object):
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

def get_average(list_number):
	average = 0.0
	for entry in list_number:
		average += entry
	
	return average/len(list_number)

def get_dev(list_number):
	dev = 0.0
	avg = get_average(list_number)
	for entry in list_number:
		dev += math.pow(entry - avg, 2)
	
	return(avg, math.sqrt(dev))
		
def sum_plus_descriptive_power_score(test_object, intags, fs, confidences, ftag, k_ant, k_cons, k_r, stabilities, alpha, metric_number, is_recommender):
    beta = 1.0 - alpha
    candidates = sum_plus_score(intags, confidences, ftag, k_ant, k_cons, k_r, stabilities, is_recommender)

    if len(candidates) > 0:
        max_conf_score = max(candidates.values())
        for c in candidates:
            candidates[c] *= (alpha/max_conf_score)

    metrics = compute_internal_frequency_metrics_normalized(test_object, fs)
    
    new_candidates = {}
    for t in metrics:
	if not is_recommender:
	        if t not in intags:
    			new_candidates[t] = metrics[t][metric_number]
	else:
		new_candidates[t] = metrics[t][metric_number]

    if len(new_candidates) > 0:
        maxv = max(new_candidates.values())
    else:
        maxv = 1.0
    for t in new_candidates:
        candidates[t] += (beta * new_candidates[t] / maxv)

    return (candidates, metrics)

def sum_plus_e_recommender_func(input_dict):
	train_filename = input_dict['train_filename']
	minsup = float(input_dict['min_support'])
	minconf = float(input_dict['min_confidence'])
	k_ant = float(input_dict['k_ant'])
	k_cons = float(input_dict['k_cons'])
	k_r = float(input_dict['k_r'])
	alpha = float(input_dict['alpha'])
	num_rec = int(input_dict['num_recommends'])
	metric_number = int(input_dict['metric_number'])
	confidence_status = int(input_dict['confidences_status'])
	confidences_filename = input_dict['confidences_filename']
	fs_file_status = int(input_dict['fs_file_status'])
	fs_filename = input_dict['fs_filename']
	ff_status = input_dict['ff_status']
	ff_filename = input_dict['ff_filename']
	threshold = float(input_dict['threshold'])
    
	if metric_number < 0 or metric_number > 3:
   		print >>sys.stderr, "Metric number must be between 0 and 3"
	   	sys.exit(-1)

	if (fs_file_status == 0):
   		#Computa Feature Spread de cada atributo textual da lista passada como parametro 
	   	fs = compute_FS(train_filename, ["TITLE", "DESCRIPTION", "TAG"])
		with open(fs_filename, 'w') as file:
			file.write(json.dumps(fs))

	if(ff_status == 0):
   		#ff = Feature Frequency (frequencia de uma palavra em uma Textual Feature (ex. Tags)
	    	(ff, n) = compute_FF_and_train_length(train_filename, ["TAG"])
		ff['TRAIN_LENGTH'] = n
		with open(ff_filename, 'w') as file:
			file.write(json.dumps(ff))
   
	if(confidence_status == 0):
   	#ff = Feature Frequency (frequencia de uma palavra em uma Textual Feature (ex. Tags)
		(ff, n) = compute_FF_and_train_length(train_filename, ["TAG"])
	
		ff['TRAIN_LENGTH'] = n
		print "Step #1 ready!"
   
		#computa as confiancas das regras de associacao obtidas do conjunto de objetos de treino
   		confidences = compute_cooccur_and_entropy_field(train_filename, ff["TAG"], minsup, minconf, "TAG")[0]
		print "Step #2 ready!"
	
		with open(ff_filename, 'w') as file:
			file.write(json.dumps(ff))
	
		with open(confidences_filename, 'w') as file:
			file.write(json.dumps(confidences))
    
	ff = defaultdict() 
	with open(ff_filename, 'r')  as file:
		ff = json.loads(file.read())
	new_ff = convert_to_math(ff)

	fs = defaultdict()
	with open(fs_filename, 'r') as file:
		fs = json.loads(file.read())
	new_fs = convert_to_math(fs)

	confidences = defaultdict()
	with open(confidences_filename, 'r') as file:
		confidences = json.loads(file.read())
	new_confidences = convert_to_math(confidences)

	# Loops for each tuple of file(test_file, inputtag_file)
	output_file_list = []
	
	for tuple_filename in input_dict['test_inputtag_filename_list']:
#		fields_list = list()
#		with open(tuple_filename[0], 'r') as input_file:
#			read_string = input_file.read().strip()
#			fields = [field.strip() for field in read_string.split('|')]
#			fields_list.append(convert_math([term.strip() for term in fields[2].strip().split(' ')[1:]]))
#			fields_list.append(convert_math([term.strip() for term in fields[3].strip().split(' ')[1:]]))

		with open(tuple_filename[0], 'r') as test_file:
			with open(tuple_filename[1], 'r') as input_tags:
				test_objects = get_all_concats_TF_weighted(test_file)
				stabilities = {}
	   			output_filename = input_dict['output_dir'] + '/' + tuple_filename[0].split("test.")[1].strip()
				output_file_list.append(output_filename.strip())
				print "Appended output: " + output_filename.strip()
				with open(output_filename, 'w') as output_file:
					for line in input_tags:
			   			split = load_list(line.strip(), " ")
					   	intags = [x for x in split[2:]]
						int_intags = []
						for tag in intags:
							int_intags.append(int(tag.strip()))
									

#						first_tuples = evaluate_ts(int_intags, fields_list, new_ff["TAG"])
#						(tuple_tags_evaluated, remained_tuples) = filter_by_threshold(first_tuples, threshold)
#						best_quality_tags = []
#						for tuple in tuple_tags_evaluated:
#							best_quality_tags.append(tuple[0])

						rid = split[1]

						test_object = test_objects[rid]
       
						#Gera tags candidatas e as ordena pelo ranking produzido
						(cand, metrics) = sum_plus_descriptive_power_score(test_object, int_intags, new_fs, new_confidences, new_ff["TAG"], k_ant, k_cons, k_r, stabilities, alpha, metric_number, True)
						# Retrieve all tags and their metrics
#						terms = metrics.keys()
#						terms.sort()
						
#						rec = get_top_ranked(cand, num_rec)
#						recs = []
						top_candidates_keys = get_top_ranked(cand, num_rec)
						print top_candidates_keys
#						for k,v in sorted(cand.items(), key=lambda x:x[1], reverse=True):
#							top_candidates.append((k,v))
#						top_candidates = top_candidates[:num_rec]
#						top_candidates = dict(top_candidates)
						
#						for rec_tag in rec:
#							if binary_search(rec_tag, terms):
								# If the term is not available in ff["TAG"] it means that tag
								# occour only in this object
#								iff_tag = None
#								try:
#									iff_tag = new_ff['TAG'][rec_tag]
#								except KeyError:
#									iff_tag = 0.0
#								iff_tag = compute_IDF(iff_tag, new_ff['TRAIN_LENGTH'])/compute_IDF(0.0, new_ff['TRAIN_LENGTH'])
#								recs.append((rec_tag, metrics[rec_tag][0], 0.0))
#							else:
#								recs.append((rec_tag, 0, 0))
#						tags_evaluated = evaluate_ts(top_candidates_keys, fields_list, new_ff)
						
						for top_candidate in top_candidates_keys:
							output_file.write(str(top_candidate).strip() + " " + str(cand[top_candidate]).strip() + "\n")
#						for rec_tag in recs:
#							output_file.write(str(rec_tag[0]) + " " + str(WEIGHT_PARAM*rec_tag[1] + (1 - WEIGHT_PARAM)*rec_tag[2]) + "\n")
	return output_file_list

def binary_search(value, seq):
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
