#!/usr/bin/env python
from optparse import OptionParser
import glob

###########################################################################################
# get_interaction_matrix.py
#
# Hi-C data is binned into 40 kb sequences and there is an interaction matrix defined for 
# each bin. This script finds the bin any given feature of a GTF file belongs to and prints
# the interaction matrix associated with that bin.
###########################################################################################
def main():
	usage = 'usage:%prog [options] <gtf_file> <chrom_sizes> <normalized_matrices>'
	parser = OptionParser(usage)
	parser.add_option('-o', dest='out_file', default='gtf_hi_c_matrices.txt', help='Output file to print normalized hi-c matrices for features in GTF file [Default: %default]')
	parser.add_option('-b', dest='bin_size', type='int', default=40000, help='Bin Size used for calculating interaction matrices [Default: %default]')
	(options, args) = parser.parse_args()

	if len(args)!=3:
		parser.error('Must provide a GTF file of features, sizes of the chromosomes and directory with the normalized matrices\n %s' %(usage))
	else:
		gtf_file = args[0]
		chrom_sizes = args[1]
		normalized_matrices = args[2]
		bin_size = options.bin_size
		out_file = open(options.out_file, 'w')
	
	chrom_bins = make_chrom_bins(chrom_sizes, bin_size)
	interaction_matrices = get_interaction_matrices(normalized_matrices, bin_size)
	
	for line in open(gtf_file):
		a = line.strip().split()
		chrom, start, end = a[0], a[2], a[3]
		for bin_name in chrom_bins[chrom].keys():
			bin_start = chrom_bins[chrom][bin_name][0]
			bin_end = chrom_bins[chrom][bin_name][1]
			bin_range = range(bin_start, bin_end + 1)
			if start and end in bin_range:
				feature_bin = bin_name
		feature_matrix = interaction_matrices[chrom][feature_bin]
		print >> out_file, '\t'.join(feature_matrix)

	out_file.close()

def make_chrom_bins(chrom_sizes, bin_size):
	chrom_bins = {}
	for line in open(chrom_sizes):
		a = line.strip().split()
		chrom = a[0]
		chrom_size = a[1]
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
		a = file_name.strip().split('/')[-1].split('.')[1]
		chrom = a[1]
		interaction_matrices[chrom] = {}
		i = 1
		for line in open(file_name):
			bin_name = 'bin' + str(i)
			bin_matrix = line.strip().split()
			interaction_matrices[chrom][bin_name] = bin_matrix
			i += 1

	return interaction_matrices

###########################################################################################
# main()
###########################################################################################
if __name__ == '__main__':
	main()