library(ggplot2)

ca = commandArgs(trailing=T)
df.file = ca[1]

df = read.table(df.file, header=T, quote="\"")
