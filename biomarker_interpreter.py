from zscore_utils import (
    calculate_zscore,
    interpret_zscore
)

from percentile_utils import (
    get_percentile_category
)


def interpret_biomarker(
    gene,
    value
):

    z = calculate_zscore(
        gene,
        value
    )

    return {
        "Gene": gene,
        "Value": round(value, 3),
        "ZScore": round(z, 3),
        "Status": interpret_zscore(z),
        "Percentile": get_percentile_category(
            gene,
            value
        )
    }