## Local Repeats

This repo contains code I have written to analyze hundreds of local repeats found in the human genome. Primarily, I am interested in understanding the role of local repeats in human lncRNAs.

This README file will be updated later to include a highlight of the main results and a list of future things to do.

**Summary of the main findings so far (Updated - 6/24/15):**

* In both the mouse and human genome, local repeats are significantly enriched in lncRNAs compared to mRNAs.
* Local repeat rich lncRNAs (LR lncRNAs) are longer, have more isoforms, exons, tandem repeats and transposable elements compared to other lncRNAs.
* LR lncRNAs are less tissue and cell type specific, more highly expressed and more highly correlated in expression to their neighbors compared to other lncRNAs.
* LR lncRNAs are significantly more nuclear than other lncRNAs only in H1-hESC. In all other cell lines, they are as nuclear as other lncRNAs.
* Local repeats found in lncRNAs (LRs) are significantly enriched at TAD boundaries and there is weak evidence for their colacalization in 3D.
* There is a sharp increase in signal for chromatin marks - H3K4Me1, H3K4Me3 and H3K27Ac concurrently only in H1-hESC.
* There is a sharp increase in conservation scores (phyloP) across LRs compared to the neighboring regions. 

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
