#!/usr/bin/env python

##################################################################################
# iterative_mapping.py
#
# This scripts takes .sra files from fastq directory, maps them to the genome and
# saves them to .hdf5 files in a directory "genomeName-mapped".
# Please follow comments along the text.
# This script has been modified from hiclib package tutorial (pipeline-2014).
##################################################################################

import atexit
import glob
import os
import logging
from hiclib import mapping
from mirnylib import h5dict, genome
from optparse import OptionParser

import numpy as np
logging.basicConfig(level=logging.DEBUG)

def cleanFile(filename):
    if os.path.exists(filename):
        os.remove(filename)

def main():
    usage='usage:%prog [options]'
    parser = OptionParser(usage)
    parser.add_option('-g', dest='genomeName', default="hg19", type=str, help='Name of the genome in HiC experiment')
    parser.add_option('-p', dest='threads', default=10, type=int, help='Number of threads used by Bowtie2 for mapping')
    parser.add_option('-b', dest='bowtiePath', default='/n/sw/bowtie2-2.0.5/bowtie2', type=str, help='Absolute path for Bowtie2')
    parser.add_option('-f', dest='fastqDir', default='fastq', type=str, help='Directory with FASTQ files')
    parser.add_option('-l', dest='lengthDir', default='lengths', type=str, help='Directory with Lengths files')
    parser.add_option('-i', dest='bowtieIndex', default='/n/rinn_data1/users/cshukla/common/data/bowtie2_indexes/human_hg19/hg19', type=str, help='Path for Bowite2 index')
    parser.add_option('-t', dest='tmpDir', default='/n/regal/rinn_lab/cshukla/hic', type=str, help='Scractch space for temporary files')
    parser.add_option('-d', dest='genome_db', default='/n/rinn_data1/users/cshukla/common/data/hg19/chrom_fasta', type=str, help='Directory with gap and genome FASTA files')
    parser.add_option('-c', dest='readChrms', default='#XYM', type=str, help='Chromosomes to read from genome database directory')
    (options, args) = parser.parse_args()
    
    genomeName = options.genomeName
    threads = options.threads
    bowtiePath = options.bowtiePath
    if not os.path.exists(bowtiePath): raise
    fastqDir = options.fastqDir
    lengthDir = options.lengthDir
    bowtieIndex = options.bowtieIndex
    tmpDir = options.tmpDir
    samFolder = "sams-{0}".format(genomeName)
    savePath = "mapped-{0}".format(genomeName)

    # Specify location of the genome files here
    genome_db = genome.Genome(options.genome_db, readChrms=list(options.readChrms))

    if not os.path.exists(samFolder):
        os.mkdir(samFolder)

    if not os.path.exists(savePath):
        os.mkdir(savePath)

    # three times because we want to get sure that if some other process got killed and left an
    # un-mapped file (which we skipped because it had a lock on it), then we would map it as well.
    
    for i in 3 * sorted(os.listdir(fastqDir)):
        expName = i
        print i
        file1 = os.path.join(fastqDir, expName)
        if not os.path.exists(file1): raise
        if not os.path.exists(file1): raise
        lengthFile = os.path.join(lengthDir, expName)
        length = (int(open(lengthFile).readlines()[0]) - 1) / 2
        print length
        minlen, step = calculateStep(length, 25)


        finalName = '%s/%s.hdf5' % (savePath, expName.replace(".sra", ""))
        lockName = finalName + ".lock"
        print finalName

        if os.path.exists(finalName) and not os.path.exists(lockName):
            print "skipping", finalName
            continue

        if os.path.exists(lockName):
            print "someone is working on", finalName
            continue

        lock = open(lockName, "w")
        lock.close()

        atexit.register(cleanFile, lockName)

        os.system("rm -rf {0}/{1}*".format(samFolder, expName.replace(".sra", "")))

        # Guess if the input is SRA or FASTQ
        if expName[-3:] == 'sra':
            bash_reader = "fastq-dump -Z"
        else:
            bash_reader= ""

        # First step. Map the reads iteratively.
        mapping.iterative_mapping(
            bowtie_path=bowtiePath,
            bowtie_index_path=bowtieIndex,
            fastq_path=file1,
            out_sam_path='{0}/{1}_1.bam'.format(samFolder, expName),
            min_seq_len=minlen,  # for bacteria mimimal mappable length is 15 bp, so I start with something slightly longer
            len_step=step,  # and go with a usualy step
            nthreads=threads,  # on intel corei7 CPUs 4 threads are as fast as
                         # 8, but leave some room for you other applications
            # max_reads_per_chunk = 10000000,  #optional, on low-memory machines
            temp_dir=tmpDir,
            seq_start=0,
            seq_end=length,
            bash_reader=bash_reader,
            bowtie_flags=" --very-sensitive ",
            )

        mapping.iterative_mapping(
            bowtie_path=bowtiePath,
            bowtie_index_path=bowtieIndex,
            fastq_path=file1,
            out_sam_path='{0}/{1}_2.bam'.format(samFolder, expName),
            min_seq_len=minlen,
            len_step=step,
            nthreads=threads,  # on intel corei7 CPUs 4 threads are as fast as
                         # 8, but leave some room for you other applications
            # max_reads_per_chunk = 10000000,  #optional, on low-memory machines
            temp_dir=tmpDir,
            seq_start=length,
            seq_end=2 * length,
            bash_reader="fastq-dump -Z",
            bowtie_flags=" --very-sensitive ",
            )

        # Second step. Parse the mapped sequences into a Python data structure,
        #    assign the ultra-sonic fragments to restriction fragments.
        mapped_reads = h5dict.h5dict(finalName)

        mapping.parse_sam(
            sam_basename1='{0}/{1}_1.bam'.format(samFolder, expName),
            sam_basename2='{0}/{1}_2.bam'.format(samFolder, expName),
            out_dict=mapped_reads,
            genome_db=genome_db,
    	save_seqs=False)

        os.remove(lockName)

def calculateStep(length, minlen, approxStep=10, maxSteps=4):
    """returns minimum length and step based on the
    length of sequence and proposed minimum length"""

    actualDif = length - minlen
    if actualDif < approxStep * 0.6:
        return length, 100

    numIter = np.array(np.around(actualDif / float(approxStep)), dtype=int)
    if numIter == 0:
        numIter = 1
    if numIter > maxSteps:
        numIter = maxSteps
    actualStep = actualDif / numIter

    minlen = length - actualStep * numIter

    return minlen, actualStep

##################################################################################
# main()
##################################################################################
if __name__ == '__main__':
    main()