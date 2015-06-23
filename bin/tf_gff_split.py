#!/usr/bin/env python

from optparse import OptionParser
import os, sys

#########################################################
# tf_gff_split.py
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
		input_dir = '/'.join(args[0].split('/')[:-1])
		file_name = args[0].split('/')[-1].split('.')[0]
		output_dir = '/'.join([input_dir, file_name])

	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	tfs = {}
	for line in gff_file:
		a = line.strip().split('\t')
		tf = a[-1]
		out_line = line
		if tf not in tfs:
			tfs[tf] = open('/'.join([output_dir, tf]) + '.gff', 'w')

		print >> tfs[tf], line.strip()

#	print >> sys.stderr, 'Finished reading all the transcription factors into the hash table'
#	print >> sys.stderr, 'Now writing individual files to %s ...' %(output_dir)
#	for key in tfs.keys():
#		out_file = open('/'.join([output_dir, key]) + '.gff', 'w')
#		print >> out_file, '\n'.join(tfs[key])
#		out_file.close()

#########################################################
# main()
#########################################################
if __name__ == '__main__':
	main()