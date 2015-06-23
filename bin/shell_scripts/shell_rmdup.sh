#!/bin/sh

sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_control_gm12878
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_control_h1esc
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_control_hela
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_control_hepg2
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_control_hsmm
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_control_nhek
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_control_nhlf
bamCoverage -b /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_control_k562_rep1.sorted.bam -o /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_control_k562.bw --normalizeTo1x 2451960000 -of bigwig

sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k4me1_gm12878
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k4me1_h1esc
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k4me1_hela
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k4me1_hepg2
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k4me1_hsmm
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k4me1_k562
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k4me1_nhlf

sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k4me3_gm12878
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k4me3_h1esc
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k4me3_hela
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k4me3_hepg2
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k4me3_hsmm
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k4me3_k562
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k4me3_nhlf

sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k27me3_gm12878
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k27me3_h1esc
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k27me3_hela
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k27me3_hepg2
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k27me3_hsmm
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k27me3_huvec
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k27me3_k562
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k27me3_nhlf

sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k27ac_gm12878
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k27ac_h1esc
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k27ac_hela
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k27ac_hepg2
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k27ac_hsmm
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k27ac_k562
sh bin/combine_reps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k27ac_nhlf



sh bin/combine_treps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_control_huvec
sh bin/combine_treps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k27ac_huvec
sh bin/combine_treps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k4me1_huvec
sh bin/combine_treps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k4me3_huvec

sh bin/combine_treps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k27ac_nhek
sh bin/combine_treps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k27me3_nhek
sh bin/combine_treps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k4me1_nhek
sh bin/combine_treps.sh /n/rinn_data1/users/cshukla/common/data/bam_files/human_hg19/chip_seq/broad_histone/chromatin_mods/rmdup_h3k4me3_nhek
