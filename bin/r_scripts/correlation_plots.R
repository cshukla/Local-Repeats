library(ggplot2)

# Spearman Correlation
lr_neighbors_corr <- read.table(file="Documents/Research/local_repeats/results/5-24-15/lr_lncRNAs_neighors_spearman.txt", sep="\t", header=T)
non_lr_neighbors_corr <- read.table(file="Documents/Research/local_repeats/results/5-24-15/non_lr_lncRNAs_neighors_spearman.txt", sep="\t", header=T)
lr_neighbors_corr<-subset(lr_neighbors_corr,!is.na(Spearman))
non_lr_neighbors_corr<-subset(non_lr_neighbors_corr,!is.na(Spearman))
corr_df <- data.frame(Type=c(rep("LR_LncRNA", times=length(lr_neighbors_corr$Spearman)), rep("Non_LR_LncRNA", times=length(non_lr_neighbors_corr$Spearman))), Spearman=c(lr_neighbors_corr$Spearman, non_lr_neighbors_corr$Spearman), P.Value=c(lr_neighbors_corr$p_val, non_lr_neighbors_corr$p_val))
wilcox.test(lr_neighbors_corr$Spearman, non_lr_neighbors_corr$Spearman)

# All genes plot
ggplot(corr_df, aes(x=Type, y=Spearman, color=Type)) + geom_boxplot() + theme_bw() + scale_color_manual(values=c("red", "grey50"))
ggplot(corr_df, aes(x=Spearman)) + geom_density(aes(color=Type)) + theme_bw() + scale_color_manual(values=c("red", "grey50"))
ggplot(corr_df, aes(x=Spearman)) + stat_ecdf(aes(color=Type)) + theme_bw() + scale_color_manual(values=c("red", "grey50"))
ggplot(corr_df, aes(x=Type, y=Spearman, color=Type)) + geom_violin() + theme_bw() + scale_color_manual(values=c("red", "grey50"))

# Limit to significantly correlated genes and make the same plots
lr_sig_corr <- subset(lr_neighbors_corr, p_val <0.05)
non_lr_sig_corr <- subset(non_lr_neighbors_corr, p_val<0.05)
wilcox.test(lr_sig_corr$Spearman, non_lr_sig_corr$Spearman)
corr_df <- subset(corr_df, P.Value<0.05)
ggplot(corr_df, aes(x=Type, y=Spearman, color=Type)) + geom_boxplot() + theme_bw() + scale_color_manual(values=c("red", "grey50"))
ggplot(corr_df, aes(x=Spearman)) + geom_density(aes(color=Type)) + theme_bw() + scale_color_manual(values=c("red", "grey50"))
ggplot(corr_df, aes(x=Spearman)) + stat_ecdf(aes(color=Type)) + theme_bw() + scale_color_manual(values=c("red", "grey50"))
ggplot(corr_df, aes(x=Type, y=Spearman, color=Type)) + geom_violin() + theme_bw() + scale_color_manual(values=c("red", "grey50"))

# Pearson Correlation
lr_neighbors_corr <- read.table(file="Documents/Research/local_repeats/results/5-24-15/lr_lncRNAs_neighors_pearson.txt", sep="\t", header=T)
non_lr_neighbors_corr <- read.table(file="Documents/Research/local_repeats/results/5-24-15/non_lr_lncRNAs_neighors_pearson.txt", sep="\t", header=T)
lr_neighbors_corr<-subset(lr_neighbors_corr,!is.na(Pearson))
non_lr_neighbors_corr<-subset(non_lr_neighbors_corr,!is.na(Pearson))
corr_df <- data.frame(Type=c(rep("LR_LncRNA", times=length(lr_neighbors_corr$Pearson)), rep("Non_LR_LncRNA", times=length(non_lr_neighbors_corr$Pearson))), Pearson=c(lr_neighbors_corr$Pearson, non_lr_neighbors_corr$Pearson), P.Value=c(lr_neighbors_corr$p_val, non_lr_neighbors_corr$p_val))
wilcox.test(lr_neighbors_corr$Pearson, non_lr_neighbors_corr$Pearson)

# All genes plots
ggplot(corr_df, aes(x=Type, y=Pearson, color=Type)) + geom_boxplot() + theme_bw() + scale_color_manual(values=c("red", "grey50"))
ggplot(corr_df, aes(x=Pearson)) + geom_density(aes(color=Type)) + theme_bw() + scale_color_manual(values=c("red", "grey50"))
ggplot(corr_df, aes(x=Pearson)) + stat_ecdf(aes(color=Type)) + theme_bw() + scale_color_manual(values=c("red", "grey50"))
ggplot(corr_df, aes(x=Type, y=Pearson, color=Type)) + geom_violin() + theme_bw() + scale_color_manual(values=c("red", "grey50"))

# Limit to significantly correlated genes and make the same plots
lr_sig_corr <- subset(lr_neighbors_corr, p_val <0.05)
non_lr_sig_corr <- subset(non_lr_neighbors_corr, p_val<0.05)
wilcox.test(lr_sig_corr$Pearson, non_lr_sig_corr$Pearson)
corr_df <- subset(corr_df, P.Value<0.05)
ggplot(corr_df, aes(x=Type, y=Pearson, color=Type)) + geom_boxplot() + theme_bw() + scale_color_manual(values=c("red", "grey50"))
ggplot(corr_df, aes(x=Pearson)) + geom_density(aes(color=Type)) + theme_bw() + scale_color_manual(values=c("red", "grey50"))
ggplot(corr_df, aes(x=Pearson)) + stat_ecdf(aes(color=Type)) + theme_bw() + scale_color_manual(values=c("red", "grey50"))
ggplot(corr_df, aes(x=Type, y=Pearson, color=Type)) + geom_violin() + theme_bw() + scale_color_manual(values=c("red", "grey50"))
