#!/bin/bash

#SBATCH -N1
#SBATCH -n4
#SBATCH --mem-per-cpu=4096M
#SBATCH -t16:00:00
#SBATCH -p general
#SBATCH --qos=test

bit_file='/Users/chinmayshukla/Documents/Research/common/data/hg19/hg19.2bit'
bam_file='/Users/chinmayshukla/Documents/Research/common/data/bam_files/human_hg19/chip_seq/broad_histone/'$1'.sorted.bam'
freq_file='/Users/chinmayshukla/Documents/Research/local_repeats/results/6-6-15/broad_histone/'$1'_freq.txt'
bias_plot='/Users/chinmayshukla/Documents/Research/local_repeats/results/6-6-15/broad_histone/'$1'_gc_bias.pdf'
corrected_bam='/Users/chinmayshukla/Documents/Research/local_repeats/results/6-6-15/broad_histone/'$1'_gc_corrected.sorted.bam'

#computeGCBias -b $bam_file --effectiveGenomeSize 2451960000 -g $bit_file -l 36 --GCbiasFrequenciesFile $freq_file --plotFileFormat pdf --biasPlot $bias_plot -p max

correctGCBias -b $bam_file --effectiveGenomeSize 2451960000 -g $bit_file --GCbiasFrequenciesFile $freq_file -o $corrected_bam -p max
