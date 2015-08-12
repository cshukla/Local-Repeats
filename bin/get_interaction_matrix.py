#!/usr/bin/env python
from optparse import OptionParser
import glob, sys

###########################################################################################
# get_interaction_matrix.py
#
# Hi-C data is binned into 40 kb sequences and there is an interaction matrix defined for 
# each bin. This script finds the bin any given feature of a BED file belongs to and prints
# the interaction matrix associated with that bin.
#
# Currently, I am dividing each chromosome into bins and then finding the bin corresponding
# to a particular feature by iteration. This isn't the optimal way to do things. Changing 
# this will substantially improve speed.
###########################################################################################
def main():
	usage = 'usage:%prog [options] <bed_file> <chrom_sizes> <normalized_matrices>'
	parser = OptionParser(usage)
	parser.add_option('-o', dest='out_file', default='bed_hi_c_matrices.txt', help='Output file to print normalized hi-c matrices for features in BED file [Default: %default]')
	parser.add_option('-b', dest='bin_size', type='int', default=40000, help='Bin Size used for calculating interaction matrices [Default: %default]')
	(options, args) = parser.parse_args()

	if len(args)!=3:
		parser.error('Must provide a BED file of features, sizes of the chromosomes and directory with the normalized matrices\n %s' %(usage))
	else:
		bed_file = args[0]
		chrom_sizes = args[1]
		normalized_matrices = args[2]
		bin_size = options.bin_size
		out_file = open(options.out_file, 'w')

	if normalized_matrices[-2:] == 'hm':
		extract_from_heatmap(bed_file, normalized_matrices, out_file, bin_size)
	else:
		extract_from_matrices(bed_file, normalized_matrices, bin_size, out_file)

def extract_from_heatmap(bed_file, normalized_matrices, out_file):
	matrices = []
	for line in bed_file:
		a = line.strip().split('\t')
		   heatmap_key = '22 22'
		elif a[0] == 'chrY':
		   heatmap_key = '23 23'
		else:
		   chrom_num = int(a[0][3:])
		   heatmap_key = ' '.join([str(chrom_num - 1), str(chrom_num - 1)])
		start, end = int(a[1]), int(a[2])
		bin_number = 1
		pos = 1
		while pos < end:
		   bin_start = pos
		   bin_end = pos + 39999
		   pos += 40000
		   bin_number += 1
		matrices.append(heatmap[heatmap_key][bin_number].tolist())

def extract_from_matrices(bed_file, normalized_matrices, bin_size, out_file):
	chrom_bins = make_chrom_bins(chrom_sizes, bin_size)
	print >> sys.stderr, 'Divided each chromosome into bins of %i bps' %(bin_size)
	interaction_matrices = get_interaction_matrices(normalized_matrices, bin_size)
	print >> sys.stderr, 'Finished storing all the interaction matrices into a hash table'
	
	print >> sys.stderr, 'Extracting normalized matrix for each feature in the bed file'
	print >> sys.stderr, 'This step is quite slow right now. Please wait...'
	for line in open(bed_file):
		a = line.strip().split()
		chrom, start, end = a[0], int(a[1]), int(a[2])
		for bin_name in chrom_bins[chrom].keys():
			bin_start = chrom_bins[chrom][bin_name][0]
			bin_end = chrom_bins[chrom][bin_name][1]
			bin_range = range(bin_start, bin_end + 1)
			if start in bin_range or end in bin_range:
				feature_bin = bin_name
		feature_matrix = interaction_matrices[chrom][feature_bin]
		print >> out_file, '\t'.join(feature_matrix)

	out_file.close()

def make_chrom_bins(chrom_sizes, bin_size):
	chrom_bins = {}
	for line in open(chrom_sizes):
		a = line.strip().split()
		chrom = a[0]
		chrom_size = int(a[1])
		chrom_bins[chrom] = {}
		i = 1
		pos = 1
		while pos < chrom_size:
			bin_name = 'bin_' + str(i)
			i += 1
			bin_start = pos
			bin_end = pos + (bin_size - 1)
			pos += bin_size
			chrom_bins[chrom][bin_name] = [bin_start, bin_end]

	return chrom_bins

def get_interaction_matrices(normalized_matrices, bin_size):
	interaction_matrices = {}
	if normalized_matrices[-1] == '/':
		normalized_matrices_files = glob.glob(normalized_matrices + '*.*')
	else:
		normalized_matrices_files = glob.glob(normalized_matrices + '/*.*')

	for file_name in normalized_matrices_files:
		a = file_name.strip().split('/')[-1].split('.')
		chrom = a[1]
		interaction_matrices[chrom] = {}
		i = 1
		for line in open(file_name):
			bin_name = 'bin_' + str(i)
			bin_matrix = line.strip().split()[1:]
			interaction_matrices[chrom][bin_name] = bin_matrix
			i += 1

	return interaction_matrices

###########################################################################################
# main()
###########################################################################################
if __name__ == '__main__':
	main()