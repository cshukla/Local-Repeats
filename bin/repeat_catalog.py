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

	all_repeats = open('all_repeats.rs', 'w')
	for repeatscout_output in glob.glob('*.repeatscout'):
		locus_name = repeatscout_output.split('.')[0]
		for line in open(repeatscout_output):
			if line[0]=='>':
				repeat_number = line.strip()[1:]
				repeatname = '>' + locus_name + '_' + repeat_number
				print >> all_repeats, repeatname
			else:
				print >> all_repeats, line.strip()

	############################################
	# Find and filter tandem repeats
	############################################

	#filter_tandem_repeats(masked_file, filtered_output)

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

def filter_tandem_repeats(masked_file, filtered_output):
	repeat_sequences = {}
	for line in open(masked_file):
		if line[0]=='>':
			repeat_name = line.strip()
			repeat_sequence = ''
			repeat_sequences[repeat_name] = repeat_sequence
		else:
			repeat_sequence += line.strip()
			repeat_sequences[repeat_name]+= repeat_sequence

	filtered_output_file = open(filtered_output, 'w')
	for repeat in sorted(repeat_sequences.keys()):
		sequence = repeat_sequences[repeat]
		if sequence.find('N') == -1:
			print >> filtered_output_file, repeat
			print >> filtered_output_file, sequence

################################################################################
#
################################################################################
if __name__ == '__main__':
	main()