#!/usr/bin/env python
from optparse import OptionParser
import math, os, pdb, random, sys
import cufflinks, scipy

################################################################################
# neighboring_genes_spearman.py
# 
# Report FPKMs and and compute Spearman corelation for every pair of 
# neighboring genes defined by the user.
################################################################################

################################################################################
# main
################################################################################
def main():
    usage = 'usage: %prog [options] <fpkm_tracking> <neighboring_genes>'
    parser = OptionParser(usage)
    parser.add_option('-o', dest='out_file', default='neighboring_genes_spearman.txt', help='Output PDF [Default: %default]')
    (options,args) = parser.parse_args()

    if len(args) != 2:
        parser.error('Must provide fpkm_tracking')
    else:
        fpkm_tracking = args[0]
        neighboring_genes = args[1]

    # map the input genes and neighboring genes
    neighboring_genes_hash = {}
    for line in open(neighboring_genes,'r'):
        input_gene, neighboring_gene = line.strip().split('\t')
        neighboring_genes_hash[input_gene] = neighboring_gene

    # load expression data
    cuff = cufflinks.fpkm_tracking(fpkm_file=fpkm_tracking)

    # open output file
    out_file = open(options.out_file, 'w')
    print >> out_file, '\t'.join(['Spearman', 'p_val'])
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
            spearman, p_val = scipy.stats.spearmanr(ge_fpkm, neighbor_ge_fpkm)
            print >> out_file, '\t'.join([str(spearman), str(p_val)])

    out_file.close()

################################################################################
# __main__
################################################################################
if __name__ == '__main__':
    main()
    #pdb.runcall(main)
