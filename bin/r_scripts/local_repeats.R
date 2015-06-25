library(ggplot2)

hg19_lncrnas <- read.table("Downloads/hg19_lncRNAs.genes_df.txt", sep="\t", header=T)
hg19_lncrnas$Length <- abs(hg19_lncrnas$End - hg19_lncrnas$Start)
hg19_lncrnas$LPN <- (1000*hg19_lncrnas$Local.Repeats)/hg19_lncrnas$Length
hg19_lncrnas$TPN <- (1000*hg19_lncrnas$Tandem.Repeats)/hg19_lncrnas$Length

hg19_proteins <- read.table("Downloads/hg19_protein_coding.length.corrected.genes_df.txt", sep="\t", header=T)
hg19_proteins$Length <- abs(hg19_proteins$End - hg19_proteins$Start)
hg19_proteins$LPN <- (1000*hg19_proteins$Local.Repeats)/hg19_proteins$Length
hg19_proteins$TPN <- (1000*hg19_proteins$Tandem.Repeats)/hg19_proteins$Length

hg19_pseudogenes <- read.table("Downloads/hg19_pseudogenes.length.corrected.genes_df.txt", sep="\t", header=T)
hg19_pseudogenes$Length <- abs(hg19_pseudogenes$End - hg19_pseudogenes$Start)
hg19_pseudogenes$LPN <- (1000*hg19_pseudogenes$Local.Repeats)/hg19_pseudogenes$Length
hg19_pseudogenes$TPN <- (1000*hg19_pseudogenes$Tandem.Repeats)/hg19_pseudogenes$Length

hg19_repeats_df <- data.frame(Gene_Type=c(rep("LncRNA", times=length(hg19_lncrnas$LPN)), rep("Protein_Coding", times=length(hg19_proteins$LPN)), rep("Pseudogenes", times=length(hg19_pseudogenes$LPN))), LPN =c(hg19_lncrnas$LPN, hg19_proteins$LPN, hg19_pseudogenes$LPN), TPN=c(hg19_lncrnas$TPN, hg19_proteins$TPN, hg19_pseudogenes$TPN), Local.Repeats=c(hg19_lncrnas$Local.Repeats, hg19_proteins$Local.Repeats, hg19_pseudogenes$Local.Repeats))

hg19_non_zero_LPN <- subset(hg19_repeats_df, LPN>0)

ggplot(hg19_non_zero_LPN, aes(x=log(LPN, 2))) + stat_ecdf(aes(color=Gene_Type)) + theme_bw()
ggplot(hg19_non_zero_LPN, aes(x=log(LPN, 2))) + geom_density(aes(color=Gene_Type)) + theme_bw()
ggplot(hg19_non_zero_LPN, aes(x=Gene_Type, y=log(LPN, 2))) + geom_violin(aes(color=Gene_Type)) + theme_bw()
ggplot(hg19_non_zero_LPN, aes(x=Gene_Type, y=log(LPN, 2))) + geom_boxplot(aes(color=Gene_Type)) + theme_bw()