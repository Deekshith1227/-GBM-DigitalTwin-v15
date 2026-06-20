\# AUDIT UPDATE (Scientific Reconstruction – June 2026)



\## Purpose



This document records evidence recovered from historical project files and notebooks during the scientific audit of the GBM Digital Twin project.



\---



\## Updated Gene Selection Pipeline



Recovered evidence indicates that the original feature-selection workflow contained an intermediate candidate-gene filtering stage.



Pipeline:



15,030 genes



↓



Expression Filtering



↓



15,030 retained transcriptomic features



Evidence:

Recovered\_Filtered\_Genes.csv



↓



Univariate Cox Proportional Hazards Regression



↓



1,822 significant prognostic genes (p < 0.05)



Evidence:

GBM\_Cox\_Results\_Recovered.csv



↓



Candidate Gene Filtering



↓



28 candidate prognostic genes



Evidence:

GBM\_28\_Significant\_Genes.csv



Genes:



GJB2

TMEM171

OSMR

IGFBP6

CPPED1

SLC17A9

PODNL1

TNFSF14

VILL

ADAMTS14

CPQ

LOXL1

PLAUR

SLC43A3

NKX3-1

GPR157

CYGB

STC1

TIMP1

SCN9A

UPP1

CTSB

ETNK2

MICAL2

RPL39L

PCOLCE2

PKD2L1

SHISA6



↓



LASSO-Cox Regression



↓



10-Gene Prognostic Signature



Evidence:

GBM\_LASSO\_Coefficients.csv



Final Genes:



OSMR

TMEM171

GJB2

VILL

SHISA6

SCN9A

GPR157

RPL39L

PKD2L1

IGFBP6



↓



Risk Score Generation



↓



Random Survival Forest Training Dataset



Evidence:

RSF\_Training\_Data.csv



↓



Survival Prediction Engine



\---



\## Biological Validation Evidence



Recovered enrichment analyses indicate that the selected genes are associated with:



\### GO Biological Processes



\* IGF receptor signaling regulation

\* Apoptosis regulation

\* Proteolysis regulation

\* Actin remodeling

\* Sodium ion transport



\### KEGG Pathways



\* Cytokine-cytokine receptor interaction

\* NF-kB signaling

\* HIF-1 signaling

\* JAK-STAT signaling

\* PI3K-AKT signaling

\* Proteoglycans in cancer



\### Reactome Pathways



\* Collagen formation

\* Extracellular matrix organization

\* ECM degradation

\* IGF transport and uptake

\* IL-6 receptor signaling

\* TNF receptor signaling



\---



\## Scientific Notes



The project contains evidence for:



\* TCGA biomarker discovery

\* Univariate Cox screening

\* Candidate gene filtering

\* LASSO-Cox feature selection

\* Random Survival Forest training

\* CGGA validation

\* GO enrichment

\* KEGG enrichment

\* Reactome enrichment



Further investigation is required to identify the exact script and criteria used to reduce the significant Cox genes to the final 28-gene candidate panel.



