library(ggplot2)

ca = commandArgs(trailing=T)
df.file = ca[1]
output.pdf = ca[2]

df = read.table(df.file, header=T, quote="\"")

ggplot(df, aes(x=Feature, y=Organism, fill=TransMap)) +
    geom_tile() +
    theme_bw() +
    scale_fill_gradient("TransMap", low="white", high="#54278f") +
	theme(axis.ticks.y=element_blank(), axis.ticks.x=element_blank(), axis.text.x=element_blank(), legend.position="none")

ggsave(output.pdf)
