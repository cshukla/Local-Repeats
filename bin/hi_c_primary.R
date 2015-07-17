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

###################################################
## code chunk number 25: ChIPfiles (eval = FALSE)
###################################################
files = c("wgEncodeBroadChipSeqPeaksGm12878H3k27me3.broadPeak.gz", "wgEncodeBroadChipSeqPeaksGm12878H3k36me3.broadPeak.gz", "wgEncodeUwDnaseSeqHotspotsRep1Gm06990.broadPeak.gz", "wgEncodeUwDnaseSeqHotspotsRep2Gm06990.broadPeak.gz")


###################################################
## code chunk number 26: readtable (eval = FALSE)
###################################################
inputDir = "~/Downloads"
outputDir = "~/Downloads"
cs = vector(mode="list", length=length(files))
for(i in seq(along=files)) {
   cat("Reading file", i, "\n")
   tab = read.table(gzfile(file.path(inputDir, files[i])),   header=FALSE, sep="\t", comment.char = "",   stringsAsFactors=FALSE)
   colnames(tab) <- c("chr", "start", "end", "name", "score", "strand", "signalValue", "pValue", "qValue")
   cs[[i]] = subset(tab, chr=="chr14")
}
 
H3K27me3.df = cs[[1]]
H3K36me3.df = cs[[2]]
DNAse1.df = cs[[3]]
DNAse2.df = cs[[4]]
 
save(list=c("H3K27me3.df", "H3K36me3.df", "DNAse1.df", "DNAse2.df"), file=file.path(outputDir, "ChipSeqData.RData"))


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

###################################################
### code chunk number 17: readChipseq
###################################################
createRleVector = function(tab){
  RleVec = Rle(0, max(tab$end))
  for(i in 1:nrow(tab)){
    RleVec = RleVec + 
      Rle(values  = c(0,              tab$signalValue[i],         0),
          lengths = c(tab$start[i]-1,
                    tab$end[i]-tab$start[i]+1,  
                    length(RleVec)-tab$end[i]))
  }
  RleVec
}


###################################################
### code chunk number 18: read
###################################################
data("ChipSeqData")
H3K27me3 = createRleVector(H3K27me3.df)
H3K36me3 = createRleVector(H3K36me3.df)
DNAse1   = createRleVector(DNAse1.df)
DNAse2   = createRleVector(DNAse2.df)


###################################################
### code chunk number 19: combinednase
###################################################
length(DNAse1)
length(DNAse2)
DNAse = DNAse1 + DNAse2[seq(along=DNAse1)]


###################################################
### code chunk number 20: plotRle
###################################################
plotRle = function(RleVector, ...){
  plot(end(RleVector), runValue(RleVector)+1, type="h", log="y",
  xlim = c(1.5e+7, 107000000), xlab="", ylab=deparse(substitute(RleVector)),
  ...)
}



###################################################
### code chunk number 21: figrle
###################################################
par(mfrow=c(4,1), mai=c(0.5,0.7,0.1,0.1))
plotRle(pc1Vec)
plotRle(H3K27me3)
plotRle(H3K36me3)
plotRle(DNAse1)


###################################################
### code chunk number 22: correlation
###################################################
c(length(H3K27me3),
  length(H3K36me3),
  length(DNAse),
  length(pc1Vec))

x = seq(along=H3K36me3)

cor(H3K27me3[x], pc1Vec[x])
cor(H3K36me3, pc1Vec[x])
cor(DNAse[x], pc1Vec[x])


