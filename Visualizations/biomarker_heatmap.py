import pandas as pd
import plotly.express as px


def create_biomarker_heatmap(
    profile
):

    genes = [
        "OSMR",
        "TMEM171",
        "GJB2",
        "VILL",
        "SHISA6",
        "SCN9A",
        "GPR157",
        "RPL39L",
        "PKD2L1",
        "IGFBP6"
    ]

    values = [
        profile[g]
        for g in genes
    ]

    heatmap_df = pd.DataFrame(
        [values],
        columns=genes,
        index=["Patient"]
    )

    fig = px.imshow(
        heatmap_df,
        color_continuous_scale="RdBu_r",
        aspect="auto",
        text_auto=".2f"
    )

    fig.update_layout(
        title="Biomarker Expression Heatmap",
        height=350
    )

    return fig