#!/usr/bin/env python

from optparse import OptionParser
import os, sys

#############################################################
# filter_blat_bed.py
#
# This script filters the BED file obtained by converting
# output of Blat program from psl to BED format. Currently, I
# am using 2 filters to remove unwanted entries.
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
#############################################################
def main():
	usage = 'usage:%prog [options] <bed_file> <repeat_lengths>'
	parser = OptionParser(usage)
	parser.add_option('-o', default='blat_output', dest='output_pre', help='Prefix of the output files. Default: %default')
	(options, args) = parser.parse_args()

	if len(args)!=2:
		parser.error(usage)
	else:
		bed_file = args[0]
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

	#print >> sys.stderr, 'Generated hash table with repeat lengths.'
	#print >> sys.stderr, 'Filtering BED file now.'

	# read the bed file and filter entries
	for line in open(bed_file):
		a = line.strip().split('\t')
		chrom, start, end, name, strand = a[0], a[1], a[2], a[3], a[5]
		repeat_length = repeat_lengths[name]
		feature_length =  abs(int(end) - int(start))
		print feature_length, repeat_length
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
	#print >> sys.stderr, 'Done. Check output'

#########################################################
# main()
#########################################################
if __name__ == '__main__':
	main()