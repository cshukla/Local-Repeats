#!/usr/bin/env python

from optparse import OptionParser
import os, sys

#############################################################
# filter_rm_gff.py
#
# This script filters the GFF file obtained by running
# RepeatMasker. There is also an option to split the final
# filtered file by repeat name. Currently, I am using two
# filters to remove unwanted entries. 
#
# Filter 1: Remove any entries longer than the consensus 
# repeat sequence length.
#
# Filter 2: Remove any entries that are not "local repeats";
# i.e. if the start and end of the entry is not in the locus
# of the local repeat +/- 10 kb; discard it.
#
# Output 2 files: 1 file with just filter 1 applied and the
# other with both the filters applied. Output the format in
# GFF file format.
#
#
# Future options: Add a filter based on score?
#############################################################
def main():
	usage = 'usage:%prog [options] <gff_file> <repeat_lengths>'
	parser = OptionParser(usage)
	parser.add_option('-o', default='rm_output', dest='output_pre', help='Prefix of the output files. Default: %default')
	parser.add_option('-s', action='store_true', dest='split', help='Do you want to split the filtered GFF file by repeat name. Default: False')
	(options, args) = parser.parse_args()

	if len(args)!=2:
		parser.error(usage)
	else:
		gff_file = args[0]
		repeat_lengths_file = args[1]

	# Open the output files
	filter_1_file = open(options.output_pre + '_long_filtered.gff', 'w')
	filter_2_file = open(options.output_pre + '_final_filtered.gff', 'w')
	discard_entries_file = open(options.output_pre + '_discarded.gff', 'w')
	
	# generate a hash table with the length of each repeat
	repeat_lengths = {}
	for line in open(repeat_lengths_file):
		a = line.strip().split('\t')
		repeat_name, length = a[0], int(a[1])
		repeat_lengths[repeat_name] = length

	# read the bed file and filter entries
	for line in open(gff_file):
		a = line.strip().split('\t')
		chrom, start, end, name, strand = a[0], a[3], a[4], a[8], a[6]
		# Sample name: Target "Motif:chr7_55807836_55826773_R=0" 185 1055
		name = name.split(':')[1].split('\"')[0]
		repeat_length = repeat_lengths[name]
		feature_length =  abs(int(end) - int(start))
		if feature_length <= repeat_length:
			filter_1_line = '\t'.join([chrom, 'InHouse', 'Repeat', start, end, '.', strand, '.', name])
			print >> filter_1_file, filter_1_line
			locus_chrom, locus_start, locus_end = name.split('_')[0:3]
			repeat_range = range(int(locus_start) - 10000, int(locus_end) + 10001) # 1 is added because of the behavior of range function
			if locus_chrom==chrom and int(start) in repeat_range and int(end) in repeat_range:
				print 'Yay. LR found'
				filter_2_line = '\t'.join([chrom, 'InHouse', 'Repeat', start, end, '.', strand, '.', name])
				print >> filter_2_file, filter_2_line
		else:
			discard_line = '\t'.join([chrom, 'InHouse', 'Repeat', start, end, '.', strand, '.', name])
			print >> discard_entries_file, discard_line

	# close all the open files
	filter_1_file.close()
	filter_2_file.close()
	discard_entries_file.close()

	if options.split:
		print >> sys.stderr, 'Splitting filtered GFF file by repeat name...'
		split_gff(options.output_pre + '_final_filtered.gff')

def split_gff(input_gff):
	input_dir = input_dir = '/'.join(input_gff.split('/')[:-1])
	file_name = input_gff.split('/')[-1].split('.')[0]
	output_dir = '/'.join([input_dir, file_name])
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	repeats = {}
	for line in open(input_gff):
		a = line.strip().split('\t')
		repeat_name = a[-1]
		if repeat_name not in repeats:
			repeat_file = '/'.join(output_dir, repeat_name)
			repeats[repeat_name] = open(repeat_file + '.gff', 'w')
		print >> repeats[repeat_name], line.strip()

	for repeat_name in repeats.keys():
		repeats[repeat_name].close()

#########################################################
# main()
#########################################################
if __name__ == '__main__':
	main()