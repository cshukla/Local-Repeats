library(ggplot2)

# Input TE Counts
lr_te_counts <- read.table(file="/Users/chinmayshukla/Documents/Research/local_repeats/results/6-18-15/lr_lncrnas_te_counts.txt", sep="\t", col.names = c("Chromosome", "Start", "End", "Gene_Name", "TE_Counts"))
non_lr_te_counts <- read.table(file="/Users/chinmayshukla/Documents/Research/local_repeats/results/6-18-15/non_lr_lncrnas_te_counts.txt", sep="\t", col.names = c("Chromosome", "Start", "End", "Gene_Name", "TE_Counts"))

# Compute Stats
wilcox.test(lr_te_counts$TE_Counts, non_lr_te_counts$TE_Counts)

# Make DataFrame
te_counts_df <- data.frame(Type=c(rep("LR_LncRNA", times=length(lr_te_counts$TE_Counts)), rep("Non_LR_LncRNA", times=length(non_lr_te_counts$TE_Counts))), TE_Counts=c(lr_te_counts$TE_Counts, non_lr_te_counts$TE_Counts))

# Make plots
ggplot(te_counts_df, aes(x=Type, y=log(TE_Counts + 1, 10), color=Type)) + geom_boxplot() + theme_bw() + scale_color_manual(values=c("red", "grey50"))
ggplot(te_counts_df, aes(x=log(TE_Counts + 1, 10))) + geom_density(aes(color=Type)) + theme_bw() + scale_color_manual(values=c("red", "grey50"))
ggplot(te_counts_df, aes(x=log(TE_Counts + 1, 10))) + stat_ecdf(aes(color=Type)) + theme_bw() + scale_color_manual(values=c("red", "grey50"))
ggplot(te_counts_df, aes(x=Type, y=log(TE_Counts + 1, 10), color=Type)) + geom_violin() + theme_bw() + scale_color_manual(values=c("red", "grey50"))
