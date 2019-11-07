import math
import pandas as pd
import numpy as np
from .helpers import donor_tier_mapper
from . import filter, aggregator, transform
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


class PreConcertSegmentation:
    '''
    concert_dates --
    '''

    def __init__(self, ticket_data, donor_data, fy, concert_dates):
        self.raw_tdata = ticket_data.copy()
        self.raw_ddata = donor_data.copy()
        self.fy = fy
        self.concert_dates = concert_dates

    def execute(self):
        tdata = filter.filter_paid_only(self.raw_tdata, 'paid_amt')
        subs = self.get_current_subs()
        donor_hist = self.donor_hist()

        segment_data = self.prep_segmentation_data(tdata)
        min_t, low_t, avg_t, high_t, max_t = self.segmentation_breakouts(segment_data, 'transactions')
        min_p, low_p, avg_p, high_p, max_p = self.segmentation_breakouts(segment_data, 'avg_paid')

        segment_data = self.get_segmentation(segment_data, self.segmentation_algo,
                              low_t, avg_t, high_t, low_p, avg_p, high_p)

        segment_data = segment_data.merge(subs, on='summary_cust_id', how='left')
        segment_data = segment_data.merge(donor_hist, on='summary_cust_id', how='left')
        segment_data = segment_data.fillna(0)
        segment_data = segment_data[['summary_cust_id', 'segment', 'subs', 'donor_5yr_history']]

        concerts = (self.get_concert_by_date(date) for date in self.concert_dates)
        solicitor = self.get_solicitor_info()

        for concert, date in zip(concerts, self.concert_dates):
            customers = pd.DataFrame(concert['summary_cust_id'].drop_duplicates()).reset_index(drop=True)
            concert_info = customers.merge(segment_data, on='summary_cust_id', how='left')
            seat_finder = self.setup_seating(concert)
            seat_finder = seat_finder.merge(solicitor, on='summary_cust_id', how='left')

            yield concert_info, seat_finder, date


    @staticmethod
    def prep_segmentation_data(data):
        data = data.copy()
        data = data.groupby(['summary_cust_id']).agg({
            'perf_dt': 'nunique',
            'paid_amt': lambda x: sum(x) / len(x)
        }).reset_index()

        data.columns = ['summary_cust_id', 'transactions', 'avg_paid']
        return data

    @staticmethod
    def segmentation_breakouts(data, column):
        highest = max(data[column])
        lowest = min(data[column])
        avg = np.mean(data[column])
        high = (highest + avg) / 2
        low = (lowest + avg) / 2
        return  lowest, low, avg, high, highest


    @staticmethod
    def segmentation_algo(transactions, avg_paid_amt, low_t, avg_t, high_t, low_p, avg_p, high_p):
        if transactions > high_t and avg_paid_amt > high_p:
            return 'group 1'
        elif (transactions > high_t and avg_paid_amt >= avg_p) |\
             (transactions >= avg_t and avg_paid_amt > high_p):
            return 'group 2'
        elif (transactions > low_t and avg_paid_amt > high_p) |\
             (transactions >= avg_t and avg_paid_amt >= avg_p) |\
             (transactions > high_t and avg_paid_amt > low_p):
            return 'group 3'
        else:
            return 'group 4'


    @staticmethod
    def get_segmentation(data, algo, low_t, avg_t, high_t, low_p, avg_p, high_p):
        data = data.copy()
        group_list = [
            algo(freq, amt, low_t, avg_t, high_t, low_p, avg_p, high_p)
            for freq, amt in zip(data['transactions'], data['avg_paid'])
        ]
        data['segment'] = group_list
        return data


    def get_current_subs(self):
        data = self.raw_tdata.copy()
        data = filter.filter_fys(data=data, fys=[self.fy])
        data = filter.filter_subs(data)
        current_subs = data['summary_cust_id'].drop_duplicates()
        current_subs = pd.DataFrame(current_subs).reset_index(drop=True)
        current_subs['subs'] = 'subscriber'
        return current_subs

    def donor_hist(self):
        data = self.raw_ddata.copy()
        data = filter.filter_fys(data=data, fys=[fy for fy in range(self.fy-4, self.fy+1)])
        data = data.groupby('summary_cust_id').agg({'gift_plus_pledge': 'sum'}).reset_index()
        data.columns = ['summary_cust_id', 'donor_5yr_history']
        return data

    def get_concert_by_date(self, date):
        data = self.raw_tdata.copy()
        data['perf_dt_date'] = data['perf_dt'].map(lambda x: x.strftime('%Y-%m-%d'))
        mask = data['perf_dt_date'] == pd.to_datetime(date).strftime('%Y-%m-%d')
        data = data.loc[mask]
        return data

    @staticmethod
    def setup_seating(concert_data):
        data = concert_data.copy()
        data['seating'] = data['section'] + ' ' + data['row'] + ' ' + data['seat'].map(str)
        data = data[['summary_cust_id', 'summary_cust_name', 'seating']]
        return data


    def get_solicitor_info(self):
        data = self.raw_ddata.copy()
        data = data.sort_values('trn_dt', ascending=False)[['summary_cust_id', 'ps_sol']].reset_index(drop=True)

        d = {}
        for sid, pssol in zip(data['summary_cust_id'], data['ps_sol']):
            if sid in d.keys():
                pass
            else:
                d.update({sid: pssol})

        solicitor = pd.DataFrame({'summary_cust_id': list(d.keys()), 'solicitor': list(d.values())})
        return solicitor

class DonorWeekly:
    def __init__(self):
        self.plot = PlotFactory('donor_weekly').plotter

    def execute(self, data):
        data['week_dt'] = data['cont_dt'].map(transform.donor_convert_cont_dt_to_monday)

        grouped = data.groupby(['campaign', 'week_dt']).agg({
                    'gift_plus_pledge': 'sum'
                  }).reset_index()

        pivoted = grouped.pivot(index='week_dt', columns='campaign', values='gift_plus_pledge').fillna(0)

        cumulative = pivoted.cumsum()

        self.plot.plot_all_campaigns(cumulative)
