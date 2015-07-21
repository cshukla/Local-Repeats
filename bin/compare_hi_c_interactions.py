#!/usr/bin/env python
from optparse import OptionParser
import glob, sys, tempfile, subprocess, os

###########################################################################################
# compare_hi_c_interactions.py
#
# This script inputs several files with normalized Hi-C matrices and compares the 
# interaction frequency among each file. Both the inputs are comma-seperated.
###########################################################################################
def main():
	usage = 'usage:%prog [options] <labels> <normalized_matrice_files>'
	parser = OptionParser(usage)
	parser.add_option('-o', dest='out_file', default='bed_hi_c_matrices.txt', help='Output file to print normalized hi-c matrices for features in BED file [Default: %default]')
	(options, args) = parser.parse_args()

	if len(args)!=2:
		parser.error('Must provide comma-seperated labels and normalized matrix files\n %s' %(usage))
	else:
		labels = args[0].split(',')
		normalized_matrice_files = args[1].split(',')
		if len(labels)!= len(normalized_matrice_files):
			print >> sys.stderr, 'Must provide labels for each matrix file'

	df = {}
	for i in range(0,len(labels)):
		label = labels[i]
		average_interactions = []
		for line in open(normalized_matrice_files[i]):
			bin_matrix = line.strip().split()
			for i in range(0, len(bin_matrix)):
				bin_matrix = float(bin_matrix[i])
			bin_average = sum(bin_matrix)/len(bin_matrix)
			average_interactions.append(bin_average)
		df[label] = average_interactions

	df_fd, df_file = tempfile.mkstemp()
	df = open(df_file, 'w')
	for label in df.keys():
		average_interactions = df[label]
		for i in range(0, len(average_interactions)):
			print >> df, '\t'.join(str(average_interactions[i]), label)

	df.close()
	r_script = 'compare_hi_c_interactions.R'
	args_str = options.out_file
	subprocess.call('R --slave --args %s %s < %s' % (df_file, args_str, r_script), shell=True)

	os.close(df_fd)
	os.remove(df_file)
###########################################################################################
# main()
###########################################################################################
if __name__ == '__main__':
	main()