## Local Repeats

This repo contains code I have written to analyze hundreds of local repeats found in the human genome. Primarily, I am interested in understanding the role of local repeats in human lncRNAs.

**Summary of the main findings so far (Updated - 6/24/15):**

* In both the mouse and human genome, local repeats are significantly enriched in lncRNAs compared to mRNAs.
* Local repeat rich lncRNAs (LR lncRNAs) are longer, have more isoforms, exons, tandem repeats and transposable elements compared to other lncRNAs.
* LR lncRNAs are less tissue and cell type specific, more highly expressed and more highly correlated in expression to their neighbors compared to other lncRNAs.
* LR lncRNAs are significantly more nuclear than other lncRNAs only in H1-hESC. In all other cell lines, they are as nuclear as other lncRNAs.
* Local repeats found in lncRNAs (LRs) are significantly enriched at TAD boundaries and there is weak evidence for their colacalization in 3D.
* There is a sharp increase in signal for chromatin marks - H3K4Me1, H3K4Me3 and H3K27Ac concurrently only in H1-hESC.
* There is a sharp increase in conservation scores (phyloP) across LRs compared to the neighboring regions. 

**Future things to Do (Updated - 6/24/15):**

* ~~Make dot plot of mouse LRs versus human LRs. See if there are any similarities.~~
* Distribution of exonic LRs in lncRNA transcripts. Are there lncRNA transcripts with only exonic LRs?
* Get expression correlation of 5,000 ranodm pairs of neighboring mRNAs and compare that distribution to correlation of LR lncRNAs with their neighbor
* Control for expression level while computing specificity.
* ~~Plot ratio of H3K4Me1/H3K4Me3 across body of LRs and test potential eRNAs in various methods.~~


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
