library(ggplot2)
library(plyr)

ca = commandArgs(trailing=T)
df.file = ca[1]

df = read.table(df.file, header=T, quote="\"")
ggplot(df, aes(x=length, color=class)) + geom_density() + theme_bw()