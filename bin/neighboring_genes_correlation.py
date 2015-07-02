#!/usr/bin/env python
from optparse import OptionParser
import math, os, pdb, random, sys
import cufflinks, scipy, tempfile

################################################################################
# neighboring_genes_spearman.py
# 
# Report FPKMs and and compute a correlation coefficient for every pair of 
# neighboring genes defined by the user. Default is to compute spearman 
# correlations.
#
# Note: Currently only limited to computing Spearman and Pearson coefficients.
# Need to expand to compute more correlations.
################################################################################

################################################################################
# main
################################################################################
def main():
    usage = 'usage: %prog [options] <fpkm_tracking> <input_bed>'
    parser = OptionParser(usage)
    parser.add_option('-o', dest='out_file', default='neighboring_genes_spearman.txt', help='Output txt file [Default: %default]')
    parser.add_option('-c', dest='correlation_coefficient', default='spearman', help='Type of correlation coefficient [Default: %default]')
    parser.add_option('-t', dest='target_bed', default='hg19_protein_coding.bed', help='')
    (options,args) = parser.parse_args()

    if len(args) != 2:
        parser.error('Must provide fpkm_tracking and input bed file. Usage = %s' %(usage))
    else:
        fpkm_tracking = args[0]
        input_bed = args[1]

    ############################################
    # get neighboring genes
    ############################################

    neighboring_genes_fd, neighboring_genes_file = get_neighbors(input_bed, options.target_bed)
    
    ############################################
    # map the input genes and neighboring genes
    ############################################

    neighboring_genes_hash = {}
    for line in open(neighboring_genes_file,'r'):
        input_gene, neighboring_gene = line.strip().split('\t')
        neighboring_genes_hash[input_gene] = neighboring_gene

    ############################################
    # clean
    ############################################

    os.close(neighboring_genes_fd)
    os.remove(neighboring_genes_file)

    ############################################
    # load expression data
    ############################################

    cuff = cufflinks.fpkm_tracking(fpkm_file=fpkm_tracking)

    ############################################
    # open output file
    ############################################

    out_file = open(options.out_file, 'w')
    if options.correlation_coefficient == 'spearman':
        print >> out_file, '\t'.join(['Spearman', 'p_val'])
    elif options.correlation_coefficient == 'pearson':
        print >> out_file, '\t'.join(['Pearson', 'p_val'])
    else:
        print >> sys.stderr, 'Currently only pearson and spearman correlation are supported'

    ############################################
    # Compute correlation coefficient
    ############################################

    for gene_id in neighboring_genes_hash.keys():
        neighbor = neighboring_genes_hash[gene_id]
        ge = cuff.gene_expr(gene_id)
        ge_fpkm = []
        neighbor_ge = cuff.gene_expr(neighbor)
        neighbor_ge_fpkm = []
    
        if not math.isnan(ge[0]):
            for i in range(len(cuff.experiments)):
                ge_fpkm.append(ge[i])
        if not math.isnan(neighbor_ge[0]):
            for i in range(len(cuff.experiments)):
                neighbor_ge_fpkm.append(neighbor_ge[i])

        if len(ge_fpkm) == len(neighbor_ge_fpkm):
            if options.correlation_coefficient == 'spearman':
                spearman, p_val = scipy.stats.spearmanr(ge_fpkm, neighbor_ge_fpkm)
                print >> out_file, '\t'.join([str(spearman), str(p_val)])
            elif options.correlation_coefficient == 'pearson':
                pearson, p_val = scipy.stats.pearsonr(ge_fpkm, neighbor_ge_fpkm)
                print >> out_file, '\t'.join([str(pearson), str(p_val)])

    out_file.close()

################################################################################
# get_neighbors()
#
# This function inputs 2 BED files and finds neighbors of input BED file 
# features in target BED file. The output is a tab delimited file of neighbors
################################################################################

def get_neighbors(input_bed, target_bed):
    closest_bed_fd, closest_bed_file = tempfile.mkstemp()
    subprocess.call('closestBed -a %s -b %s -io -S -t first > %s' %(input_bed, target_bed, closest_bed_file), shell=True)
    neighboring_genes_fd, neighboring_genes_file = tempfile.mkstemp()
    subprocess.call('awk "{OFS="\t"}{print $4, $8}" %s > %s' %(closest_bed_file, neighboring_genes_file), shell=True)
    os.close(closest_bed_fd)
    os.remove(closest_bed_file)

    return neighboring_genes_fd, neighboring_genes_file

################################################################################
# __main__
################################################################################
if __name__ == '__main__':
    main()
    #pdb.runcall(main)
