import math

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from .donors import Donors
from .helpers import donor_dtype, tier_mapper

class TierAnalysis(Donors):
    '''
    A simplified process of calculating donor tier plots

    Args:
        path        path to the data files
                    default: '../../data/donor/'
        dtype       dtype provided to pandas for quicker data load
                    default: dtype provided by .helpers.donor_dtype
        file_yr     the starting year of file data
                    default: '08'
        fy          fiscal year used for analysis
                    default: 20
    '''

    def __init__(self, path='../../data/donor/', dtype=donor_dtype,
                 file_yr='08', fy=20):
        super().__init__(path, dtype, file_yr)
        self.fy = fy

        self.parse_campaign_fy()

        cols = ['summary_cust_id', 'fy', 'gift_plus_pledge']

        cur_mask = self.data.fy == self.fy
        py_mask = self.data.fy ==  (self.fy - 1)

        self.data = self.data.loc[cur_mask | py_mask][cols]
        self.data = self.data.groupby(['summary_cust_id','fy']).sum().reset_index()
        self.data.columns = ['customer_id','fy', 'transaction_amount']


    def do_tier_analysis(self, mapper=False):
        """This function will calculate the number of retained customers across a\
        given time frame and within provided ranges (ex. annual giving levels\
        between $10,000 and $50,000).

        Keyword arguments:
        df -- must contain at least three specific columns:
            1: customer_id
            2: transaction_amount
            3: fy
        tier -- results for a specific tier instead of across all tiers (default 'all')
        mapper -- dictionary to map donor levels against. Provided mapper used if False. (default False)
                  default: tier_mapper

        """
        df = self.data.copy()

        if not mapper:
            mapper = tier_mapper

        df = df[df.transaction_amount >= 1].reset_index(drop=True)

        # Categorize each donor at each fiscal year:
        donor_tier = []
        for amount in df.transaction_amount:
            donor_tier.append(
                [int(key) for key,val in mapper.items() if val[0] <= round(amount,2) <= val[1]][0]
            )

        df = df.join(pd.Series(donor_tier, name='donor_tier'))

        cur = df.loc[df.fy == self.fy][['customer_id', 'transaction_amount', 'donor_tier']]
        py = df.loc[df.fy == (self.fy - 1)][['customer_id', 'donor_tier']]

        py.columns = ['customer_id', 'py_donor_tier']


        ## GET TIER COUNTS
        combined = cur.merge(py, on='customer_id', how='left')
        combined['comparison'] = combined['donor_tier'] - combined['py_donor_tier']
        combined['classification'] = combined['comparison'].map(self.donor_classifier)

        self.tier_counts = combined.groupby(['donor_tier', 'classification']).agg({
            'customer_id': 'count'
        }).reset_index()

        self.tier_counts.columns = ['donor_tier', 'classification', 'count']

        ## GET TIER REVENUE
        self.tier_revenue = cur.groupby(['donor_tier']).agg({
            'transaction_amount': 'sum'
        }).reset_index()

        return print('Success: Updated self.tier_counts and self.tier_revenue')


    def donor_classifier(self, val):
        if math.isnan(val):
            return 'new'
        elif val > 0:
            return 'upgrade'
        elif val < 0:
            return 'downgrade'
        else:
            return 'retained'


    def plot_tier_counts(self):
        tier_counts_form = self.tier_counts.pivot(
            index='donor_tier', columns='classification', values='count'
        ).fillna(0)

        # Plot setup
        fig, ax = plt.subplots(figsize=(15,10))
        sns.set(style="ticks")

        # Create the plot
        tier_counts_form.plot(ax=ax, kind='bar', stacked=True)

        # titles
        ax.set_title("Donor Tier Funnel - Number of Donors - FY20", fontsize=30)

        # axes
        ax.tick_params(axis='both', labelsize=16)
        ax.set_xlabel('Donor Tier', fontsize=20)
        ax.set_ylabel('Number of Donors', fontsize=20)

        plt.xticks(rotation=0)

        # Show plot
        plt.show()


    def plot_tier_revenue(self):
        # Plot setup
        fig, ax = plt.subplots(figsize=(15,10))
        sns.set(style="ticks")

        # Create the plot
        ax = sns.barplot(x="donor_tier", y="transaction_amount", data=self.tier_revenue)

        # titles
        ax.set_title("Revenue Generated per Tier - FY20", fontsize=30)

        # axes
        ax.tick_params(axis='both', labelsize=16)
        ax.set_xlabel('Donor Tier', fontsize=20)
        ax.set_ylabel('Revenue Generated', fontsize=20)

        plt.xticks(rotation=0)

        # Show plot
        plt.show()
