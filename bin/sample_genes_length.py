#!/usr/bin/env python
from optparse import OptionParser
import math, os, random
import numpy as np
from sklearn.neighbors.kde import KernelDensity
import cufflinks, gff, ggplot

################################################################################
# sample_genes_length.py
#
# Sample genes from one length distribution to match those in another.
################################################################################


################################################################################
# main
################################################################################
def main():
    usage = 'usage: %prog [options] <lengths_file> <distr_gtf> <sample_gtf>'
    parser = OptionParser(usage)
    parser.add_option('-n', dest='num_sample', default=1000, type='int', help='Number of genes to sample [Default: %default]')
    (options,args) = parser.parse_args()

    if len(args) != 3:
        parser.error('Must provide legnths file, a GTF file of genes to establish the lengths distribution, and a GTF file to sample genes from')
    else:
        lengths_file = args[0]
        distr_gtf = args[1]
        sample_gtf = args[2]

    ############################################
    # hash gene lengths
    ############################################

    gene_lengths = {}
    for line in open(lengths_file):
        a = line.strip().split('\t')
        gene_id = a[1]
        gene_length = float(a[0])
        gene_lengths[gene_id] = math.log(0.125 + gene_length, 2)

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
        #gene_id = gff.gtf_kv(a[8])['gene_id']
        gene_id = a[8].split(';')[0].split('"')[1]
        sample_genes.add(gene_id)

    ############################################
    # learn fpkm densities
    ############################################
    min_length = 0.125
    sample_lengths = np.array([[gene_lengths.get(gene_id, min_length)] for gene_id in sample_genes])
    sample_lengths_kde = KernelDensity(kernel='gaussian', bandwidth=0.5).fit(sample_lengths)

    distr_lengths = np.array([[gene_lengths.get(gene_id, min_length)] for gene_id in distr_genes])
    distr_lengths_kde = KernelDensity(kernel='gaussian', bandwidth=0.5).fit(distr_lengths)

    ############################################
    # choose genes
    ############################################
    # for gene in sample genes
    chosen_genes = set()
    for gene_id in sample_genes:
        sample_dens = math.exp(sample_lengths_kde.score(gene_lengths.get(gene_id, min_length)))
        distr_dens = math.exp(distr_lengths_kde.score(gene_lengths.get(gene_id, min_length)))

        sample_p = (options.num_sample/float(len(sample_genes)))*(distr_dens/sample_dens)
        if random.random() < sample_p:
            chosen_genes.add(gene_id)

    ############################################
    # plot distributions to see how we did
    ############################################
    df = {'length':[], 'class':[]}
    df['length'] += [gene_lengths.get(gene_id, min_length) for gene_id in chosen_genes]
    df['class'] += ['sampled']*len(chosen_genes)
    df['length'] += [gene_lengths.get(gene_id, min_length) for gene_id in sample_genes]
    df['class'] += ['original']*len(sample_genes)
    df['length'] += [gene_lengths.get(gene_id, min_length) for gene_id in distr_genes]
    df['class'] += ['distribution']*len(distr_genes)

    r_script = '/Users/chinmayshukla/Documents/Research/firre/bin/sample_genes_fpkm.r'
    ggplot.plot(r_script, df, [])
    ggplot.print_df(df, 'sample.txt')
    ############################################
    # output chosen genes as GTF
    ############################################
    for line in open(sample_gtf):
        a = line.split('\t')
        #gene_id = gff.gtf_kv(a[8])['gene_id']
        gene_id = a[8].split(';')[0].split('"')[1]
        if gene_id in chosen_genes:
            print line,


################################################################################
# __main__
################################################################################
if __name__ == '__main__':
    main()
