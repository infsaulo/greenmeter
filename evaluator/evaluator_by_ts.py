WEIGTH_PARAM = 0.85
from rec.metrics.term_freq import compute_IDF

# Do binary search
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

# Try to evaluate each tag by TS metric
def evaluate_ts(list_tags, fields, ff_structure):
	tuple_tags_evaluated = []
	for tag in list_tags:
		metric = 0.0
		for field in fields:
			list_terms = field
			#list_terms.sort()
			if(tag in list_terms):#binary_search(tag, list_terms)):
				metric += 1.0
		metric = metric/float(len(fields))
		try:
			iff_tag = ff_structure['TAG'][int(tag)]
		except KeyError:
			iff_tag = 0
		iff_tag = compute_IDF(iff_tag, ff_structure['TRAIN_LENGTH'])/float(compute_IDF(0.0, ff_structure['TRAIN_LENGTH']))
		tuple_tags_evaluated.append((tag, (WEIGTH_PARAM * metric) + ((1 - WEIGTH_PARAM) * iff_tag)))
	return tuple_tags_evaluated

