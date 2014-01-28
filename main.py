# Description: main.py implements all steps to crawls, maps, and recommends the tags for some pages at lastfm
# Author: Saulo Marques Ribeiro Ricci
# Date: 2010/08/24

from crawler.insulation_crawler import insulation_crawler
from mapper.insulation_mapper import insulation_mapper
from rec.insulation_recommender import insulation_recommender
from evaluator.insulation_evaluator import insulation_evaluator
from format_builder.insulation_format_builder import insulation_format_builder
from settings import *
import time

def crawling(crawler):
	crawler.execute()
	for entry in crawler.output_set['output_files_list']:
		print entry
def mapping(mapper):
	mapper.execute()
	for entry in mapper.output_set['output_files_list']:
		print entry

def evaluating(evaluator):
	evaluator.execute()
	for entry in evaluator.output_set['output_files_list']:
		print entry

def building_format(format_builder):
	format_builder.execute()
	for entry in format_builder.output_set['output_files_list']:
		print entry

def main():
	start_time = time.time()
	# Do crawl job
	crawler = insulation_crawler(CRAWLER_INPUT_DICT, CRAWLER_OUTPUT_DICT)
	crawling(crawler)

	# Do map job
	for entry in crawler.output_set['output_files_list']:
		MAPPER_INPUT_DICT['xml_filename_list'].append(entry)
	mapper = insulation_mapper(MAPPER_INPUT_DICT, MAPPER_OUTPUT_DICT)
	mapping(mapper)
	
	# Do recommend job
	for mapped_tuple in mapper.output_set['output_files_list']:
		RECOMMENDER_INPUT_DICT['test_inputtag_filename_list'].append((mapped_tuple[0], mapped_tuple[1]))
	recommender = insulation_recommender(RECOMMENDER_INPUT_DICT, RECOMMENDER_OUTPUT_DICT)
	recommender.execute()
	
	# Do evaluating job
	for mapped_tuple in mapper.output_set['output_files_list']:
		EVALUATOR_INPUT_DICT['test_filename_list'].append(mapped_tuple[0])
	evaluator = insulation_evaluator(EVALUATOR_INPUT_DICT, EVALUATOR_OUTPUT_DICT)
	evaluating(evaluator)
	
	for file in recommender.output_set['output_files_list']:
		print file
	# Do building format
	for index in range(len(recommender.output_set['output_files_list'])):
		FORMAT_BUILDER_INPUT_DICT['tag_rec_tag_filename_list'].append((evaluator.output_set['output_files_list'][index], recommender.output_set['output_files_list'][index]))
		FORMAT_BUILDER_INPUT_DICT['unstemm_filename_list'].append(mapper.output_set['output_files_list'][index][2])

	format_builder = insulation_format_builder(FORMAT_BUILDER_INPUT_DICT, FORMAT_BUILDER_OUTPUT_DICT)
	building_format(format_builder)
	
	end_time = time.time()
	print str(end_time - start_time)

if __name__ == "__main__":
	main()
