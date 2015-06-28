#!/usr/bin/env python
from optparse import OptionParser
import math, os, random
import numpy as np
from sklearn.neighbors.kde import KernelDensity
import cufflinks, gff, ggplot

################################################################################
# sample_genes_fpkm.py
#
# Sample genes from one FPKM distribution to match those in another.
################################################################################


################################################################################
# main
################################################################################
def main():
    usage = 'usage: %prog [options] <fpkm_tracking> <distr_gtf> <sample_gtf>'
    parser = OptionParser(usage)
    parser.add_option('-f', dest='fpkm_condition', help='Condition from which to consider FPKM')
    parser.add_option('-m', dest='min_fpkm', default=0.125, type='float', help='Minimum FPKM for log transformation [Default: %default]')
    parser.add_option('-n', dest='num_sample', default=1000, type='int', help='Number of genes to sample [Default: %default]')
    (options,args) = parser.parse_args()

    if len(args) != 3:
        parser.error('Must provide fpkm_tracking file, a GTF file of genes to establish the FPKM distribution, and a GTF file to sample genes from')
    else:
        fpkm_tracking = args[0]
        distr_gtf = args[1]
        sample_gtf = args[2]

    ############################################
    # hash gene fpkm's
    ############################################
    cuff = cufflinks.fpkm_tracking(fpkm_tracking)

    if len(cuff.experiments) == 1:
        options.fpkm_condition = cuff.experiments[0]
    else:
        if options.fpkm_condition == None:
            parser.error('fpkm_tracking has >1 condition, specify with -f which to use')
        elif not options.fpkm_condition in cuff.experiments:
            parser.error('%s not in fpkm_tracking. try %s' % (options.fpkm_tracking,','.join(cuff.experiments)))

    gene_fpkm = {}
    for gene_id in cuff.gene_map:
        gene_fpkm[gene_id] = math.log(options.min_fpkm + cuff.gene_expr_exp(gene_id, options.fpkm_condition), 2)

    ############################################
    # split genes
    ############################################
    # get distribution genes
    distr_genes = set()
    for line in open(distr_gtf):
        a = line.split('\t')
        gene_id = gff.gtf_kv(a[8])['gene_id']
        distr_genes.add(gene_id)

    # get sample genes
    sample_genes = set()
    for line in open(sample_gtf):
        a = line.split('\t')
        gene_id = gff.gtf_kv(a[8])['gene_id']
        sample_genes.add(gene_id)

    ############################################
    # learn fpkm densities
    ############################################
    miss_fpkm = math.log(options.min_fpkm,2)
    sample_fpkms = np.array([[gene_fpkm.get(gene_id,miss_fpkm)] for gene_id in sample_genes])
    sample_fpkm_kde = KernelDensity(kernel='gaussian', bandwidth=0.5).fit(sample_fpkms)

    distr_fpkms = np.array([[gene_fpkm.get(gene_id,miss_fpkm)] for gene_id in distr_genes])
    distr_fpkm_kde = KernelDensity(kernel='gaussian', bandwidth=0.5).fit(distr_fpkms)

    ############################################
    # choose genes
    ############################################
    # for gene in sample genes
    chosen_genes = set()
    for gene_id in sample_genes:
        sample_dens = math.exp(sample_fpkm_kde.score(gene_fpkm.get(gene_id,miss_fpkm)))
        distr_dens = math.exp(distr_fpkm_kde.score(gene_fpkm.get(gene_id,miss_fpkm)))

        sample_p = (options.num_sample/float(len(sample_genes)))*(distr_dens/sample_dens)
        if random.random() < sample_p:
            chosen_genes.add(gene_id)

    ############################################
    # plot distributions to see how we did
    ############################################
    df = {'fpkm':[], 'class':[]}
    df['fpkm'] += [gene_fpkm.get(gene_id,miss_fpkm) for gene_id in chosen_genes]
    df['class'] += ['sampled']*len(chosen_genes)
    df['fpkm'] += [gene_fpkm.get(gene_id,miss_fpkm) for gene_id in sample_genes]
    df['class'] += ['original']*len(sample_genes)
    df['fpkm'] += [gene_fpkm.get(gene_id,miss_fpkm) for gene_id in distr_genes]
    df['class'] += ['distribution']*len(distr_genes)

    r_script = '/Users/chinmayshukla/Documents/Research/Local-Repeats/bin/r_scripts/sample_genes_fpkm.r'
    ggplot.plot(r_script, df, [])
    
    ############################################
    # output chosen genes as GTF
    ############################################
    for line in open(sample_gtf):
        a = line.split('\t')
        gene_id = gff.gtf_kv(a[8])['gene_id']
        if gene_id in chosen_genes:
            print line,


################################################################################
# __main__
################################################################################
if __name__ == '__main__':
    main()
