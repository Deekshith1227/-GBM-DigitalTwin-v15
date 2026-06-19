\# MASTER PROJECT RECORD



\## Project Name



GBM Digital Twin v2.1



\## Full Project Title



Development and Validation of a Multi-Modal Glioblastoma Digital Twin Platform for Survival Prediction, Therapeutic Response Assessment, and Clinical Decision Support Using Clinical and Transcriptomic Biomarkers



\---



\# Project Vision



Develop an industry-grade digital twin platform capable of:



\* Survival prediction

\* Drug response prediction

\* Drug resistance prediction

\* Recurrence prediction

\* Explainable AI

\* Treatment simulation



for Glioblastoma patients using multi-modal clinical and transcriptomic data.



\---



\# Current Development Status



Version: GBM Digital Twin v2.1



Status:



Completed:



\* Survival prediction engine

\* Risk stratification

\* PDF report generation

\* Manual Entry

\* Clinical + RNA Upload

\* CSV Upload

\* Excel Upload

\* Patient Matrix Upload



Pending:



\* Drug Response Prediction

\* Drug Resistance Detection

\* Recurrence Prediction

\* Explainable AI

\* Treatment Simulator



\---



\# Datasets Used



\## TCGA



Status:

Exploration / Feature Discovery



Data Types:



\* Clinical

\* RNA-seq

\* Survival

\* Mutation



Notes:

Used during early project exploration and model development planning.



\---



\## CGGA-693



Status:

Training Cohort



Data Types:



\* Clinical

\* RNA-seq

\* Survival



\---



\## CGGA-325



Status:

External Validation Cohort



Data Types:



\* Clinical

\* RNA-seq

\* Survival



\---



\# Features Used In Current Model



Clinical Features:



\* Age

\* Grade

\* IDH Mutation Status

\* MGMT Promoter Methylation Status



Transcriptomic Features:



\* OSMR

\* TMEM171

\* GJB2

\* VILL

\* SHISA6

\* SCN9A

\* GPR157

\* RPL39L

\* PKD2L1

\* IGFBP6



Total Features:

14



\---



\# Models Investigated



1\. Cox Proportional Hazards

&#x20;  Status: Investigated



2\. Random Survival Forest

&#x20;  Status: Deployed



3\. XGBoost Survival

&#x20;  Status: Future Evaluation



4\. DeepSurv

&#x20;  Status: Future Evaluation



5\. DeepHit

&#x20;  Status: Future Evaluation



\---



\# Current Production Model



Model Type:

Random Survival Forest



Model File:

DigitalTwin\_v15\_Model.pkl



Framework:

scikit-survival



\---



\# Validation



Training Cohort:

CGGA-693



External Validation Cohort:

CGGA-325



Training C-index:

0.7331



External Validation C-index:

0.7471



\---



\# Application Components



Main App:

app\_v21.py



Gene Extractor:

gene\_extractor.py



Clinical Loader:

clinical\_loader.py



Patient Matrix Extractor:

patient\_matrix\_extractor.py



PDF Generator:

pdf\_report.py



Model:

DigitalTwin\_v15\_Model.pkl



\---



\# Roadmap



Phase 2



1\. Drug Response Prediction

2\. Drug Resistance Detection

3\. Recurrence Prediction

4\. Explainable AI

5\. Treatment Simulator



\---



\# Backup Policy



Before every major module:



1\. Backup

2\. Commit

3\. Push



Commands:



copy app\_v21.py backups<module>.py



git add .

git commit -m "<message>"

git push



\---



\# Research Standards To Be Followed



Feature Selection:



\* Differential Expression Analysis

\* Cox Regression

\* LASSO-Cox



Survival Models:



\* CoxPH

\* RSF

\* DeepSurv

\* DeepHit



Validation:



\* Cross Validation

\* External Validation

\* C-index

\* Time-dependent AUC

\* Integrated Brier Score

\* Calibration Curves



Explainability:



\* SHAP

\* Feature Importance Analysis



\---

\# Cohort Architecture



Discovery:

TCGA



Development:

CGGA-693



External Validation:

CGGA-325



Independent Validation:

REMBRANDT



Independent Validation:

GLASS (planned)

