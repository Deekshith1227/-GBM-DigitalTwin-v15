from gene_extractor import extract_genes

genes = extract_genes(
    r"C:\Users\ROHITH\CGGA\CGGA.mRNAseq_693.RSEM-genes.20200506.txt",
    "CGGA_1002"
)

print(genes)