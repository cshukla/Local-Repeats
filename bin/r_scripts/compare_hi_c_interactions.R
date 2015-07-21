library(ggplot2)

ca = commandArgs(trailing=T)
df.file = ca[1]
output.pre = ca[2]

df = read.table(df.file, header=F, quote="\"")
colnames(df) = c("Average.Interactions", "Label")
ggplot(df, aes(x=Average.Interactions, color=Label)) + 
	geom_density() + 
	theme_bw()

ggsave(paste0(output.pre, "_density.pdf"))

ggplot(df, aes(x=Average.Interactions, color=Label)) +
	stat_ecdf() +
	theme_bw()

ggsave(paste0(output.pre, "_cdf.pdf"))

ggplot(df, aes(x=Label, y=Average.Interactions, color=Label)) +
	geom_boxplot() +
	theme_bw()

ggsave(paste0(output.pre, "_boxplot.pdf"))

ggplot(df, aes(x=Label, y=Average.Interactions, color=Label)) +
	geom_violin() +
	theme_bw()

ggsave(paste0(output.pre, "_violin.pdf"))