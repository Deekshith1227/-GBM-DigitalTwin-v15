EGFR_HIGH = 779.40
PDGFRA_HIGH = 60.12
MET_HIGH = 13.32


def recommend_drugs(profile, risk_group):

    recommendations = []

    if profile.get("EGFR", 0) >= EGFR_HIGH:

        recommendations.append(
            ("Afatinib",
             "High EGFR expression")
        )

        recommendations.append(
            ("Gefitinib",
             "High EGFR expression")
        )

    if profile.get("PDGFRA", 0) >= PDGFRA_HIGH:

        recommendations.append(
            ("Axitinib",
             "High PDGFRA expression")
        )

    if profile.get("MET", 0) >= MET_HIGH:

        recommendations.append(
            ("Crizotinib",
             "High MET expression")
        )

    if risk_group == "HIGH RISK":

        recommendations.append(
            ("Temsirolimus",
             "High-risk molecular profile")
        )

    return recommendations