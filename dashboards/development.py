from .. import TierAnalysis, Donors, Tickets

def dev_builder(fy, file_yr):
    '''FY is fiscal year of dashboard (ex. for fiscal year 20, fy=20)'''
    fys = [fy-1, fy]

    # Importing and transforming data from other classes
    tiers = TierAnalysis()
    donors = Donors(file_yr=file_yr)
    tix = Tickets(fys=fys)

    # Aggregate tiers for analysis
    df = tiers.aggregate_retention().reset_index(drop=True)
    df.set_index('classification', inplace=True)

    # Determine high capacity and activities
    high_cap = donors.high_cap_prospects(fys=fys)
    # Keep only high capacity ids in ticketing data
    high_cap_mask = tix.data.summary_cust_id.isin(high_cap)
    high_cap_tix = tix.data.loc[high_cap_mask].reset_index(drop=True)
    high_cap_activities = high_cap_tix[['perf_dt', 'customer_no']].drop_duplicates()

    # Build KPIs
    kpis = {
        'upgrade': f"{round(df.loc['upgrade']['count'] / df.loc['prior year donors']['count'] * 100, 2)}%",
        'downgrade': f"{round(df.loc['downgrade']['count'] / df.loc['prior year donors']['count'] * 100, 2)}%",
        'total retention': f"{round(df.loc['total retained to date']['count'] / df.loc['prior year donors']['count'] * 100, 2)}%",
        'high capacity prospects': len(high_cap),
        'avg activities by high cap prospects': len(high_cap_activities) / len(high_cap)
    }

    # Build tier plots
    tiers.plot_tier_revenue()
    tiers.plot_tier_counts()

    return kpis
