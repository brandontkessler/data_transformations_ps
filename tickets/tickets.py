from collections import namedtuple
import copy

from . import _BaseTickets
from ..helper import price_type_group_mapper

class Tickets(_BaseTickets):

    # ---------------------- filter methods -----------------
    def filter_series(self, data=None, series=['Classics', 'Pops', 'Summer'],
                      inplace=False):
        '''Filters to only include series provided

        Args:
        data -- Provide the dataframe to manipulate
                default: self.data
        series -- Iterable consisting of the names of the series' to include
                  Default: ['Classics', 'Pops', 'Summer']
        inplace -- Overwrites existing data if True
                   default: False

        '''
        data = self._check_data(data) # Check if dataframe provided
        self._check_series(series) # Check if series are valid
        result = data[data['series'].isin(series)].reset_index(drop=True)
        return self._inplace(inplace, result)


    def keep_paid(self, data=None, inplace=False):
        data = self._check_data(data) # Check if dataframe provided
        result = data[data.paid_amt > 0].reset_index(drop=True)
        return self._inplace(inplace, result)


    def drop_subs(self, data=None, inplace=False):
        data = self._check_data(data)
        data = self.transform_price_type_group(data=data)

        current_subs = data.loc[data['price_type_group'] == 'Subscription']
        current_subs = set(current_subs['summary_cust_id'])

        result = data.loc[~data['summary_cust_id'].isin(current_subs)]
        return self._inplace(inplace, result)


    def filter_fy(self, fy, data=None, inplace=False):
        data = self._check_data(data)
        result = data.loc[data.fy == fy]
        return self._inplace(inplace, result)

    # -------------------------- mutations -----------------------------
    def transform_price_type_group(self, mapper=price_type_group_mapper,
                                   data=None, inplace=False):
        data = self._check_data(data)
        data['price_type_group'] = data['price_type_group'].map(mapper)
        return self._inplace(inplace, data)

    # ------------------------- summary info -----------------------
    def total_subs(self, fy=None):
        '''Simplified analysis of subscribers (Subscriptions and Flex)

        args:
        fy -- (optional) Fiscal Year under analysis (ie. 19)

        returns:
        SubData -- a named tuple consisting of two variables:
            sub_ids -- list of all unique summary_cust_ids that are subs
            num_of_subs -- total count in subscriber_list
        '''

        sub_categories = ['Subscription', 'Flex']
        mask = self.data.price_type_group.isin(sub_categories)

        if fy:
            mask = mask & (self.data.fy == fy)

        filtered_data = self.data.loc[mask]

        sub_ids = filtered_data.summary_cust_id.unique()
        num_of_subs = len(sub_ids)

        SubData = namedtuple('SubData', 'sub_ids num_of_subs')

        return SubData(sub_ids, num_of_subs)


    def tickets_sold_by_date(self, date_start, date_end):
        '''Calculates total tickets sold within a provided date range
        Note: This uses the order date column to calculate

        Args:
        date_start -- starting date of date range (inclusive)
        date_end -- ending date of date range

        Returns:
        tickets_sold -- total number of tickets sold (excluding comps) within
                        the provided date range
        '''
        date_start = self._date_convert(date_start)
        date_end = self._date_convert(date_end)

        data = self.keep_paid()

        start_mask = self.data.order_dt >= date_start
        end_mask = self.data.order_dt <= date_end

        filtered = data.loc[start_mask & end_mask]

        return len(filtered)


    def minimum_purchases(self, min_lim=3, series=['Classics', 'Pops'], fy=None):
        '''All non-subscribers that have purchased the min_lim amount or more

        Args:
        min_lim -- minimum concert purchases to be included
                   ex. if min_lim=3, only keep ids with purchases at >=3 concerts
                   default: 3
        series -- Iterable of series to be included
                  default: ['Classics', 'Pops']
        fy -- If provided, filter based on just the provided fy
        '''
        data = self.data.copy()

        data = self.filter_series(data=data, series=series)
        data = self.drop_subs(data=data)
        data = self.keep_paid(data=data)

        if fy:
            data = self.filter_fy(fy=fy, data=data)

        data = data[['summary_cust_id', 'perf_dt', 'fy']].reset_index(drop=True)
        data = data.drop_duplicates()

        data = data.groupby('summary_cust_id').agg('count').reset_index()
        data = data.loc[data.fy >= min_lim]

        return len(data)
