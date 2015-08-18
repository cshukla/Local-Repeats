library(biomaRt)
library(sleuth)

base_dir <- "~/Downloads/cuffdiff2_data_kallisto_results"
sample_id <- dir(file.path(base_dir,"results"))
kal_dirs <- sapply(sample_id, function(id) file.path(base_dir, "results", id, "kallisto"))
s2c <- read.table(file.path(base_dir,"hiseq_info.txt"), header = TRUE, stringsAsFactors=FALSE)
s2c <- dplyr::select(s2c, sample = run_accession, condition)
t2g <- biomaRt::getBM(attributes = c("ensembl_transcript_id", "ensembl_gene_id",
    "external_gene_name"), mart = mart)
t2g <- dplyr::rename(t2g, target_id = ensembl_transcript_id,
  ens_gene = ensembl_gene_id, ext_gene = external_gene_name)
so <- sleuth_prep(kal_dirs, s2c, ~ condition, target_mapping = t2g)
so <- sleuth_fit(so)
so <- sleuth_test(so, which_beta = 'conditionscramble')
results_table <- sleuth_results(so, 'conditionscramble') 

