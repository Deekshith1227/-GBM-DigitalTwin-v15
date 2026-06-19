\# Bootstrap Validation Report



\## Objective



To evaluate the stability and robustness of the Random Survival Forest (RSF) model through repeated bootstrap resampling.



\## Method



\* Model: Random Survival Forest

\* Trees: 500

\* Bootstrap iterations: 100

\* Training cohort: 223 patients

\* Features: 10-gene prognostic signature



Genes:



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



\## Results



Mean C-index: 0.8087



Standard deviation: 0.0171



\## Interpretation



The RSF model demonstrated excellent predictive performance with a mean bootstrap concordance index above 0.80.



The low standard deviation indicates strong model stability and reproducibility across repeated resampling experiments.



These results support the robustness of the GBM Digital Twin Survival Engine and indicate that the model is not overly dependent on specific training samples.



\## Conclusion



The GBM Digital Twin Survival Engine achieved stable and reproducible performance during bootstrap validation and can be considered statistically robust for survival prediction.



