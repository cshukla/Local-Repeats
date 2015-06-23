#!/bin/sh

#SBATCH -N1
#SBATCH -n8
#SBATCH --mem-per-cpu=6000M
#SBATCH -t48:00:00
#SBATCH -p general
#SBATCH --qos=test

output_name=$1
output_dir='/n/rinn_data1/users/cshukla/local_repeats/results/5-19-15/'$output_name
genome_fa='/n/rinn_data1/users/cshukla/common/data/bowtie2_indexes/human_hg19/hg19.fa'
gtf_file='/n/rinn_data1/users/cshukla/local_repeats/results/5-15-15/gencode_moran_merged_catalog.gtf'
reads=$2

cuffquant -p 8 -b $genome_fa -o $output_dir -u $gtf_file $reads