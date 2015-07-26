## Local Repeats

This repo contains code I have written to analyze hundreds of local repeats found in the human genome. Primarily, I am interested in understanding the role of local repeats in human lncRNAs.

**Summary of the main findings so far (Updated - 7/25/15):**

* In both the mouse and human genome, local repeats are significantly enriched in lncRNAs compared to mRNAs. There is only LR that is same in human and mouse.
* Local repeat rich lncRNAs (LR lncRNAs) are longer, have more isoforms, exons, tandem repeats and transposable elements compared to other lncRNAs.
* LR lncRNAs are similarly tissue and cell type specific, but more highly expressed and more highly correlated in expression to their neighbors compared to other lncRNAs and protein coding genes.
* LR lncRNAs are significantly more nuclear than other lncRNAs only in H1-hESC. In all other cell lines, they are as nuclear as other lncRNAs.
* Local repeats found in lncRNAs (LRs) are significantly enriched at TAD boundaries and there is weak evidence for their colacalization in 3D.
* There is a sharp increase in signal for chromatin marks - H3K4Me1, H3K4Me3 and H3K27Ac concurrently only in H1-hESC. For a few LRs, the ratio of H3K4Me1/H3K4Me3 is greater than 3 suggesting potential enhancer like roles.
* There is a sharp increase in conservation scores (phyloP) across LRs compared to the neighboring regions. 
* LR elncRNAs have more 3D contacts than other lncRNAs and protein coding genes
* LR elncRNAs are more correlated with their neighbors but have a similar expression and specificity profile as protein coding genes and other lncRNAs

**Future things to Do (Updated - 7/25/15):**

* Distribution of exonic LRs in lncRNA transcripts. Are there lncRNA transcripts with only exonic LRs?
* For each category have a pony and or named lncRNA
* Check LR lncRNA distribution in Sheq's fractionation data.
* What is the average distance form neighbor for LR vs non  LR?

A lot of the scripts written here are built on the following publicly available software:

* [Segemehl] (http://www.bioinf.uni-leipzig.de/Software/segemehl/)
* [TopHat] (https://ccb.jhu.edu/software/tophat/index.shtml)
* [Cufflinks] (https://github.com/cole-trapnell-lab/cufflinks)
* [MUMmer] (http://mummer.sourceforge.net/)
* [DeepTools] (https://github.com/fidelram/deepTools)
* [RepeatScout] (http://bix.ucsd.edu/repeatscout/)
* [Jellyfish] (https://github.com/gmarcais/Jellyfish)
* [RepeatMasker] (http://www.repeatmasker.org/)
* [HyperBrowser] (https://hyperbrowser.uio.no/hb/)
* [GNU Parallel] (https://www.gnu.org/software/parallel/)
* [BedTools] (https://github.com/arq5x/bedtools2)
* [The Meme Suite] (http://meme-suite.org/index.html)
