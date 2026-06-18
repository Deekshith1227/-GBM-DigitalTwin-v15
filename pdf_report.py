from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from datetime import datetime


def create_report(
    filename,
    patient_id,
    patient_name,
    age,
    grade,
    risk_score,
    risk_group,
    surv1,
    surv3,
    surv5
):

    doc = SimpleDocTemplate(
        filename
    )

    styles = getSampleStyleSheet()

    story = []

    # ---------------------------------
    # TITLE
    # ---------------------------------

    story.append(
        Paragraph(
            "GBM Digital Twin v2.1 Clinical Report",
            styles["Title"]
        )
    )

    story.append(
        Spacer(1, 10)
    )

    story.append(
        Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 20)
    )

    # ---------------------------------
    # PATIENT INFORMATION
    # ---------------------------------

    story.append(
        Paragraph(
            "<b>Patient Information</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"Patient ID: {patient_id}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Patient Name: {patient_name}",
            styles["Normal"]
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

    story.append(
        Spacer(1, 10)
    )

    # ---------------------------------
    # RISK ASSESSMENT
    # ---------------------------------

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

    story.append(
        Paragraph(
            "Reference Median Risk: 2.7226",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 10)
    )

    # ---------------------------------
    # SURVIVAL PREDICTION
    # ---------------------------------

    story.append(
        Paragraph(
            "<b>Survival Prediction</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"1-Year Survival Probability: {surv1:.2f}%",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"3-Year Survival Probability: {surv3:.2f}%",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"5-Year Survival Probability: {surv5:.2f}%",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 10)
    )

    # ---------------------------------
    # INTERPRETATION
    # ---------------------------------

    story.append(
        Paragraph(
            "<b>Interpretation</b>",
            styles["Heading2"]
        )
    )

    if risk_group == "HIGH RISK":

        interpretation = (
            "The patient is classified as HIGH RISK "
            "relative to the training cohort and may "
            "have a less favorable predicted prognosis."
        )

    else:

        interpretation = (
            "The patient is classified as LOW RISK "
            "relative to the training cohort and may "
            "have a comparatively favorable predicted prognosis."
        )

    story.append(
        Paragraph(
            interpretation,
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 10)
    )

    # ---------------------------------
    # MODEL INFORMATION
    # ---------------------------------

    story.append(
        Paragraph(
            "<b>Model Information</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            "Model: GBM Digital Twin v2.1",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            "Training Cohort: CGGA-693",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            "External Validation Cohort: CGGA-325",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            "Training C-index: 0.7331",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            "External Validation C-index: 0.7471",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 10)
    )

    # ---------------------------------
    # DISCLAIMER
    # ---------------------------------

    story.append(
        Paragraph(
            "<b>Research Disclaimer</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            "This report is generated using the GBM Digital Twin v2.1 "
            "machine learning framework. Predictions are intended for "
            "research and educational use only and should not be used "
            "as the sole basis for clinical decision-making.",
            styles["Normal"]
        )
    )

    # ---------------------------------
    # BUILD PDF
    # ---------------------------------

    doc.build(
        story
    )