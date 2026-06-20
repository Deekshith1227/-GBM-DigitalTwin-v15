from clinical_loader import *
from gene_extractor import *

clinical_df = load_clinical_file(
    r"C:\Users\ROHITH\CGGA\CGGA.mRNAseq_693_clinical.20200506.txt"
)

clinical = get_clinical_profile(
    clinical_df,
    "CGGA_1002"
)

genes = extract_genes(
    r"C:\Users\ROHITH\CGGA\CGGA.mRNAseq_693.RSEM-genes.20200506.txt",
    "CGGA_1002"
)

profile = {}

profile.update(clinical)
profile.update(genes)

print(profile)