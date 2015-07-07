#!/usr/bin/env python

from optparse import OptionParser
import os, subprocess, tempfile, glob

################################################################################
# repeat_catalog.py
#
# Given a BED File output the catalog of local repeats for the features.
################################################################################
def main():
	usage = 'usage:%prog [options] <bed_file> <genome_fasta>'
	parser = OptionParser(usage)
	(options, args) = parser.parse_args()

	if len(args)!=2:
		parser.error('Must provide required input files')
	else:
		bed_file = args[0]
		genome_fasta = args[1]

	############################################
	# Get repeats in each feature
	############################################

	for line in open(bed_file):
		a = line.strip().split('\t')
		chromosome, start, end = a[0], a[1], a[2]
		get_repeats(chromosome, start, end, genome_fasta)

	############################################
	# Combine all repeats in 1 file
	############################################

	all_repeats = 'all_repeats.rs'
	all_repeats_file = open(all_repeats, 'w')
	for repeatscout_output in glob.glob('*.repeatscout'):
		locus_name = repeatscout_output.split('.')[0]
		for line in open(repeatscout_output):
			if line[0]=='>':
				repeat_number = line.strip()[1:]
				repeatname = '>' + locus_name + '_' + repeat_number
				print >> all_repeats_file, repeatname
			else:
				print >> all_repeats_file, line.strip()

	all_repeats_file.close()

	############################################
	# Find and filter tandem repeats
	############################################

	masked_file = mask_tandem_repeats(all_repeats)
	filter_tandem_repeats(masked_file)

################################################################################
# get_repeats()
# 
# This function inputs the location and FASTA file of the genome. The output is
# a fasta file of the RepeatScout output detailing all repeats found in the 
# location.
################################################################################

def get_repeats(chromosome, start, end, genome_fasta):

	############################################
	# Get feature sequence
	############################################

	locus_name = '_'.join([chromosome, start, end])
	sequence_file = make_fasta(chromosome, start, end, genome_fasta, locus_name)
	lmer_file = locus_name + '.16mer'
	repeats_file = locus_name + '.repeatscout'

	############################################
	# Get Local Repeats in the sequence
	############################################

	subprocess.call('build_lmer_table -l 16 -sequence %s -freq %s' %(sequence_file, lmer_file), shell=True)
	subprocess.call('RepeatScout -sequence %s -output %s -freq %s -l 16' %(sequence_file, repeats_file, lmer_file), shell=True)

################################################################################
# make_fasta()
# 
# This function inputs the location, locus name and FASTA file of the genome. 
# The output is a fasta file of the location saved by the locus name.
################################################################################

def make_fasta(chromosome, start, end, genome_fasta, locus_name):
	feature_gtf_fd, feature_gtf = tempfile.mkstemp()
	feature_gtf_file = open(feature_gtf,'w')
	gtf_line = '\t'.join([chromosome, 'Cufflinks', 'Exon', start, end, '.', '+', '.', 'Feature_GTF'])
	print >> feature_gtf_file, gtf_line
	feature_gtf_file.close()
	sequence_file = '.'.join([locus_name, 'fa'])
	subprocess.call('gtf_to_fasta %s %s %s' %(feature_gtf, genome_fasta, sequence_file), shell=True)

	############################################
	# clean
	############################################

	os.close(feature_gtf_fd)
	os.remove(feature_gtf)

	return sequence_file

################################################################################
# mask_tandem_repeats()
# 
# The input is a fasta file of sequences. The output is a fasta file in which
# tandem repeats are masked.
################################################################################

def mask_tandem_repeats(all_repeats):
	masked_file = 'all_repeats.masked.rs'
	subprocess.call('trf %s 2 7 7 80 10 50 500 -f -d -m' %(all_repeats) , shell = True)
	subprocess.call('rm *.dat', shell=True)
	subprocess.call('rm *.html', shell=True)
	subprocess.call('mv *.mask %s' %(masked_file), shell=True)
	return masked_file

################################################################################
# filter_tandem_repeats()
# 
# The function inputs a FASTA file with tandem repeats masked by N's. The output
# is a FASTA file in which sequences with any tandem repeats are filtered.
################################################################################

def filter_tandem_repeats(masked_file):
	repeat_sequences = {}
	for line in open(masked_file):
		if line[0]=='>':
			repeat_name = line.strip()
			repeat_sequences[repeat_name] = ''
		else:
			repeat_sequences[repeat_name]+= line.strip()

	filtered_output = 'all_repeats.filtered.rs'
	filtered_output_file = open(filtered_output, 'w')
	for repeat in sorted(repeat_sequences.keys()):
		sequence = repeat_sequences[repeat]
		if sequence.find('N') == -1:
			print >> filtered_output_file, repeat
			print >> filtered_output_file, sequence

	filtered_output_file.close()

################################################################################
#
################################################################################
if __name__ == '__main__':
	main()