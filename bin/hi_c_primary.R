##################################################
## This script plots the raw interactions as well
## as the normalized interactions for a given 
## chromosome and Hi-C experiment. Please set the
## chromosome name, input dir and output dir each
## time (I will fix it soon!)
##################################################

##################################################
## Get Data
##################################################

library(KernSmooth)
library(IRanges)
sampleAnnotation = data.frame(file = c("GSM455133_30E0LAAXX.1.maq.hic.summary.binned.txt.gz", "GSM455134_30E0LAAXX.2.maq.hic.summary.binned.txt.gz", "GSM455135_30U85AAXX.2.maq.hic.summary.binned.txt.gz", "GSM455136_30U85AAXX.3.maq.hic.summary.binned.txt.gz", "GSM455137_30305AAXX.1.maq.hic.summary.binned.txt.gz", "GSM455138_30305AAXX.2.maq.hic.summary.binned.txt.gz"), experiment = c(1, 1, 2, 2, 3, 3), lane = c(1,2,1,2,1,2), restrictionenzyme = c("HindIII", "HindIII", "HindIII", "HindIII", "NcoI", "NcoI"), stringsAsFactors = FALSE)

inputDir = "~/Downloads"
outputDir = "~/Downloads"
df = vector(mode="list", length=nrow(sampleAnnotation))
for(i in seq(along=df)) {
  cat("Reading file", i, "\n")
  r = read.table(gzfile(file.path(inputDir, sampleAnnotation$file[i])), 
           header=FALSE, sep="\t", comment.char = "", stringsAsFactors=FALSE)
  colnames(r) = c("read name",
     "chromosome1", "position1", "strand1", "restrictionfragment1",
     "chromosome2", "position2", "strand2", "restrictionfragment2")
  ## filter chromosome X
  df[[i]] = subset(r, (chromosome1==23) & (chromosome2==23))
}
HiC_GM_chrX = do.call(rbind, df)
save(HiC_GM_chrX,
     file=file.path(outputDir, "HiC_GM_chrX.RData"))

head(HiC_GM_chrX)
pos = with(HiC_GM_chrX, cbind(position1, position2))

##################################################
## Print Scatter Plot
##################################################
pdf("~/Downloads/contact_map_chr14_erez_2009.pdf",width=1024,height=1024)
plot(pos, pch='.', col="#77777777")
dev.off()

###################################################
### Smooth interaction matrix M
###################################################
chrlen = max(pos)
gridsize = ceiling(chrlen/2e5)
bandwidth = 3e5
den = bkde2D( pos, bandwidth=c(1,1)*bandwidth, gridsize=c(1,1)*gridsize)


###################################################
### Symmetrize smoothened matrix M
###################################################
den$fhat <- den$fhat + t(den$fhat)


###################################################
### Plot symmetrized and smoothened matrix M
###################################################
with(den, image(x=x1, y=x2, z=fhat^0.3, 
      col=colorRampPalette(c("white","blue"))(256), useRaster=TRUE))


###################################################
### Normalize
###################################################
m = matrix(0, nrow=gridsize, ncol=gridsize)
for(i in 1:(gridsize-1)) {
  band = (row(m)==col(m)+i)
  m[band] = mean(den$fhat[band])
}
m = m + t(m)
diag(m) = mean(diag(den$fhat))


###################################################
### code chunk number 8: figmatm
###################################################
image(x=den$x1, y=den$x2, z=m^0.3, 
      col=colorRampPalette(c("white","blue"))(256), useRaster=TRUE)


###################################################
### code chunk number 9: figaverage
###################################################
genomicDistance = den$x1 - min(den$x1)
averageInteractions = m[1,]
plot(genomicDistance, sqrt(averageInteractions), type ="l")


###################################################
### Normalize
###################################################
fhatNorm <- den$fhat/m


###################################################
### code chunk number 11: figmatrix2
###################################################
image(x=den$x1, y=den$x2, z=fhatNorm, 
      col=colorRampPalette(c("white","blue"))(256), useRaster=TRUE)


###################################################
### code chunk number 12: cormatrix
###################################################
cm <- cor(fhatNorm)


###################################################
### code chunk number 13: figmatrix3
###################################################
image(x=den$x1, y=den$x2, z=cm, 
     zlim=c(-1,1),
     col=colorRampPalette(c("red", "white","blue"))(256), useRaster=TRUE)


###################################################
### code chunk number 14: cormatrix
###################################################
princp = princomp(cm)


###################################################
### code chunk number 15: figprcomp1
###################################################
plot(den$x1, princp$loadings[,1], type="l")


###################################################
### code chunk number 16: pc1Vec
###################################################
pc1Vec = Rle(values  = princp$loadings[,1],
             lengths = c(den$x1[1], diff(den$x1)))
pc2Vec = Rle(values  = princp$loadings[,2],
             lengths = c(den$x1[1], diff(den$x1)))


