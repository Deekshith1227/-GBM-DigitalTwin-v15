import plotly.express as px
import numpy as np
print("SCATTER MODULE LOADED V2")

def create_response_resistance_scatter(treatment_df):

    plot_df = treatment_df.copy()

    print(plot_df.columns.tolist())
    print(plot_df.head())

    # Always positive sizes
    plot_df["Bubble_Size"] = (
        np.abs(plot_df["Final_Score"]) + 0.1
    ) * 50

    fig = px.scatter(
        plot_df,
        x="Response_Score",
        y="Resistance_Probability",
        color="Final_Score",
        size="Bubble_Size",
        hover_name="Drug",
        color_continuous_scale="RdYlGn",
        title="Drug Response vs Resistance Landscape"
    )

    fig.update_layout(
        height=650,
        template="plotly_white"
    )
    
    print("NEW SCATTER FUNCTION EXECUTED") 
    return fig