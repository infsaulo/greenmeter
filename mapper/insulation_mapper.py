# Description: insulation_mapper.py implements a mapper that be insulated
# Author: Saulo Marques Ribeiro Ricci
# Date: 2010/08/24
import commands
from insulation.insulation import insulation
from mapper.mapper_lfm_artist import mapper_lfm_artist
from settings import *

class insulation_mapper(insulation, mapper_lfm_artist):
	def __init__(self, input_set, output_set):
		insulation.__init__(self, input_set, output_set)

	def execute(self):
		not_mapped_file_list = []
		mapped_file_list = []
		# Check the output of mapped files to look up for any file that corresponds in output files of the crawler
		result = commands.getoutput("ls " + self.input_set['output_dir'] + "/test.*")
		result_split = []
		if result != "":
			result_split = result.split('\n')
			result_split.sort()
			for entry in self.input_set['xml_filename_list']:
				modified_entry = self.input_set['output_dir'] + "/test." + entry.split("lastfm.ar.")[1].lower().strip()
				if self.binary_search(modified_entry, result_split) == False:
					not_mapped_file_list.append(entry)
				else:
					mapped_file_list.append((modified_entry, modified_entry.replace('test.', 'inputtag.'), modified_entry.replace('test.', 'unstemmtag.')))
					
		if not_mapped_file_list != []:
			print "I gonna map!"
			mapper_lfm_artist.__init__(self, not_mapped_file_list, self.input_set['output_dir'], self.input_set['aho_corasick_filename'], self.input_set['vocabulary_filename'])
			self.output_set['output_files_list'] = self.output_file_list + mapped_file_list
		else:
			self.output_set['output_files_list'] = mapped_file_list
			
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
