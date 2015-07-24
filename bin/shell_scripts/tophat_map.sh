#!/bin/sh

#SBATCH -N1
#SBATCH -n16
#SBATCH --mem-per-cpu=6000M
#SBATCH -t24:00:00
#SBATCH -p general
#SBATCH --qos=test

output_dir=$1
reads_1=$2
reads_2=$3
bowtie_index='/n/rinn_data1/users/cshukla/common/data/bowtie2_indexes/human_hg19/hg19'

tophat --no-coverage-search -o $output_dir -p 16 $bowtie_index $reads_1 $reads_2