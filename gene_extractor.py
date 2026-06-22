import pandas as pd


SIGNATURE_GENES = [

    # Survival Signature
    "OSMR",
    "TMEM171",
    "GJB2",
    "VILL",
    "SHISA6",
    "SCN9A",
    "GPR157",
    "RPL39L",
    "PKD2L1",
    "IGFBP6",

    # Drug Response Biomarkers
    "EGFR",
    "PDGFRA",
    "MET",
    "MGMT",
    "IDH1"
]

def extract_genes(file_path, patient_id=None):

    # TXT RNA-seq matrix
    if file_path.endswith(".txt"):

        df = pd.read_table(file_path)

        if patient_id is None:
            raise ValueError(
                "patient_id required for RNA-seq matrix"
            )

        profile = {}

        for gene in SIGNATURE_GENES:

            value = df.loc[
                df["Gene_Name"] == gene,
                patient_id
            ].values

            if len(value) > 0:
                profile[gene] = float(value[0])

            else:
                profile[gene] = None

        return profile

    # CSV gene-expression file
    elif file_path.endswith(".csv"):

        df = pd.read_csv(file_path)

        gene_dict = dict(
            zip(
                df["Gene"],
                df["Expression"]
            )
        )

        profile = {}

        for gene in SIGNATURE_GENES:
            profile[gene] = gene_dict.get(
                gene,
                None
            )

        return profile

    # Excel gene-expression file
    elif (
        file_path.endswith(".xlsx")
        or
        file_path.endswith(".xls")
    ):

        df = pd.read_excel(file_path)

        gene_dict = dict(
            zip(
                df["Gene"],
                df["Expression"]
            )
        )

        profile = {}

        for gene in SIGNATURE_GENES:
            profile[gene] = gene_dict.get(
                gene,
                None
            )

        return profile

    else:

        raise ValueError(
            "Unsupported file format"
        )

def extract_full_transcriptome(
    file_path,
    patient_id
):

    import pandas as pd

    df = pd.read_table(file_path)

    expr = pd.Series(
        df[patient_id].values,
        index=df["Gene_Name"]
    )

    return expr