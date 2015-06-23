library(ggplot2)

setwd("Documents/Research/local_repeats")

non_lr_GM12878 <- read.table(file="results/5-31-15/non_lr_lncrna_nc_ratio_GM12878_raw.txt", sep="\t", quote="", header=T)

lr_GM12878 <- read.table(file="results/5-31-15/lr_lncrna_nc_ratio_GM12878_raw.txt", sep="\t", col.names=colnames(non_lr_GM12878), quote="")

high_lr_GM12878 <- read.table(file="results/5-31-15/high_maxFPKM_lr_lncrna_nc_ratio_GM12878_raw.txt", sep="\t", quote="", col.names=colnames(non_lr_GM12878))

merged_df_GM12878 <- data.frame(Type=c(rep("LR_LncRNA", times=length(lr_GM12878$nuclear_fpkm)), rep("Non_LR_LncRNA", times=length(non_lr_GM12878$nuclear_fpkm)), rep("highmaxFPKM", times=length(high_lr_GM12878$nuclear_fpkm))), nuclear_fpkm=c(lr_GM12878$nuclear_fpkm, non_lr_GM12878$nuclear_fpkm, high_lr_GM12878$nuclear_fpkm), cytosolic_fpkm=c(lr_GM12878$cytosolic_fpkm, non_lr_GM12878$cytosolic_fpkm, high_lr_GM12878$cytosolic_fpkm), nc_ratio=c(lr_GM12878$nc_ratio, non_lr_GM12878$nc_ratio, high_lr_GM12878$nc_ratio))

wilcox.test(log(high_lr_GM12878$nc_ratio+0.25,2), log(non_lr_GM12878$nc_ratio+0.25,2))

wilcox.test(log(lr_GM12878$nc_ratio+0.25,2), log(non_lr_GM12878$nc_ratio+0.25,2))

ggplot(merged_df_GM12878, aes(x=Type, y=log(nc_ratio+0.25,2))) + geom_boxplot() + theme_bw()
ggplot(merged_df_GM12878, aes(x=log(nc_ratio+0.25,2))) + stat_ecdf(aes(color=Type)) + theme_bw()


lr_HUVEC <- read.table(file="results/6-10-15/lr_lncrnas_huvec_fractionation.tab", sep="\t", header=T)
non_lr_HUVEC <- read.table(file="results/6-10-15/non_lr_lncrnas_huvec_fractionation.tab", sep="\t", header=T)
high_lr_HUVEC <- read.table(file="results/6-10-15/highmaxFPKM_lr_lncrnas_huvec_fractionation.tab", sep="\t", header=T)
merged_df_HUVEC <- data.frame(Type=c(rep("LR_LncRNA", times=length(lr_HUVEC$Nuclear_FPKM)), rep("Non_LR_LncRNA", times=length(non_lr_HUVEC$Nuclear_FPKM)), rep("highmaxFPKM", times=length(high_lr_HUVEC$Nuclear_FPKM))), Nuclear_FPKM=c(lr_HUVEC$Nuclear_FPKM, non_lr_HUVEC$Nuclear_FPKM, high_lr_HUVEC$Nuclear_FPKM), Cytosolic_FPKM=c(lr_HUVEC$Cytosolic_FPKM, non_lr_HUVEC$Cytosolic_FPKM, high_lr_HUVEC$Cytosolic_FPKM), NC_Ratio=c(lr_HUVEC$NC_Ratio, non_lr_HUVEC$NC_Ratio, high_lr_HUVEC$NC_Ratio))
ggplot(merged_df_HUVEC, aes(x=Type, y=log(NC_Ratio+0.25,2))) + geom_boxplot() + theme_bw()
ggsave("results/6-11-15/HUVEC_NC_Ratio_Boxplot.pdf")
ggplot(merged_df_HUVEC, aes(x=log(NC_Ratio+0.25,2))) + stat_ecdf(aes(color=Type)) + theme_bw()
ggsave("results/6-11-15/HUVEC_NC_Ratio_CDF.pdf")
wilcox.test(log(high_lr_HUVEC$NC_Ratio+0.25,2), log(non_lr_HUVEC$NC_Ratio+0.25,2))
wilcox.test(log(lr_HUVEC$NC_Ratio+0.25,2), log(non_lr_HUVEC$NC_Ratio+0.25,2))
