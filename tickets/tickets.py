from collections import namedtuple

import pandas as pd

from . import helpers


class Tickets:
    '''
    A simplified process of importing and transforming Pacific Symphony data.

    Args:
        fys             a list of integers representing fiscal years (ie. 2009 NOT 09)
        path            path to the data files
                        default: '../../data/ticket/'
        dtype           dtype provided to pandas for quicker data load
                        default: helpers.ticketing_dtype

    Methods:
        convert_dates   converts the dates for 'perf_dt' and 'order_dt' to
                        datetime objects.
        drop_bad_ids    removes all rows with 'summary_cust_id' matching
                        ids that should not be included. These come from the 
                        bad_ids list provided by 'helpers.bad_ids'
        drop_unsold     removes all rows that don't include a sale.
        remove_outliers excludes paid amounts <$5, >$500 (per ticket) by
                        default
    '''


    def __init__(self, fys, path='../../data/ticket/', dtype=helpers.ticketing_dtype):
        self.fys = fys
        self._path = path
        self._dtype = dtype

        _tmp_dfs = []
        for fy in fys:
            file = self._path + f'fy{str(fy)[2:]}_all.csv'
            df = pd.read_csv(file, skiprows=3, dtype=self._dtype)
            df['fy'] = fy - 2000
            _tmp_dfs.append(df)

        self.data = pd.concat(_tmp_dfs, ignore_index=True)


    def convert_dates(self):
        self.data['perf_dt'] = pd.to_datetime(self.data['perf_dt']).reset_index(drop=True)
        self.data['order_dt'] = pd.to_datetime(self.data['order_dt']).reset_index(drop=True)
        return self


    def drop_bad_ids(self):
        self.data = self.data[~self.data['summary_cust_id'].isin(helpers.bad_ids)].reset_index(drop=True)
        return self


    def drop_unsold(self):
        self.data = self.data[pd.notnull(self.data['summary_cust_id'])].reset_index(drop=True)
        return self


    def total_subs(self, fy=None):
        '''Simplified analysis of subscribers (Subscriptions and Flex)

        args:
        fy          (optional) Fiscal Year under analysis

        returns:
        SubData     a named tuple consisting of two variables:
            subscriber_list             consisting of sub_list
            number_of_subscribers       consisting of sub_count

        sub_list    list of all summary_cust_ids associated with subscription purchase
        sub_count   count of unique summary_cust_ids with subscription purchase
        '''
        sub_categories = ['Subscription', 'Flex']
        
        if fy:
            filtered_data = self.data.loc[self.data.price_type_group.isin(sub_categories) & (self.data.fy == fy)]
        else: 
            filtered_data = self.data.loc[self.data.price_type_group.isin(sub_categories)]

        sub_list = filtered_data.summary_cust_id.unique()
        sub_count = len(sub_list)

        SubData = namedtuple('SubData', ['subscriber_list', 'number_of_subscribers'])

        return SubData._make([sub_list, sub_count])


    def tickets_sold(self, date_start, date_end):
        '''Calculates total tickets sold within a provided date range
        Note: This uses the order date column to calculate

        Args:
        date_start      starting date of date range (inclusive)
        date_end        ending date of date range

        Returns:
        tickets_sold    total number of tickets sold (excluding comps) within 
                        the provided date range
        '''
        try:
            date_start = pd.to_datetime(date_start)
            date_end = pd.to_datetime(date_end)
        except TypeError:
            print("Unable to convert to date object. Please try this format: 'yyyy-mm-dd'")

        start_mask = self.data.order_dt >= date_start
        end_mask = self.data.order_dt <= date_end
        sold_mask = self.data.paid_amt > 0

        filtered = self.data.loc[start_mask & end_mask & sold_mask]
        tickets_sold = len(filtered)

        return tickets_sold


    def __repr__(self):
        return f"Tickets(fys='{self.fys}')"


    def __str__(self):
        return f"Tickets class consisting of {self.fys} for fiscal years"
