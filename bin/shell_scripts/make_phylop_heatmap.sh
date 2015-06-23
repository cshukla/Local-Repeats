#!/bin/sh

phylop_bw=$1
bed='results/5-26-15/hg19_rm_out_final_filtered.bed'

# Compute Matrix Outputs
phylop_span_output='results/6-18-15/phylop_rm_out_final_filtered_span.gz'
phylop_span_tab='results/6-18-15/phylop_rm_out_final_filtered_span.tab'
phylop_window_output='results/6-18-15/phylop_rm_out_final_filtered_window.gz'
phylop_window_tab='results/6-18-15/phylop_rm_out_final_filtered_window.tab'
# HeatMapper Outputs
phylop_heat_span='results/6-18-15/phylop_rm_out_final_filtered_span_heat.svg'
phylop_heat_span_data='results/6-18-15/phylop_rm_out_final_filtered_span_heat.dat'
phylop_heat_span_sorted='results/6-18-15/phylop_rm_out_final_filtered_span_heat_sorted_regions.txt'
phylop_heat_span_mat='results/6-18-15/phylop_rm_out_final_filtered_span_heat.tab'
phylop_heat_window='results/6-18-15/phylop_rm_out_final_filtered_window_heat.svg'
phylop_heat_window_data='results/6-18-15/phylop_rm_out_final_filtered_window_heat.dat'
phylop_heat_window_sorted='results/6-18-15/phylop_rm_out_final_filtered_window_heat_sorted_regions.txt'
phylop_heat_window_mat='results/6-18-15/phylop_rm_out_final_filtered_window_heat.tab'

# Plots
computeMatrix scale-regions -S $phylop_bw -R $bed -out $phylop_span_output --outFileNameMatrix $phylop_span_tab -m 100 --startLabel RSS --endLabel RES -a 0 -b 0 -bs 10 --skipZeros
computeMatrix scale-regions -S $phylop_bw -R $bed -out $phylop_window_output --outFileNameMatrix $phylop_window_tab -m 100 --startLabel RSS --endLabel RES -a 10000 -b 10000 -bs 10 --skipZeros
heatmapper -m $phylop_span_output -out $phylop_heat_span --outFileNameData $phylop_heat_span_data --outFileSortedRegions $phylop_heat_span_sorted --outFileNameMatrix $phylop_heat_span_mat  --colorMap YlGnBu
heatmapper -m $phylop_window_output -out $phylop_heat_window --outFileNameData $phylop_heat_window_data --outFileSortedRegions $phylop_heat_window_sorted --outFileNameMatrix $phylop_heat_window_mat  --colorMap YlGnBu 
