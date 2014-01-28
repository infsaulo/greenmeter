# Description: insultation_recommender.py implements a recommender that be insulated
# Author: Saulo Marques Ribeiro Ricci
# Date: 2010/08/31
from insulation.insulation import insulation
from recommender.sum_plus_descriptive_power import sum_plus_e_recommender_func
from settings import *

import commands

class insulation_recommender(insulation):
	def __init__(self, input_set, output_set):
		insulation.__init__(self, input_set, output_set)

	def execute(self):
		output_file_list = sum_plus_e_recommender_func(self.input_set)
		self.output_set['output_files_list'] = output_file_list
