import math
import pandas as pd
from .helpers import donor_tier_mapper
from . import filter, aggregator
from .plot import PlotFactory

class TierAnalysis:
    def __init__(self):
        self.plot = PlotFactory('tier_analysis').plotter()
        self.tier_counts = None
        self.tier_revenue = None

    def execute(self, data, fy, mapper=None):
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
                  default: donor_tier_mapper

        """
        data = data.copy()
        if mapper is None:
            mapper = donor_tier_mapper

        data = filter.filter_fys(data, [fy-1, fy])
        filtered = filter.filter_individual_giving(data)
        aggregate = aggregator.basic_aggregator(filtered, ['summary_cust_id','fy'],
            'gift_plus_pledge', 'sum', ['customer_id','fy', 'transaction_amount'])

        paid_only = filter.filter_paid_only(aggregate, 'transaction_amount')
        donor_tier = self.categorize_donors(paid_only, mapper)
        paid_donor_merge = paid_only.join(pd.Series(donor_tier, name='donor_tier'))

        cur, py, combined = self.cur_py_combo_breakout(paid_donor_merge, fy)

        combined['comparison'] = combined['donor_tier'] - combined['py_donor_tier']
        combined['classification'] = combined['comparison'].map(self.donor_classifier)

        self.tier_counts = aggregator.basic_aggregator(combined, ['donor_tier', 'classification'],
            'customer_id', 'count', ['donor_tier', 'classification', 'count'])

        self.tier_revenue = aggregator.basic_aggregator(cur, ['donor_tier'],
            'transaction_amount', 'sum')

        agg_tiers = aggregator.basic_aggregator(self.tier_counts, ['classification'],
            'count', 'sum')

        py_data = self.get_py_data(cur, py)

        agg = agg_tiers.append(py_data).reset_index(drop=True)

        self.plot.plot_tier_counts(self.tier_counts)
        self.plot.plot_tier_revenue(self.tier_revenue)
        return agg


    @staticmethod
    def cur_py_combo_breakout(data, fy):
        cur = data.loc[data.fy == fy][['customer_id', 'transaction_amount', 'donor_tier']]

        py = data.loc[data.fy == (fy - 1)][['customer_id', 'donor_tier']]
        py.columns = ['customer_id', 'py_donor_tier']

        combo = cur.merge(py, on='customer_id', how='left')

        return cur, py, combo


    @staticmethod
    def categorize_donors(data, mapper):
        donor_tier = []

        for amount in data['transaction_amount']:
            donor_tier.append(
                [int(key) for key,val in mapper.items() if val[0] <= round(amount,2) <= val[1]][0]
            )

        return donor_tier


    @staticmethod
    def donor_classifier(val):
        if math.isnan(val):
            return 'new'
        elif val > 0:
            return 'upgrade'
        elif val < 0:
            return 'downgrade'
        else:
            return 'retained'


    @staticmethod
    def get_py_data(current_donors, py_donors):
        lost_to_date = len(py_donors) - len(current_donors)
        py_data = pd.DataFrame({
            'classification': [
                'lost to date',
                'total retained to date',
                'prior year donors'
            ],
            'count': [
                lost_to_date,
                len(py_donors) - lost_to_date,
                len(py_donors)
            ]
        })

        return py_data
