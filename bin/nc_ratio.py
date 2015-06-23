#!/usr/bin/env python

from optparse import OptionParser
import math, os, random, sys, cufflinks, scipy

#######################################################################################
# nc_ratio.py
#
# Input a fpkm tracking file from cellular fractionation data and calculate 
# nuclear to cytoplasmic ratio for all genes using the following formula:
# 	if: nuclear_fpkm < 0.01; nc_ratio = 0
#	else if: cytosolic_fpkm < 0.01; nc_ratio = nuclear_fpkm
#	else: nc_ratio = (nuclear_fpkm/total_nuclear)/(cytosolic_fpkm/total_cytosolic)
#######################################################################################
def main():
	usage = 'usage:%prog [options] <genes.fpkm_tracking>'
	parser = OptionParser(usage)
	parser.add_option('-g', dest='gtf', help='GTF file of genes to display')
	parser.add_option('-o', dest='out_file', default='nc_ratio.tab', help='NC Ratio Output Table [Default: %default]')
	(options, args) = parser.parse_args()

	if len(args)!=1:
		parser.error('Must provide fpkm tracking file')
	else:
		fpkm_tracking = args[0]

	#############################
	# open output file
	#############################

	out_file = open(options.out_file, 'w')
	print >> out_file, '\t'.join(['Gene_ID', 'Nuclear_FPKM', 'Cytosolic_FPKM', 'NC_Ratio'])
	
	#############################
	# load expression data
	#############################

	cuff = cufflinks.fpkm_tracking(fpkm_file=fpkm_tracking)

	#############################
	# determine genes
	#############################

	all_genes = set(cuff.genes)
	if options.gtf:
		all_genes = set()
		for line in open(options.gtf):
			a = line.split('\t')
			all_genes.add(gtf_kv(a[8])['gene_id'])

	#############################
	# load nuclear and cytosolic
	# fpkm for all genes
	#############################
	
	nuclear_fpkms = {}
	total_nuclear_fpkm = 0
	cytosolic_fpkms = {}
	total_cytosolic_fpkm = 0
	for gene_id in all_genes:
		ge = cuff.gene_expr(gene_id)
		if not math.isnan(ge[0]):
			for i in range(len(cuff.experiments)):
				sample = cuff.experiments[i]
				gene_exp = ge[i]
				if 'nucleus' in sample:
					nuclear_fpkms[gene_id] = float(gene_exp)
					if not math.isnan(gene_exp):
						total_nuclear_fpkm += float(gene_exp)
				elif 'cytosol' in sample:
					cytosolic_fpkms[gene_id] = float(gene_exp)
					if not math.isnan(gene_exp):
						total_cytosolic_fpkm += float(gene_exp)

	#############################
	# compute nuclear/cytosolic 
	# ratio and write output file
	#############################

	for gene_id in nuclear_fpkms.keys():
		nuclear_fpkm = nuclear_fpkms[gene_id]
		cytosolic_fpkm = cytosolic_fpkms[gene_id]
		if not math.isnan(nuclear_fpkm and cytosolic_fpkm):
			if nuclear_fpkm < 0.01:
				nc_ratio = 0
			elif cytosolic_fpkm < 0.01:
				nc_ratio = nuclear_fpkm
			else:
				nuclear_ratio = nuclear_fpkm/total_nuclear_fpkm
				cytosolic_ratio = cytosolic_fpkm/total_cytosolic_fpkm
				nc_ratio = float(nuclear_ratio)/float(cytosolic_ratio)
			out_line = '\t'.join([gene_id, str(nuclear_fpkm), str(cytosolic_fpkm), str(nc_ratio)])
			print >> out_file, out_line

	#############################
	# close all open files
	#############################

	out_file.close()

################################################################################
# gtf_kv
#
# Convert the last gtf section of key/value pairs into a dict.
################################################################################
def gtf_kv(s):
    d = {}

    a = s.split(';')
    for key_val in a:
        if key_val.strip():
            eq_i = key_val.find('=')
            if eq_i != -1 and key_val[eq_i-1] != '"':
                kvs = key_val.split('=')
            else:
                kvs = key_val.split()

            key = kvs[0]
            if kvs[1][0] == '"' and kvs[-1][-1] == '"':
                val = (' '.join(kvs[1:]))[1:-1].strip()
            else:
                val = (' '.join(kvs[1:])).strip()

            d[key] = val

    return d

#######################################################################################
# main()
#######################################################################################
if __name__ == '__main__':
	main()