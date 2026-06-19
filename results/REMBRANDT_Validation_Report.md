\# REMBRANDT Independent Validation



\## Dataset



Dataset: REMBRANDT



Total Samples Downloaded: 580



Patients With Survival Information: 397



Genes Available From Signature: 9 / 10



Missing Gene:



\* SHISA6



\---



\## Risk Stratification



Risk scores were generated using the previously trained Random Survival Forest model.



Median Risk Score:

2.439



High-Risk Patients:

199



Low-Risk Patients:

198



\---



\## Kaplan-Meier Survival Analysis



A Kaplan-Meier analysis was performed using the median risk score as the cutoff.



Result:



The high-risk group demonstrated significantly poorer survival compared to the low-risk group.



Evidence:



REMBRANDT\_KM\_Curve.png



\---



\## Log-Rank Test



Test Statistic:

76.26



P-value:

2.49 × 10^-18



Interpretation:



The survival difference between the high-risk and low-risk groups is highly significant.



Evidence:



REMBRANDT\_LogRank.txt



\---



\## Cox Proportional Hazards Model



Hazard Ratio (HR):

23.98



95% Confidence Interval:

12.66 – 45.43



P-value:

< 0.005



Interpretation:



Patients with higher risk scores have substantially increased mortality risk.



Evidence:



REMBRANDT\_CoxPH.csv



\---



\## Concordance Index



C-index:

0.672



Interpretation:



The model demonstrates good prognostic discrimination in an independent cohort.



Evidence:



REMBRANDT\_Cindex.txt



\---



\## Scientific Conclusion



The GBM Digital Twin Survival Engine successfully generalized to the independent REMBRANDT cohort.



Key Findings:



\* Significant Kaplan-Meier separation

\* Highly significant Log-Rank test

\* Strong Cox hazard ratio

\* Acceptable C-index

\* External reproducibility demonstrated



This supports the robustness of the survival signature beyond the original training datasets.



Status:



Independent Validation Completed



Date:

19 June 2026



