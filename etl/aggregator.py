def basic_aggregator(data, grp_by, col_to_agg, method, new_col_names=None):
    aggregated = data.groupby(grp_by).agg({
        col_to_agg: method
    }).reset_index()

    if new_col_names:
        aggregated.columns = new_col_names

    return aggregated
