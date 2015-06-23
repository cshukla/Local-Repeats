
#!/usr/bin/env python

from optparse import OptionParser
import os, sys

#########################################################
# rmsk_split.py
#
# This script inputs the output of repeat masker and 
# splits into several files one each for a repeat family. 
# The output files as saved as '.bed' files in the same 
# directory as the input file.
#########################################################
def main():
	usage = 'usage:%prog [options] <input_file>'
	parser = OptionParser(usage)
	(options, args) = parser.parse_args()

	if len(args)!=1:
		parser.error(usage)
	else:
		input_file = open(args[0])
		input_dir = '/'.join(args[0].split('/')[:-1])
		file_name = args[0].split('/')[-1].split('.')[0]
		output_dir = '/'.join([input_dir, file_name])

	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	repeats = {}
	for line in input_file:
		if line[0] != '#':
			line = line.strip().split('\t')
			repeat_family = line[-1].split('"')[1]
			repeat_family = repeat_family.split(':')[1].split('=')
			repeat_family = ''.join(repeat_family)
			chrom = line[0]
			start = line[3]
			end = line[4]
			strand = line[6]
			out_line = '\t'.join([chrom, start, end, strand, '\n'])
			if repeat_family not in repeats:
				repeats[repeat_family] = ''

			repeats[repeat_family] += out_line

	print >> sys.stderr, 'Finished reading all the repeats into the hash table'
	print >> sys.stderr, 'Now writing individual files to %s ...' %(output_dir)
	for key in repeats.keys():
		out_file = open('/'.join([output_dir, key]) + '.bed', 'w')
		print >> out_file, repeats[key]
		out_file.close()

#########################################################
# main()
#########################################################
if __name__ == '__main__':
	main()