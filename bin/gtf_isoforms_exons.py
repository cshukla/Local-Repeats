#!/usr/bin/env python

from optparse import OptionParser
from collections import defaultdict

################################################################################
# gtf_isoforms_exons.py
#
# Given a GTF File output a file with the number of isoforms for every gene.
################################################################################
def main():
	usage = 'usage:%prog [options] <gtf_file>'
	parser = OptionParser(usage)
	parser.add_option('-o', dest='output_pre', default='gtf')
	(options, args) = parser.parse_args()

	if len(args)!=1:
		parser.error('Must provide GTF file')
	else:
		gtf_file = args[0]

	gene_isoforms = defaultdict(list)
	isoforms_exons = defaultdict(list)
	for line in open(gtf_file):
		a = line.strip().split('\t')
		if a[2]=='exon':
			gene_id = a[-1].split(' ')[1][1:-2]
			transcript_id = a[-1].split(' ')[3][1:-2]
			exon_start = int(a[3])
			exon_end = int(a[4])
			exon_length = exon_end - exon_start
			if transcript_id not in gene_isoforms[gene_id]:
				gene_isoforms[gene_id].append(transcript_id)
			isoforms_exons[transcript_id].append(exon_length)

	gene_isoforms_file = open(options.output_pre + '_gene_isoforms.txt', 'w')
	for gene_id in gene_isoforms.keys():
		number_of_isoforms = len(gene_isoforms[gene_id])
		transcripts = ','.join(gene_isoforms[gene_id])
		out_line = '\t'.join([gene_id, transcripts, str(number_of_isoforms)])
		print >>gene_isoforms_file, out_line
	gene_isoforms_file.close()

	isoforms_exons_file = open(options.output_pre + '_isoform_exons.txt', 'w')
	for isoform in isoforms_exons.keys():
		number_of_exons = len(isoforms_exons[isoform])
		length_of_transcript = sum(isoforms_exons[isoform])
		out_line = '\t'.join([isoform, str(number_of_exons), str(length_of_transcript)])
		print >> isoforms_exons_file, out_line
	isoforms_exons_file.close()

################################################################################
#
################################################################################
if __name__ == '__main__':
	main()
