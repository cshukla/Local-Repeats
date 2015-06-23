# Load dependencies
library(ggplot2)
library(reshape2)
library(stringr)
library(dplyr)
library(distr)
library(mgcv) # for gam fitting
library(cummeRbund)

# Knitr setup
library(knitr)
opts_chunk$set(comment=NA, fig.width=10, fig.height=10,warning=FALSE,message=FALSE)

# Variables
fpkmCutoff<-log10(3)

#####################################################################################################
# Helper functions (most derived directly from cummeRbund with a few relevent modifications)        #
#####################################################################################################


JSdist<-function(mat,...){
  res<-matrix(0,ncol=dim(mat)[2],nrow=dim(mat)[2])

#   col_js <- matrix(0,ncol=dim(mat)[2],nrow=1)
#   for(i in 1:dim(mat)[2]){
#       col_js[,i] <- shannon.entropy(mat[,i])
#   }
    col_js<-apply(mat,MARGIN=2,shannon.entropy)
    #print(col_js)
    colnames(res)<-colnames(mat)
    rownames(res)<-colnames(mat)
    for(i in 1:dim(mat)[2]){
        for(j in i:dim(mat)[2]){
            a<-mat[,i]
            b<-mat[,j]
            JSdiv<-shannon.entropy((a+b)/2)-(col_js[i]+col_js[j])*0.5
            res[i,j] = sqrt(JSdiv)
            res[j,i] = sqrt(JSdiv)
        }
    }
    res<-as.dist(res,...)
    attr(res,"method")<-"JSdist"
    res
}


JSdistVec<-function(p,q){
  JSdiv<-shannon.entropy((p+q)/2)-(shannon.entropy(p)+shannon.entropy(q))*0.5
    JSdist<-sqrt(JSdiv)
    JSdist
}


makeprobsvec<-function(p){
  phat<-p/sum(p)
    phat[is.na(phat)] = 0
    phat
}

shannon.entropy <- function(p) {
    if (min(p) < 0 || sum(p) <=0)
        return(Inf)
    p.norm<-p[p>0]/sum(p)
    -sum( log2(p.norm)*p.norm)
}

maxSpecificity<-function(p){
  probs<-makeprobsvec(p)
  specs<-c()
  for(i in 1:length(probs)){
    q<-rep(0,length(probs))
    q[i]<-1
    specs<-c(specs,1-JSdistVec(probs,q))
  }
  return (max(specs))
}

minJSDist<-function(p){
  probs<-makeprobsvec(p)
  specs<-c()
  for(i in 1:length(p)){
    q<-rep(0,length(p))
    q[i]<-1
    specs<-c(specs,JSdistVec(p,q))
  }
  return (min(specs))
}

# Input the Cuffnorm output directory and get FPKM of genes across conditions
cuff<-readCufflinks(dir='/Users/chinmayshukla/Documents/Research/local_repeats/results/5-23-15/cuffnorm_tissue_quantification')
sigGenes.melt<-fpkm(genes(cuff))
sigGenes.melt$fpkm<-log10(sigGenes.melt$fpkm+1)

# Input the mapping between gene_id and gene_type
gene_id_type_df<-read.table(file='/Users/chinmayshukla/Documents/Research/local_repeats/results/5-22-15/gene_types.txt', header=T, sep="\t", quote="")

# Add gene type feature to the sigGenes.melt data frame
sigGenes.melt$gene_type = gene_id_type_df[match(sigGenes.melt$gene_id, gene_id_type_df$gene_id),"gene_type"]

# Sanity check
head(sigGenes.melt)
#table(sigGenes.melt$gene_type)

# Find max fpkm and max specificity for each gene across tissues
geneSummary<-sigGenes.melt %.%
  group_by(gene_id,gene_type) %.%
  summarize(maxFPKM=max(fpkm),maxSpec=maxSpecificity(fpkm),minJSDist=minJSDist(fpkm))

geneSummary<-subset(geneSummary,!is.na(maxSpec))

# Sanity check
head(geneSummary)

# CDF to compare specificities of different gene type's
p <- ggplot(geneSummary)
p <- p + stat_ecdf(aes(x=maxSpec,color=gene_type)) + 
  theme_bw() + 
  #scale_color_manual(values=c("red","grey5")) + 
  #scale_x_continuous(limits=c(0,1.0)) +
  coord_equal(1)

p
pdf("initial_spec.pdf",width=10,height=10)
p
dev.off()

p<-ggplot(geneSummary)
p<- p + geom_density(aes(x=maxFPKM,color=gene_type)) + 
  theme_bw() + 
  #scale_color_manual(values=c("red","black")) + 
  coord_equal(2)

p
pdf("cell_type_expression_dist.pdf",width=10,height=10)
p
dev.off()
