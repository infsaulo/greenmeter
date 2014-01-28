# Description: settings.py defines constants for each component
# Colaborators: Saulo Ricci
# Date: 2010/08/24

import os

# Some constants for crawler
CRAWLER_DIR = os.getcwd() + "/crawler"
CRAWLER_OUTPUT_DIR = CRAWLER_DIR + "/outputs"

CRAWLER_SEEDS_FILENAME = CRAWLER_DIR + "/seeds"

LASTFM_CRAWLER_API_KEY = 'ce5769694bce1d32dff787b0a33daf1a'

# Input datas dictionary for the insulation crawler
CRAWLER_INPUT_DICT = {
	'lastfm_api_key': LASTFM_CRAWLER_API_KEY,
	'seeds_filename': CRAWLER_SEEDS_FILENAME,
	'output_dir': CRAWLER_OUTPUT_DIR,
}

# Output datas dictionary for the insulation crawler
CRAWLER_OUTPUT_DICT = {
	'output_files_list': []
}

# Some constants for insulation mapper
MAPPER_DIR = os.getcwd() + "/mapper"
MAPPER_OUTPUT_DIR = MAPPER_DIR + "/outputs"
MAPPER_VOCABULARY_FILENAME = MAPPER_DIR + "/stemmized_dictionary"

# Input datas dictionary for the insulation mapper
MAPPER_INPUT_DICT = {
	'xml_filename_list': [],
	'output_dir': MAPPER_OUTPUT_DIR,
	'aho_corasick_filename': MAPPER_DIR + "/stored_prefix_tree",
	'vocabulary_filename': MAPPER_VOCABULARY_FILENAME
}

# Output datas dictionary for the insulation mapper
MAPPER_OUTPUT_DICT = {
	'output_files_list': []
}


# Some constants for insulation recommender
RECOMMENDER_DIR = os.getcwd() + "/rec"
RECOMMENDER_OUTPUT_DIR = RECOMMENDER_DIR + "/outputs"

# Input datas dictionary for the insulation recommender
RECOMMENDER_INPUT_DICT = {
	'output_dir': RECOMMENDER_OUTPUT_DIR,
	'train_filename': RECOMMENDER_DIR + "/recommender/lastfm_stemm_2",
	'test_inputtag_filename_list': [],
	'threshold': 0.5,
	'min_support': 2,
	'min_confidence': 0.5,
	'k_ant': 5,
	'k_cons': 5,
	'k_r': 1,
	'alpha': 0.9,
	'num_recommends': 100,
	'metric_number': 0,
	'confidences_status': 1,
	'confidences_filename': RECOMMENDER_DIR + "/recommender/confidences_file",
	'fs_file_status': 1,
	'fs_filename': RECOMMENDER_DIR + "/recommender/fs_file",
	'ff_status': 1,
	'ff_filename': RECOMMENDER_DIR + "/recommender/ff_file",
}

# Output datas dictionary for the insulation recommender
RECOMMENDER_OUTPUT_DICT = {
	'output_files_list': []
}

# Some constants for insulation evaluator
EVALUATOR_DIR = os.getcwd() + "/evaluator"
EVALUATOR_OUTPUT_DIR = EVALUATOR_DIR + "/outputs"

# Input datas dictionary for the insulation evaluator
EVALUATOR_INPUT_DICT = {
	'test_filename_list': [],
	'output_dir': EVALUATOR_OUTPUT_DIR,
	'threshold': 0.5,
	'min_support': 2,
	'min_confidence': 0.5,
	'k_ant': 5,
	'k_cons': 5,
	'k_r': 1,
	'alpha': 0.9,
	'num_recommends': 100,
	'metric_number': 0,
	'confidences_filename': RECOMMENDER_DIR + "/recommender/confidences_file",
	'vocabulary_filename': MAPPER_VOCABULARY_FILENAME, 
	'fs_filename': RECOMMENDER_DIR + "/recommender/fs_file",
	'ff_filename': RECOMMENDER_DIR + "/recommender/ff_file"
}

# Output datas dictionary for the insulation evaluator
EVALUATOR_OUTPUT_DICT = {
	'output_files_list': []
}

# Some constants for insulation format builder
FORMAT_BUILDER_DIR = os.getcwd() + "/format_builder"
FORMAT_BUILDER_OUTPUT_DIR = FORMAT_BUILDER_DIR + "/outputs"

# Input datas dictionary for the insulation format builder
FORMAT_BUILDER_INPUT_DICT = {
	'tag_rec_tag_filename_list': [],	
	'unstemm_filename_list': [],
	'language_unstemm_filename': FORMAT_BUILDER_DIR + '/unstemm',
	'black_list_filename': FORMAT_BUILDER_DIR + '/black_list',
	'dictionary_filename': FORMAT_BUILDER_DIR + '/en',
	'output_dir': FORMAT_BUILDER_OUTPUT_DIR,
	'vocabulary_filename': MAPPER_VOCABULARY_FILENAME,
	'num_recommends': 5
}

# Output datas dictionary for the insulation format builder
FORMAT_BUILDER_OUTPUT_DICT = {
	'output_files_list': []
}
