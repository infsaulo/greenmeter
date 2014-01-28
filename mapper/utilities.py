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

def get_vocabulary_and_keys_voc(voc_filename):
	with open(voc_filename, 'r') as voc_file:
		dict_terms = dict()
		for line in voc_file:
			splited_terms = [term + ' ' for term in line.strip().split(' ')]
			dict_terms[''.join(splited_terms[:len(splited_terms) - 1]).strip()] = int(splited_terms[len(splited_terms) - 1].strip())
		keys_voc = dict_terms.keys()
		keys_voc.sort()

	return (dict_terms, keys_voc)	
