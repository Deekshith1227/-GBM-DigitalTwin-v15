\# Gene Selection Audit



Project:

Integrated Multi-Omics Digital Twin for Personalized Survival Prediction and Therapeutic Decision Support in Glioblastoma



\---



\## Initial Transcriptome



Source:

TCGA RNA-Seq



Initial Gene Count:

\~20,000 genes



\---



\## Expression Filtering



Input:

Raw TCGA transcriptome



Output:

15,030 genes



Evidence:

Recovered\_Filtered\_Genes.csv



Purpose:

Remove low-expression and non-informative genes.



\---



\## Univariate Cox Screening



Input:

15,030 genes



Method:

Univariate Cox proportional hazards regression



Output:

391 prognostic genes



Evidence:

GBM\_Univariate\_Cox.csv



Selection Criterion:

p < 0.05



\---



\## LASSO Feature Selection



Input:

391 prognostic genes



Method:

LASSO-Cox regression



Output:

10-gene signature



Evidence:

GBM\_LASSO\_Coefficients.csv



Final Genes:



1\. OSMR

2\. TMEM171

3\. GJB2

4\. VILL

5\. SHISA6

6\. SCN9A

7\. GPR157

8\. RPL39L

9\. PKD2L1

10\. IGFBP6



\---



\## Survival Model Development



Input:

Clinical + Molecular + Transcriptomic Features



Clinical Variables:

\- Age

\- Grade

\- IDH1 Mutation

\- MGMT Methylation



Transcriptomic Variables:

\- OSMR

\- TMEM171

\- GJB2

\- VILL

\- SHISA6

\- SCN9A

\- GPR157

\- RPL39L

\- PKD2L1

\- IGFBP6



Machine Learning Model:

Random Survival Forest (RSF)



\---



\## Validation



Training:

CGGA-693



External Validation:

CGGA-325



Metrics:

\- C-index

\- Time-dependent ROC

\- Kaplan-Meier

\- Log-rank test

