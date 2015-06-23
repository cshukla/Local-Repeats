library(ggplot2)

# Read input BED files
lr_lncrnas <- read.table(file="Documents/Research/local_repeats/results/5-19-15/lr_lncrnas.genes.bed", sep="\t", col.names=c("Chromosome", "Catalog", "Type", "Start", "End", "Name"))
non_lr_lncrnas <- read.table(file="Documents/Research/local_repeats/results/5-19-15/non_lr_lncrnas.genes.bed", sep="\t", col.names=c("Chromosome", "Catalog", "Type", "Start", "End", "Name"))

# Get lengths of genes in both classes
lr_lncrna_length = lr_lncrnas$End - lr_lncrnas$Start
non_lr_lncrna_length = non_lr_lncrnas$End - non_lr_lncrnas$Start
length_df <- data.frame(Type=c(rep("LR_LncRNA", times=length(lr_lncrna_length)), rep("Non_LR_LncRNA", times=length(non_lr_lncrna_length))), Length=c(lr_lncrna_length, non_lr_lncrna_length))

# Make a boxplot, density plot, violin plot and CDF plot
ggplot(length_df, aes(x=Type, y=log(Length, base=10))) + geom_boxplot(aes(fill=Type)) + theme_bw()
ggplot(length_df, aes(x=log(Length, base=10))) + geom_density(aes(color=Type)) + theme_bw()
ggplot(length_df, aes(x=Type, y=log(Length, base=10))) + geom_violin(aes(fill=Type)) + theme_bw()
ggplot(length_df, aes(x=log(Length, base=10))) + stat_ecdf(aes(color=Type)) + theme_bw()

# Read genes to isoforms files
lr_lncrnas_isoforms <- read.table(file="Documents/Research/local_repeats/results/5-19-15/lr_lncrnas.genes.bed", sep="\t", col.names=c("Gene_ID", "Transcripts", "Isoforms"))$Isoforms
non_lr_lncrnas_isoforms <- read.table(file="Documents/Research/local_repeats/results/5-19-15/non_lr_lncrnas.genes.bed", sep="\t", col.names=c("Gene_ID", "Transcripts", "Isoforms"))$Isoforms
lr_lncrnas_isoforms <- lr_lncrnas_isoforms$Isoforms
non_lr_lncrnas_isoforms <- non_lr_lncrnas_isoforms$Isoforms
isoforms_df <- data.frame(Type=c(rep("LR_LncRNA", times=length(lr_lncrnas_isoforms)), rep("Non_LR_LncRNA", times=length(non_lr_lncrnas_isoforms))), Isoforms=c(lr_lncrnas_isoforms, non_lr_lncrnas_isoforms))

# Make a boxplot and CDF plot (Violin plot and density plot are difficult to interpret)
ggplot(isoforms_df, aes(x=Isoforms)) + stat_ecdf(aes(color=Type)) + theme_bw()
ggplot(isoforms_df, aes(x=Type, y=log(Isoforms, base=2))) + geom_boxplot(aes(fill=Type)) + theme_bw() + scale_y_continuous(limits=c(-1,7))
