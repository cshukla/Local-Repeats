#!/usr/bin/env python

from optparse import OptionParser

################################################################################
# gtf_genes_bed.py
#
# Given a GTF File output a BED file with a feature for every gene.
################################################################################
def main():
	usage = 'usage:%prog [options] <gtf_file>'
	parser = OptionParser(usage)
	(options, args) = parser.parse_args()

	if len(args)!=1:
		parser.error('Must provide GTF file')
	else:
		gtf_file = args[0]

	gene_cordinates = {}
	for line in open(gtf_file):
		a = line.strip().split('\t')
		gene_id = a[-1].split(' ')[1][1:-2]
		gene_cordinates[gene_id] = []

	for line in open(gtf_file):
		a = line.strip().split('\t')
		chromosome, start, end = a[0], a[3], a[4]
		gene_id = a[-1].split(' ')[1][1:-2]
		gene_cordinates[gene_id].append(int(start))
		gene_cordinates[gene_id].append(int(end))

	for gene_id in gene_cordinates.keys():
		cordinates = sorted(gene_cordinates[gene_id])
		gene_start = cordinates[0]
		gene_end = cordinates[-1]
		gene_cordinates[gene_id] = [gene_start, gene_end]
		
	for line in open(gtf_file):
		a = line.strip().split('\t')
		chromosome = a[0]
		gene_id = a[-1].split(' ')[1][1:-2]
		gene_cordinates[gene_id].append(chromosome)

	for gene_id in gene_cordinates.keys():
		gene_start, gene_end, chromosome = gene_cordinates[gene_id][0:3]
		out_line = '\t'.join([chromosome, str(gene_start), str(gene_end), gene_id])
		print out_line

################################################################################
#
################################################################################
if __name__ == '__main__':
	main()
