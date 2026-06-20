import pandas as pd

TCGA_STATS = {
    "EGFR": {
        "mean": 543.518637,
        "std": 809.141540
    },
    "PDGFRA": {
        "mean": 104.084702,
        "std": 291.598755
    },
    "MET": {
        "mean": 15.408065,
        "std": 52.324932
    },
    "MGMT": {
        "mean": 5.111095,
        "std": 3.436494
    },
    "IDH1": {
        "mean": 101.566073,
        "std": 51.495055
    }
}

def calculate_zscore(gene, value):

    mean = TCGA_STATS[gene]["mean"]
    std = TCGA_STATS[gene]["std"]

    return (value - mean) / std


def interpret_zscore(z):

    if z >= 2:
        return "Very High"

    elif z >= 1:
        return "High"

    elif z <= -2:
        return "Very Low"

    elif z <= -1:
        return "Low"

    else:
        return "Normal"