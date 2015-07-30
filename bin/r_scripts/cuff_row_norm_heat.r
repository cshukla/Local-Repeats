library(ggplot2)
library(reshape2)
library(scales)

ca = commandArgs(trailing=T)
df.file = ca[1]
output.pdf = ca[2]

df = read.table(df.file, header=T, quote="\"")
df = dcast(df, Gene ~ Sample, value.var="FPKM")
df = cbind(df$Gene, df[,-1]/rowMeans(df[,-1]))
df = melt(df)
colnames(df) = c("Gene", "Sample", "FPKM")

fpkm.matrix = acast(df, Gene ~ Sample, value.var="FPKM")

gene.dist = dist(fpkm.matrix)
gene.clust = hclust(gene.dist)
gene.order = rownames(fpkm.matrix)[gene.clust$order]

sample.dist = dist(t(fpkm.matrix))
sample.clust = hclust(sample.dist)
sample.order = colnames(fpkm.matrix)[sample.clust$order]

#pdf("/Users/chinmayshukla/Documents/hclust.pdf")
#plot(hclust(dist(t(fpkm.matrix)), "ave"))
#dev.off()

ggplot(df, aes(x=Sample, y=Gene, fill=FPKM)) +
    geom_tile() +
    scale_x_discrete("",limits=sample.order) +    
    scale_y_discrete(limits=gene.order) +
    scale_fill_gradient2("FPKM", midpoint=1.0, low="#ca0020", high="#0571b0", mid="white") +
    theme_bw() +
    theme(axis.text.x=element_text(angle=315, hjust=0, vjust=1), axis.ticks.y=element_blank(), axis.text.y=element_blank())

ggsave(output.pdf)
