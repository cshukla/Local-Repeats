#!/usr/bin/env python

from optparse import OptionParser
import os, sys

#########################################################
# lr_motifs.py
#
# This script inputs the output of repeat masker and 
# splits into several files one each for a repeat family. 
# The output files as saved as '.bed' files in the same 
# directory as the input file.
#########################################################
def main():
	usage = 'usage:%prog [options] <gff_file>'
	parser = OptionParser(usage)
	(options, args) = parser.parse_args()

	if len(args)!=1:
		parser.error(usage)
	else:
		gff_file = open(args[0])

	repeat_tf_pairs = {}
	for line in gff_file:
		a = line.strip().split('\t')
		repeat_name = a[0]
		tf = a[-1]
		repeat_tf_pair = (tf, repeat_name)
		if repeat_tf_pair not in repeat_tf_pairs.keys():
			repeat_tf_pairs[repeat_tf_pair] = 1

		repeat_tf_pairs[repeat_tf_pair]+=1	 

	for pair in repeat_tf_pairs.keys():
		tf, repeat_name = pair[0], pair[1]
		number_of_motifs = repeat_tf_pairs[pair]
		out_line = '\t'.join([tf, repeat_name, str(number_of_motifs)])
		print out_line

#########################################################
# main()
#########################################################
if __name__ == '__main__':
	main()