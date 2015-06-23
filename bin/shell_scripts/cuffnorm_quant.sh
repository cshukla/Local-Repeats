#!/bin/bash

#SBATCH -N1
#SBATCH -n8
#SBATCH --mem-per-cpu=6000M
#SBATCH -t48:00:00
#SBATCH -p general
#SBATCH --qos=test

cuffnorm --output-format cuffdiff -o results/5-23-15/cuffnorm_tissue_quantification -L adipose,adrenal,brain,breast,colon,h1ESC,heart,kidney,liver,lung,lymph_node,ovary,prostate,skeletal_muscle,testes,thyroid,white_blood_cells -p 8 results/5-22-15/protein_coding_lncrna_merged.gtf results/5-22-15/adipose/abundances.cxb results/5-22-15/adrenal/abundances.cxb results/5-22-15/brain/abundances.cxb results/5-22-15/breast/abundances.cxb results/5-22-15/colon/abundances.cxb results/5-22-15/h1esc_JR2/abundances.cxb results/5-22-15/heart/abundances.cxb results/5-22-15/kidney/abundances.cxb results/5-22-15/liver/abundances.cxb results/5-22-15/lung/abundances.cxb results/5-22-15/lymphnode/abundances.cxb results/5-22-15/ovary/abundances.cxb results/5-22-15/prostate/abundances.cxb results/5-22-15/skeletal_muscle/abundances.cxb results/5-22-15/testes/abundances.cxb results/5-22-15/thyroid/abundances.cxb results/5-22-15/white_blood_cells/abundances.cxb 