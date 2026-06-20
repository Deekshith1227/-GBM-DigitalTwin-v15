from clinical_loader import *

clinical_df = load_clinical_file(
    r"C:\Users\ROHITH\CGGA\CGGA.mRNAseq_693_clinical.20200506.txt"
)

patient = get_clinical_profile(
    clinical_df,
    "CGGA_1002"
)

print(patient)