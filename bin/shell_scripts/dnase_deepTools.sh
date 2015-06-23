#!/bin/sh

samtools index /Users/chinmayshukla/Documents/Research/common/data/bam_files/human_hg19/dhs/uw_dnase1_hs/HeLa_rep1.sorted.bam

samtools index /Users/chinmayshukla/Documents/Research/common/data/bam_files/human_hg19/dhs/uw_dnase1_hs/HeLa_rep2.sorted.bam

samtools index /Users/chinmayshukla/Documents/Research/common/data/bam_files/human_hg19/dhs/uw_dnase1_hs/GM12878_rep1.sorted.bam

samtools index /Users/chinmayshukla/Documents/Research/common/data/bam_files/human_hg19/dhs/uw_dnase1_hs/GM12878_rep2.sorted.bam

samtools index /Users/chinmayshukla/Documents/Research/common/data/bam_files/human_hg19/dhs/uw_dnase1_hs/NHLF_rep1.sorted.bam

samtools index /Users/chinmayshukla/Documents/Research/common/data/bam_files/human_hg19/dhs/uw_dnase1_hs/NHLF_rep2.sorted.bam

# HeLa

echo 'Processing HeLa datasets'

bamCompare -b1 /Users/chinmayshukla/Documents/Research/common/data/bam_files/human_hg19/dhs/uw_dnase1_hs/HeLa_rep1.sorted.bam -b2 /Users/chinmayshukla/Documents/Research/common/data/bam_files/human_hg19/dhs/uw_dnase1_hs/HeLa_rep2.sorted.bam -o results/5-31-15/HeLa_uw_dnase1.bw -of bigwig --scaleFactorsMethod SES

computeMatrix scale-regions -S results/5-31-15/HeLa_uw_dnase1.bw -R results/5-26-15/hg19_rm_out_final_filtered.bed -out results/5-31-15/HeLa_rm_out_final_filtered.gz --outFileNameMatrix results/5-31-15/HeLa_rm_out_final_filtered.tab -m 100 --startLabel RSS --endLabel RES -a 0 -b 0 -bs 10

computeMatrix scale-regions -S results/5-31-15/HeLa_uw_dnase1.bw -R results/5-26-15/hg19_rm_out_final_filtered.bed -out results/5-31-15/HeLa_rm_out_final_filtered_window.gz --outFileNameMatrix results/5-31-15/HeLa_rm_out_final_filtered_window.tab -m 1000 --startLabel RSS --endLabel RES -a 10000 -b 10000 -bs 10

heatmapper -m results/5-31-15/HeLa_rm_out_final_filtered.gz -out results/5-31-15/HeLa_rm_out_final_filtered.pdf

heatmapper -m results/5-31-15/HeLa_rm_out_final_filtered_window.gz -out results/5-31-15/HeLa_rm_out_final_filtered_window.pdf


# GM12878

echo 'Processing GM12878 datasets'

bamCompare -b1 /Users/chinmayshukla/Documents/Research/common/data/bam_files/human_hg19/dhs/uw_dnase1_hs/GM12878_rep1.sorted.bam -b2 /Users/chinmayshukla/Documents/Research/common/data/bam_files/human_hg19/dhs/uw_dnase1_hs/GM12878_rep2.sorted.bam -o results/5-31-15/GM12878_uw_dnase1.bw -of bigwig --scaleFactorsMethod SES

computeMatrix scale-regions -S results/5-31-15/GM12878_uw_dnase1.bw -R results/5-26-15/hg19_rm_out_final_filtered.bed -out results/5-31-15/GM12878_rm_out_final_filtered.gz --outFileNameMatrix results/5-31-15/GM12878_rm_out_final_filtered.tab -m 100 --startLabel RSS --endLabel RES -a 0 -b 0 -bs 10

computeMatrix scale-regions -S results/5-31-15/GM12878_uw_dnase1.bw -R results/5-26-15/hg19_rm_out_final_filtered.bed -out results/5-31-15/GM12878_rm_out_final_filtered_window.gz --outFileNameMatrix results/5-31-15/GM12878_rm_out_final_filtered_window.tab -m 1000 --startLabel RSS --endLabel RES -a 10000 -b 10000 -bs 10

heatmapper -m results/5-31-15/GM12878_rm_out_final_filtered.gz -out results/5-31-15/GM12878_rm_out_final_filtered.pdf

heatmapper -m results/5-31-15/GM12878_rm_out_final_filtered_window.gz -out results/5-31-15/GM12878_rm_out_final_filtered_window.pdf


# NHLF

echo 'Processing NHLF datasets'

bamCompare -b1 /Users/chinmayshukla/Documents/Research/common/data/bam_files/human_hg19/dhs/uw_dnase1_hs/NHLF_rep1.sorted.bam -b2 /Users/chinmayshukla/Documents/Research/common/data/bam_files/human_hg19/dhs/uw_dnase1_hs/NHLF_rep2.sorted.bam -o results/5-31-15/NHLF_uw_dnase1.bw -of bigwig --scaleFactorsMethod SES

computeMatrix scale-regions -S results/5-31-15/NHLF_uw_dnase1.bw -R results/5-26-15/hg19_rm_out_final_filtered.bed -out results/5-31-15/NHLF_rm_out_final_filtered.gz --outFileNameMatrix results/5-31-15/NHLF_rm_out_final_filtered.tab -m 100 --startLabel RSS --endLabel RES -a 0 -b 0 -bs 10

computeMatrix scale-regions -S results/5-31-15/NHLF_uw_dnase1.bw -R results/5-26-15/hg19_rm_out_final_filtered.bed -out results/5-31-15/NHLF_rm_out_final_filtered_window.gz --outFileNameMatrix results/5-31-15/NHLF_rm_out_final_filtered_window.tab -m 1000 --startLabel RSS --endLabel RES -a 10000 -b 10000 -bs 10

heatmapper -m results/5-31-15/NHLF_rm_out_final_filtered.gz -out results/5-31-15/NHLF_rm_out_final_filtered.pdf

heatmapper -m results/5-31-15/NHLF_rm_out_final_filtered_window.gz -out results/5-31-15/NHLF_rm_out_final_filtered_window.pdf
