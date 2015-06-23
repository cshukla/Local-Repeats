#!/bin/bash

#SBATCH -N1
#SBATCH -n4
#SBATCH --mem-per-cpu=4096M
#SBATCH -t16:00:00
#SBATCH -p general
#SBATCH --qos=test

bam_1=$1'_rep1_gc_corrected.sorted.bam'
bam_2=$1'_rep2_gc_corrected.sorted.bam'
bw_output=$1'_gc_corrected.bw'

bed='results/5-26-15/hg19_rm_out_final_filtered.bed'

mat_output_span=$1'_gc_corrected_rm_out_final_filtered_span.gz'
mat_table_output_span=$1'_gc_corrected_rm_out_final_filtered_span.tab'
mat_output_window=$1'_gc_corrected_rm_out_final_filtered_window.gz'
mat_table_output_window=$1'_gc_corrected_rm_out_final_filtered_window.tab'

heat_span=$1'_gc_corrected_rm_out_final_filtered_span_heat.pdf'
heat_span_data=$1'_gc_corrected_rm_out_final_filtered_span_heat.dat'
heat_span_sorted=$1'_gc_corrected_rm_out_final_filtered_span_heat_sorted_regions.txt'
heat_span_mat=$1'_gc_corrected_rm_out_final_filtered_span_heat.tab'
heat_window=$1'_gc_corrected_rm_out_final_filtered_window_heat.pdf'
heat_window_data=$1'_gc_corrected_rm_out_final_filtered_window_heat.dat'
heat_window_sorted=$1'_gc_corrected_rm_out_final_filtered_window_heat_sorted_regions.txt'
heat_window_mat=$1'_gc_corrected_rm_out_final_filtered_window_heat.tab'



bamCompare -b1 $bam_1 -b2 $bam_2 -o $bw_output --ratio add --normalizeTo1x 2451960000 -p max 

computeMatrix scale-regions -S $bw_output -R $bed -out $mat_output_span --outFileNameMatrix $mat_table_output_span -m 100 --startLabel RSS --endLabel RES -a 0 -b 0 -bs 10

computeMatrix scale-regions -S $bw_output -R $bed -out $mat_output_window --outFileNameMatrix $mat_table_output_window -m 100 --startLabel RSS --endLabel RES -a 10000 -b 10000 -bs 10

heatmapper -m $mat_output_span -out $heat_span --outFileNameData $heat_span_data --outFileSortedRegions $heat_span_sorted --outFileNameMatrix $heat_span_mat 

heatmapper -m $mat_output_window -out $heat_window --outFileNameData $heat_window_data --outFileSortedRegions $heat_window_sorted --outFileNameMatrix $heat_window_mat 
