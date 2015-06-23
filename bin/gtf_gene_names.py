#!/usr/bin/env python

from optparse import OptionParser

################################################################################
# gtf_gene_names.py
#
# Given a GTF File output a list of gene names.
################################################################################
def main():
	usage = 'usage:%prog [options] <gtf_file>'
	parser = OptionParser(usage)
	(options, args) = parser.parse_args()

	if len(args)!=1:
		parser.error('Must provide GTF file')
	else:
		gtf_file = args[0]

	for line in open(gtf_file):
		a = line.strip().split('\t')
		if len(a) == 9:
			gene_id = a[-1].split(' ')[1][1:-2]
			print gene_id
		else:
			gene_id = a[-1]
			print gene_id

################################################################################
#
################################################################################
if __name__ == '__main__':
	main()
