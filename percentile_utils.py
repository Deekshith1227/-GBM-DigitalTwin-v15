TCGA_PERCENTILES = {

    "EGFR": {
        25: 44.104825,
        50: 172.250800,
        75: 779.402675
    },

    "PDGFRA": {
        25: 12.153650,
        50: 28.554900,
        75: 60.122800
    },

    "MET": {
        25: 1.606600,
        50: 4.967450,
        75: 13.324975
    },

    "MGMT": {
        25: 2.209025,
        50: 4.478450,
        75: 7.199825
    },

    "IDH1": {
        25: 64.260800,
        50: 90.471600,
        75: 124.827550
    }
}


def get_percentile_category(gene, value):

    p = TCGA_PERCENTILES[gene]

    if value < p[25]:
        return "<25th percentile"

    elif value < p[50]:
        return "25-50th percentile"

    elif value < p[75]:
        return "50-75th percentile"

    else:
        return ">75th percentile"