from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


def create_report(
    filename,
    age,
    grade,
    risk_score,
    risk_group,
    surv1,
    surv3,
    surv5
):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "GBM Digital Twin v1.5 Clinical Report",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "<b>Patient Information</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"Age: {age}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Grade: {grade}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "<b>Risk Assessment</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"Risk Score: {risk_score:.4f}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Risk Group: {risk_group}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "<b>Survival Prediction</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"1-Year Survival: {surv1:.2f}%",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"3-Year Survival: {surv3:.2f}%",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"5-Year Survival: {surv5:.2f}%",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "<b>Model Information</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            "Model: GBM Digital Twin v1.5",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            "External Validation C-index: 0.7471",
            styles["Normal"]
        )
    )

    doc.build(story)