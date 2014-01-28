from evaluator.evaluator_by_ts import evaluate_ts
from rec.recommender.sum_plus_descriptive_power import *

def filter_by_threshold(tag_tuples, threshold):
	filtered_tuples = []
	remained_tuples = []

	for tuple in tag_tuples:
		if tuple[1] >= threshold:
			filtered_tuples.append(tuple)
		else:
			remained_tuples.append(tuple)
	return (filtered_tuples, remained_tuples)

def evaluate_sum_ts_combined(list_tags, fields, test_object, fs, confidences, ff_tag, k_ant, k_cons, k_r, stabilities, alpha, metric_number, number_rec, threshold, ff_structure):
	# First, evaluate according to TS metric
	first_tuples = evaluate_ts(list_tags, fields, ff_structure)
	(tuple_tags_evaluated, remained_tuples) = filter_by_threshold(first_tuples, threshold)
	best_quality_tags = []
	for tuple in tuple_tags_evaluated:
		best_quality_tags.append(tuple[0])

	(cand, metrics) = sum_plus_descriptive_power_score(test_object, best_quality_tags, fs, confidences, ff_tag, k_ant, k_cons, k_r, stabilities, alpha, metric_number, False)
	top_candidates = []
	for k,v in sorted(cand.items(), key=lambda x:x[1], reverse=True):
		top_candidates.append((k,v))
	top_candidates = top_candidates[:number_rec]
	top_candidates = dict(top_candidates)
	for index in range(len(remained_tuples)):
		if remained_tuples[index][0] in top_candidates.keys():
			new_quality = remained_tuples[index][1] + top_candidates[remained_tuples[index][0]]
			#new_quality = 0.5 + top_candidates[remained_tuples[index][0]]
			new_quality = 1.0 if new_quality > 1.0 else new_quality
			remained_tuples[index] = (remained_tuples[index][0], new_quality)

	tuple_tags_evaluated += remained_tuples

	return tuple_tags_evaluated
