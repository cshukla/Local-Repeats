#!/usr/bin/env python

from optparse import OptionParser

################################################################################
# lr_lengths.py
#
# Given a fasta file with local repeats output the length of each local repeat.
################################################################################
def main():
	usage = 'usage:%prog [options] <fasta_file>'
	parser = OptionParser(usage)
	parser.add_option('-o', dest='output_pre', default='lr_lengths')
	(options, args) = parser.parse_args()

	if len(args)!=1:
		parser.error('Must provide fasta file with repeat sequences')
	else:
		fasta_file = args[0]

	lr_lengths_file = open(options.output_pre + '.txt', 'w')
	repeat_lengths={'0-300':0, '300-1000':0, '>1000':0}
	lr_chromosome={}
	for line in open(fasta_file):
		a = line.strip()
		if a[0]=='>':
			chromosome = a.split('_')[0][1:]
			repeat_name = a[1:]
			lr_chromosome[chromosome] = 1 + lr_chromosome.get(chromosome, 0)
		else:
			repeat_sequence = line.strip()
			out_line = '\t'.join([repeat_name, str(len(repeat_sequence))])
			print >> lr_lengths_file, out_line
			if len(repeat_sequence) <= 300:
				repeat_lengths['0-300']+=1
			elif len(repeat_sequence) <= 1000:
				repeat_lengths['300-1000']+=1
			else:
				repeat_lengths['>1000']+=1

	lr_lengths_file.close()

	lr_ranges_file = open(options.output_pre + '_ranges.txt', 'w')
	out_line = '\t'.join(['0-300', str(repeat_lengths['0-300'])])
	print >> lr_ranges_file, out_line
	out_line = '\t'.join(['300-1000', str(repeat_lengths['300-1000'])])
	print >> lr_ranges_file, out_line
	out_line = '\t'.join(['>1000', str(repeat_lengths['>1000'])])
	print >> lr_ranges_file, out_line

	lr_chromosome_file = open(options.output_pre + '_chrom.txt', 'w')
	for key in lr_chromosome.keys():
		out_line = '\t'.join([key, str(lr_chromosome[key])])
		print >> lr_chromosome_file, out_line

################################################################################
#
################################################################################
if __name__ == '__main__':
	main()
