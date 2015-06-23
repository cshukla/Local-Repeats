#!/usr/bin/env python

from optparse import OptionParser
import numpy as np
import sys, subprocess, os, tempfile
import pdb

###################################################################
# repeat_enrichment.py
#
# This script inputs a text file (output of firre_repeats.py) of 
# features and their counts to calculate the enrichment of each 
# feature in the input.
#
# How to assign this a p-value to this?
# 
# One approach can be to shuffle the repeat file a 100 times and
# check how many times the # of features intersecting with FIRRE is
# more than the input value. Divide by 100 and get a p-value.
###################################################################
def main():
	usage = 'usage: %prog [options] <feature_counts>'
	parser = OptionParser(usage)
	parser.add_option('-r', dest='rm_out', help='Output of Repeat Masker')
	parser.add_option('-g', dest='genome_bed', help='.genome file for shuffleBed')
	parser.add_option('-e', dest='gaps_bed', help='gaps file giving exclusion for shuffleBed')
	parser.add_option('-f', dest='firre_bed', help='Bed file giving co-ordinates of FIRRE')
	parser.add_option('-o', dest='output_file', help='The file where you want to print output of this script')
	(options, args) = parser.parse_args()

	if len(args) != 1:
		parser.error('Must provide the gff file and all the options files')
	else:
		feature_counts = args[0]

	features = {}
	for line in open(feature_counts):
		contents = line.split('\t')
		features[contents[0]] = int(contents[1])

	for key in sorted(features.keys()):
		print key
		firre_count = features[key]
		grep_key = "'" + key + "'"
		key_gff_fd, key_gff_file = tempfile.mkstemp()
		subprocess.call('grep -i %s %s > %s' %(grep_key, options.rm_out, key_gff_file), shell=True)
		count = 0
		fail = 0
		enrichment = []
		seed = 1234
		while count < 100:
			key_shuffle_fd, key_shuffle_file = tempfile.mkstemp()
			subprocess.call('shuffleBed -seed %d -excl %s -i %s -g %s > %s' %(seed, options.gaps_bed, key_gff_file, options.genome_bed, key_shuffle_file), shell=True)
			p = subprocess.Popen('intersectBed -a %s -b %s -wo | wc -l' %(options.firre_bed, key_shuffle_file), shell=True, stdout=subprocess.PIPE)
			for line in p.stdout:
				shuffle_count = float(line.strip().split(' ')[0]) #+ 0.001
			if shuffle_count > 0:
				enrichment.append(firre_count/shuffle_count)
			if shuffle_count > firre_count:
				fail +=1
			count += 1
			seed += 500
			os.close(key_shuffle_fd)
			os.remove(key_shuffle_file)
		enrichment = np.median(enrichment)
		p_val = float(fail)/100
		features[key] = '\t'.join([str(firre_count), str(enrichment), str(p_val)])	

	output_file = open(options.output_file, 'w')
	for key in sorted(features.keys()):
		print >> output_file, '\t'.join([key, features[key]])
###################################################################
# main()
###################################################################
if __name__ == '__main__':
	main()


