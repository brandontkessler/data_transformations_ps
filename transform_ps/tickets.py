from collections import namedtuple
import copy

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from .base_tickets import _BaseTickets
from .helpers import price_type_group_mapper
from .decorators import check_data, check_series, inplace

class Tickets(_BaseTickets):
    # ---------------------- filter methods -----------------
    @check_series
    @check_data
    @inplace
    def filter_series(self, *, series=['Classics', 'Pops', 'Summer'],
                      data=None, inplace=False):
        '''Filters to only include series provided

        Args:
        data -- Provide the dataframe to manipulate
                default: self.data
        series -- Iterable consisting of the names of the series' to include
                  Default: ['Classics', 'Pops', 'Summer']
        inplace -- Overwrites existing data if True
                   default: False
        '''
        result = data[data['series'].isin(series)].reset_index(drop=True)
        return result


    @check_data
    @inplace
    def keep_paid(self, *, data=None, inplace=False):
        result = data[data.paid_amt > 0].reset_index(drop=True)
        return result


    @check_data
    @inplace
    def drop_subs(self, *, data=None, inplace=False):
        current_subs = data.loc[
            (data['price_type_group'] == 'Subscription') |\
            (data['price_type_group'] == 'Flex')
        ]
        current_subs = set(current_subs['summary_cust_id'])

        result = data.loc[~data['summary_cust_id'].isin(current_subs)]
        return result


    @check_data
    @inplace
    def drop_sub_sales(self, *, data=None, inplace=False):
        mask = (data['price_type_group'] == 'Subscription') |\
               (data['price_type_group'] == 'Flex')

        result = data.loc[~mask]
        return result


    @check_data
    @inplace
    def filter_fys(self, fys, *, data=None, inplace=False):
        result = data.loc[data.fy.isin(fys)]
        return result


    @check_data
    @inplace
    def filter_perf_dt(self, to_date, *, data=None, inplace=False):
        result = data.loc[data['perf_dt'] <= to_date]
        return result


    # -------------------------- mutations -----------------------------
    @check_data
    @inplace
    def transform_price_type_group(self, *, data=None, inplace=False):
        data['price_type_group'] = data['price_type_group'].map(price_type_group_mapper)
        return data


    @check_data
    @inplace
    def add_concert_number(self, *, data=None, inplace=False):
        data['performance'] = data['perf_dt'].map(self._concert_mapper)
        data = data[pd.notnull(data['performance'])].reset_index(drop=True)

        # order/number performances
        ordered_perfs = data.sort_values('perf_dt')['performance'].drop_duplicates()
        numbered = {perf: num+1 for num,perf in enumerate(ordered_perfs)}

        # map numbered to performances
        data['perf_number'] = data['performance'].map(numbered)

        return data

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


    @check_data
    def new_to_file(self, fy, paid_only=True, *, data=None):
        '''Calculates total tickets sold within a provided date range

        Args:
        fy -- FY to identify new to file singles

        Returns:
        list of customer id numbers
        '''
        if paid_only:
            data = self.keep_paid()

        current = self.filter_fys(data=data, fys=[fy])
        prior_three = self.filter_fys(data=data, fys=[fy-1, fy-2, fy-3])

        current_customers = set(current.summary_cust_id)
        existing_customers = set(prior_three.summary_cust_id)

        new_to_file = current_customers - existing_customers

        current = current.loc[current.summary_cust_id.isin(new_to_file)]
        current = current[['summary_cust_id', 'perf_dt']].drop_duplicates()
        current = current.groupby('summary_cust_id').count().reset_index()

        retained_new = current.loc[current.perf_dt > 1]

        return new_to_file, retained_new


    @check_series
    def minimum_purchases(self, *, min_lim=3, series=['Classics', 'Pops'], fys=None):
        '''All non-subscribers that have purchased the min_lim amount or more

        Args:
        min_lim -- minimum concert purchases to be included
                   ex. if min_lim=3, only keep ids with purchases at >=3 concerts
                   default: 3
        series -- Iterable of series to be included
                  default: ['Classics', 'Pops']
        fys -- Filter based on provided fys
        '''
        data = self.data.copy()

        if fys:
            data = self.filter_fys(fys=fys, data=data)

        data = self.filter_series(data=data, series=series)
        data = self.drop_subs(data=data)
        data = self.keep_paid(data=data)

        data = data[['summary_cust_id', 'perf_dt']].reset_index(drop=True)
        data = data.drop_duplicates()

        data = data.groupby('summary_cust_id').agg('count').reset_index()

        data = data.loc[data.perf_dt >= min_lim]

        return len(data)


    @check_series
    def returning_singles_plt(self, to_date, series=['Classics', 'Pops', 'Summer'],
                          fys=None):
        '''Plots flow throughout the year of single ticket buyers
        '''
        to_date = self._date_convert(to_date)

        data = self.data.copy()

        data = self.filter_series(data=data, series=series)
        data = self.drop_subs(data=data)
        data = self.keep_paid(data=data)
        data = self.filter_perf_dt(to_date=to_date, data=data)

        if fys:
            data = self.filter_fys(fys=fys, data=data)

        data = data[['summary_cust_id', 'perf_dt']].reset_index(drop=True)
        data = data.drop_duplicates().reset_index(drop=True)

        concerts_to_dt = self.add_concert_number(data=data)
        attendances = concerts_to_dt.groupby('summary_cust_id').agg('count').reset_index()

        attendances = attendances.groupby('perf_number').agg({
            'summary_cust_id': 'count'
        }).reset_index()

        # If less than 10, fill out concerts with 0 attendance up to 10
        if len(attendances) < 10:
            for i in range(len(attendances)+1, 11):
                attendances = attendances.append(
                    pd.DataFrame({'perf_number': [i], 'summary_cust_id': [0]})
                )

        # Plot setup
        fig, ax = plt.subplots(figsize=(25,10))
        sns.set(style="ticks")

        # Create the plot
        ax = sns.barplot(x="perf_number", y="summary_cust_id", data=attendances)

        # titles
        ax.set_title("Non Subscription Retention to Date", fontsize=30)

        # axes
        ax.tick_params(axis='both', labelsize=16)
        ax.set_xlabel('Number of Performances', fontsize=20)
        ax.set_ylabel('Customers', fontsize=20)

        plt.xticks(rotation=0)

        # Show plot
        plt.show()


    @check_series
    def plot_singles_by_zone(self, to_date, series=['Classics'],
                         fys=None):
        to_date = self._date_convert(to_date)

        data = self.data.copy()

        data = self.filter_series(data=data, series=series)
        data = self.drop_subs(data=data)
        data = self.keep_paid(data=data)
        data = self.filter_perf_dt(to_date=to_date, data=data)

        if fys:
            data = self.filter_fys(fys=fys, data=data)

        data = data.groupby('price_zone').agg({'paid_amt': 'count'}).reset_index()
        data = data.loc[~data.price_zone.isin(['Price B', 'Price P'])]

        # Plot setup
        fig, ax = plt.subplots(figsize=(15,10))
        sns.set(style="ticks")

        # Create the plot
        ax = sns.barplot(x="price_zone", y="paid_amt", data=data)

        # titles
        ax.set_title(f"Single Tickets Sold by Price Zone {series}", fontsize=30)

        # axes
        ax.tick_params(axis='both', labelsize=16)
        ax.set_xlabel('Price Zone', fontsize=20)
        ax.set_ylabel('Total Single Tickets Sold to Date', fontsize=20)

        plt.xticks(rotation=0)

        # Show plot
        plt.show()