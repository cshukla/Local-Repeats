#!/usr/bin/env python

from optparse import OptionParser
import tempfile, subprocess

###################################################################
# make_oligo_pool.py
#
# Input a BED file of genomic regions and size of tiling window. 
# Output a MPRA pool with oligos tiling genomic region by 
# specified window.
##################################################################

##################################################################
# main()
##################################################################

def main():
	usage = 'usage:%prog [options] <genomic_regions> <genome_fasta> <window_size>'
	parser = OptionParser(usage)
	parser.add_option('-l', dest='oligo_length', type = int, default=87, help='Length of the sequence in each oligo [Default: %default]')
	(options, args) = parser.parse_args()

	if len(args)!=3:
		parser.error('Must provide file with genomic regions, genome fasta file and size of tiling window to be used')
	else:
		genomic_regions = args[0]
		genome_fasta = args[1]
		window_size = int(args[2])

	tiled_regions = tile_genomic_regions(genomic_regions, window_size, options.oligo_length, genome_fasta)
	for i in range(0, len(tiled_regions)):
		oligo_seq = tiled_regions[i]
		seq_head = '>' + 'Oligo_' + str(i+1)
		print seq_head
		print oligo_seq

def tile_genomic_regions(genomic_regions, window_size, oligo_length, genome_fasta):
	tiled_regions = []
	scratch_fd, scratch_file = tempfile.mkstemp()
	scratch_file_open = open(scratch_file, 'w')

	for line in open(genomic_regions):
		a = line.split('\t')
		region_chrom, region_start, region_end = a[0], int(a[1]), int(a[2])
		if len(a)>3:
			region_strand = a[4]
		else:
			region_strand = '+'
		oligo_start = region_start
		oligo_end = 0
		oligo_number = 1
		while oligo_end <= region_end:
			oligo_end = oligo_start + 86
			out_line = '\t'.join([region_chrom, 'Cufflinks', 'Exon', str(oligo_start), str(oligo_end), '.', region_strand, '.', 'Oligo_' + str(oligo_number)])
			print >> scratch_file_open, out_line
			oligo_start += 5
			oligo_number += 1
			
	scratch_file_open.close()
	scratch_seq_fd, scratch_seq_file = tempfile.mkstemp()
	subprocess.call('gtf_to_fasta %s %s %s' %(scratch_file, genome_fasta, scratch_seq_file), shell=True)
	oligo_seq = ''
	for line in open(scratch_seq_file, 'r'):
		if line[0]!='>':
			seq = line.strip()
			oligo_seq += seq
			if len(oligo_seq) == oligo_length:
				tiled_regions.append(oligo_seq)
				oligo_seq = ''
			else:
				oligo_seq = oligo_seq

	os.close(scratch_fd)
	os.remove(scratch_file)
	os.close(scratch_seq_fd)
	os.remove(scratch_seq_file)

	return tiled_regions

##################################################################
# 
##################################################################
if __name__ == '__main__':
	main()