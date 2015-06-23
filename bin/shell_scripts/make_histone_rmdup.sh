#!/bin/bash

#SBATCH -N1
#SBATCH -n4
#SBATCH --mem-per-cpu=4096M
#SBATCH -t16:00:00
#SBATCH -p general
#SBATCH --qos=test

# Get bigwig files for all conditions
sample_name=$1
bw_base='/Users/chinmayshukla/Documents/Research/common/data/bam_files/human_hg19/chip_seq/broad_histone/'
control_bw=$bw_base'rmdup_control_'$1'.bw'
h3k4me1_bw=$bw_base'rmdup_h3k4me1_'$1'.bw'
h3k4me3_bw=$bw_base'rmdup_h3k4me3_'$1'.bw'
h3k27ac_bw=$bw_base'rmdup_h3k27ac_'$1'.bw'
h3k27me3_bw=$bw_base'rmdup_h3k27me3_'$1'.bw'

# Get BED file with regions to make plots
bed='results/5-26-15/hg19_rm_out_final_filtered.bed'

# Declare output files for all the conditions

# 1. H3K4Me3
# bigwig Compare Output
h3k4me3_input_norm_bw='results/6-17-15/h3k4me3_'$1'_input_norm.bw'
# Compute Matrix Outputs
h3k4me3_span_output='results/6-17-15/h3k4me3_'$1'_rm_out_final_filtered_span.gz'
h3k4me3_span_tab='results/6-17-15/h3k4me3_'$1'_rm_out_final_filtered_span.tab'
h3k4me3_window_output='results/6-17-15/h3k4me3_'$1'_rm_out_final_filtered_window.gz'
h3k4me3_window_tab='results/6-17-15/h3k4me3_'$1'_rm_out_final_filtered_window.tab'
# HeatMapper Outputs
h3k4me3_heat_span='results/6-17-15/h3k4me3_'$1'_rm_out_final_filtered_span_heat.svg'
h3k4me3_heat_span_data='results/6-17-15/h3k4me3_'$1'_rm_out_final_filtered_span_heat.dat'
h3k4me3_heat_span_sorted='results/6-17-15/h3k4me3_'$1'_rm_out_final_filtered_span_heat_sorted_regions.txt'
h3k4me3_heat_span_mat='results/6-17-15/h3k4me3_'$1'_rm_out_final_filtered_span_heat.tab'
h3k4me3_heat_window='results/6-17-15/h3k4me3_'$1'_rm_out_final_filtered_window_heat.svg'
h3k4me3_heat_window_data='results/6-17-15/h3k4me3_'$1'_rm_out_final_filtered_window_heat.dat'
h3k4me3_heat_window_sorted='results/6-17-15/h3k4me3_'$1'_rm_out_final_filtered_window_heat_sorted_regions.txt'
h3k4me3_heat_window_mat='results/6-17-15/h3k4me3_'$1'_rm_out_final_filtered_window_heat.tab'

# 2. H3K4Me1
# bigwig Compare Output
h3k4me1_input_norm_bw='results/6-17-15/h3k4me1_'$1'_input_norm.bw'
# Compute Matrix Outputs
h3k4me1_span_output='results/6-17-15/h3k4me1_'$1'_rm_out_final_filtered_span.gz'
h3k4me1_span_tab='results/6-17-15/h3k4me1_'$1'_rm_out_final_filtered_span.tab'
h3k4me1_window_output='results/6-17-15/h3k4me1_'$1'_rm_out_final_filtered_window.gz'
h3k4me1_window_tab='results/6-17-15/h3k4me1_'$1'_rm_out_final_filtered_window.tab'
# HeatMapper Outputs
h3k4me1_heat_span='results/6-17-15/h3k4me1_'$1'_rm_out_final_filtered_span_heat.svg'
h3k4me1_heat_span_data='results/6-17-15/h3k4me1_'$1'_rm_out_final_filtered_span_heat.dat'
h3k4me1_heat_span_sorted='results/6-17-15/h3k4me1_'$1'_rm_out_final_filtered_span_heat_sorted_regions.txt'
h3k4me1_heat_span_mat='results/6-17-15/h3k4me1_'$1'_rm_out_final_filtered_span_heat.tab'
h3k4me1_heat_window='results/6-17-15/h3k4me1_'$1'_rm_out_final_filtered_window_heat.svg'
h3k4me1_heat_window_data='results/6-17-15/h3k4me1_'$1'_rm_out_final_filtered_window_heat.dat'
h3k4me1_heat_window_sorted='results/6-17-15/h3k4me1_'$1'_rm_out_final_filtered_window_heat_sorted_regions.txt'
h3k4me1_heat_window_mat='results/6-17-15/h3k4me1_'$1'_rm_out_final_filtered_window_heat.tab'

# 3. H3K27Ac
# bigwig Compare Output
h3k27ac_input_norm_bw='results/6-17-15/h3k27ac_'$1'_input_norm.bw'
# Compute Matrix Outputs
h3k27ac_span_output='results/6-17-15/h3k27ac_'$1'_rm_out_final_filtered_span.gz'
h3k27ac_span_tab='results/6-17-15/h3k27ac_'$1'_rm_out_final_filtered_span.tab'
h3k27ac_window_output='results/6-17-15/h3k27ac_'$1'_rm_out_final_filtered_window.gz'
h3k27ac_window_tab='results/6-17-15/h3k27ac_'$1'_rm_out_final_filtered_window.tab'
# HeatMapper Outputs
h3k27ac_heat_span='results/6-17-15/h3k27ac_'$1'_rm_out_final_filtered_span_heat.svg'
h3k27ac_heat_span_data='results/6-17-15/h3k27ac_'$1'_rm_out_final_filtered_span_heat.dat'
h3k27ac_heat_span_sorted='results/6-17-15/h3k27ac_'$1'_rm_out_final_filtered_span_heat_sorted_regions.txt'
h3k27ac_heat_span_mat='results/6-17-15/h3k27ac_'$1'_rm_out_final_filtered_span_heat.tab'
h3k27ac_heat_window='results/6-17-15/h3k27ac_'$1'_rm_out_final_filtered_window_heat.svg'
h3k27ac_heat_window_data='results/6-17-15/h3k27ac_'$1'_rm_out_final_filtered_window_heat.dat'
h3k27ac_heat_window_sorted='results/6-17-15/h3k27ac_'$1'_rm_out_final_filtered_window_heat_sorted_regions.txt'
h3k27ac_heat_window_mat='results/6-17-15/h3k27ac_'$1'_rm_out_final_filtered_window_heat.tab'

# 4. H3K27Me3
# bigwig Compare Output
h3k27me3_input_norm_bw='results/6-17-15/h3k27me3_'$1'_input_norm.bw'
# Compute Matrix Outputs
h3k27me3_span_output='results/6-17-15/h3k27me3_'$1'_rm_out_final_filtered_span.gz'
h3k27me3_span_tab='results/6-17-15/h3k27me3_'$1'_rm_out_final_filtered_span.tab'
h3k27me3_window_output='results/6-17-15/h3k27me3_'$1'_rm_out_final_filtered_window.gz'
h3k27me3_window_tab='results/6-17-15/h3k27me3_'$1'_rm_out_final_filtered_window.tab'
# HeatMapper Outputs
h3k27me3_heat_span='results/6-17-15/h3k27me3_'$1'_rm_out_final_filtered_span_heat.svg'
h3k27me3_heat_span_data='results/6-17-15/h3k27me3_'$1'_rm_out_final_filtered_span_heat.dat'
h3k27me3_heat_span_sorted='results/6-17-15/h3k27me3_'$1'_rm_out_final_filtered_span_heat_sorted_regions.txt'
h3k27me3_heat_span_mat='results/6-17-15/h3k27me3_'$1'_rm_out_final_filtered_span_heat.tab'
h3k27me3_heat_window='results/6-17-15/h3k27me3_'$1'_rm_out_final_filtered_window_heat.svg'
h3k27me3_heat_window_data='results/6-17-15/h3k27me3_'$1'_rm_out_final_filtered_window_heat.dat'
h3k27me3_heat_window_sorted='results/6-17-15/h3k27me3_'$1'_rm_out_final_filtered_window_heat_sorted_regions.txt'
h3k27me3_heat_window_mat='results/6-17-15/h3k27me3_'$1'_rm_out_final_filtered_window_heat.tab'

# Plots for H3K4Me3
bigwigCompare -b1 $h3k4me3_bw -b2 $control_bw -o $h3k4me3_input_norm_bw --ratio log2 -p max 
computeMatrix scale-regions -S $h3k4me3_input_norm_bw -R $bed -out $h3k4me3_span_output --outFileNameMatrix $h3k4me3_span_tab -m 100 --startLabel RSS --endLabel RES -a 0 -b 0 -bs 10 --skipZeros
computeMatrix scale-regions -S $h3k4me3_input_norm_bw -R $bed -out $h3k4me3_window_output --outFileNameMatrix $h3k4me3_window_tab -m 100 --startLabel RSS --endLabel RES -a 10000 -b 10000 -bs 10 --skipZeros
heatmapper -m $h3k4me3_span_output -out $h3k4me3_heat_span --outFileNameData $h3k4me3_heat_span_data --outFileSortedRegions $h3k4me3_heat_span_sorted --outFileNameMatrix $h3k4me3_heat_span_mat  --colorMap YlGnBu
heatmapper -m $h3k4me3_window_output -out $h3k4me3_heat_window --outFileNameData $h3k4me3_heat_window_data --outFileSortedRegions $h3k4me3_heat_window_sorted --outFileNameMatrix $h3k4me3_heat_window_mat  --colorMap YlGnBu 

# Plots for H3K4Me1
bigwigCompare -b1 $h3k4me1_bw -b2 $control_bw -o $h3k4me1_input_norm_bw --ratio log2 -p max 
computeMatrix scale-regions -S $h3k4me1_input_norm_bw -R $bed -out $h3k4me1_span_output --outFileNameMatrix $h3k4me1_span_tab -m 100 --startLabel RSS --endLabel RES -a 0 -b 0 -bs 10 --skipZeros
computeMatrix scale-regions -S $h3k4me1_input_norm_bw -R $bed -out $h3k4me1_window_output --outFileNameMatrix $h3k4me1_window_tab -m 100 --startLabel RSS --endLabel RES -a 10000 -b 10000 -bs 10 --skipZeros
heatmapper -m $h3k4me1_span_output -out $h3k4me1_heat_span --outFileNameData $h3k4me1_heat_span_data --outFileSortedRegions $h3k4me1_heat_span_sorted --outFileNameMatrix $h3k4me1_heat_span_mat  --colorMap YlGnBu 
heatmapper -m $h3k4me1_window_output -out $h3k4me1_heat_window --outFileNameData $h3k4me1_heat_window_data --outFileSortedRegions $h3k4me1_heat_window_sorted --outFileNameMatrix $h3k4me1_heat_window_mat --colorMap YlGnBu

# Plots for H3K27Ac
bigwigCompare -b1 $h3k27ac_bw -b2 $control_bw -o $h3k27ac_input_norm_bw --ratio log2 -p max 
computeMatrix scale-regions -S $h3k27ac_input_norm_bw -R $bed -out $h3k27ac_span_output --outFileNameMatrix $h3k27ac_span_tab -m 100 --startLabel RSS --endLabel RES -a 0 -b 0 -bs 10 --skipZeros
computeMatrix scale-regions -S $h3k27ac_input_norm_bw -R $bed -out $h3k27ac_window_output --outFileNameMatrix $h3k27ac_window_tab -m 100 --startLabel RSS --endLabel RES -a 10000 -b 10000 -bs 10 --skipZeros
heatmapper -m $h3k27ac_span_output -out $h3k27ac_heat_span --outFileNameData $h3k27ac_heat_span_data --outFileSortedRegions $h3k27ac_heat_span_sorted --outFileNameMatrix $h3k27ac_heat_span_mat --colorMap YlGnBu
heatmapper -m $h3k27ac_window_output -out $h3k27ac_heat_window --outFileNameData $h3k27ac_heat_window_data --outFileSortedRegions $h3k27ac_heat_window_sorted --outFileNameMatrix $h3k27ac_heat_window_mat --colorMap YlGnBu

# Plots for H3K27Me3
bigwigCompare -b1 $h3k27me3_bw -b2 $control_bw -o $h3k27me3_input_norm_bw --ratio log2 -p max 
computeMatrix scale-regions -S $h3k27me3_input_norm_bw -R $bed -out $h3k27me3_span_output --outFileNameMatrix $h3k27me3_span_tab -m 100 --startLabel RSS --endLabel RES -a 0 -b 0 -bs 10 --skipZeros
computeMatrix scale-regions -S $h3k27me3_input_norm_bw -R $bed -out $h3k27me3_window_output --outFileNameMatrix $h3k27me3_window_tab -m 100 --startLabel RSS --endLabel RES -a 10000 -b 10000 -bs 10 --skipZeros
heatmapper -m $h3k27me3_span_output -out $h3k27me3_heat_span --outFileNameData $h3k27me3_heat_span_data --outFileSortedRegions $h3k27me3_heat_span_sorted --outFileNameMatrix $h3k27me3_heat_span_mat --colorMap YlGnBu
heatmapper -m $h3k27me3_window_output -out $h3k27me3_heat_window --outFileNameData $h3k27me3_heat_window_data --outFileSortedRegions $h3k27me3_heat_window_sorted --outFileNameMatrix $h3k27me3_heat_window_mat --colorMap YlGnBu

