import pandas as pd
import numpy as np

from .helpers import pkg_definitions

class Subscriptions:
    '''A class to simplify the process of managing subscription data.
    DATA USED FROM TESSITURA = "PS Package Order Listing"

    Args:
    fy -- fiscal year in question (19, 20, etc.)
    path -- path to data
            Default: '../../data/sub/'
    '''

    def __init__(self, fy, path='../../data/sub/'):
        self.fy = fy
        self.data = self._data_import(fy=fy, path=path)
        self.py_data = self._data_import(fy=fy-1, path=path)
        self.total_pkgs = self._get_total_pkgs()
        self.py_customer_numbers = set(self.py_data['customer_no'])
        self.customer_numbers = set(self.data['customer_no'])

    # ------------------- constructor methods --------------
    def _data_import(self, fy, path):
        data = pd.read_csv(path + f'fy{fy}.csv', encoding='ISO-8859-1')
        data['fy'] = fy
        data['order_dt'] = self._date_convert(data['order_dt'])
        return data

    def _date_convert(self, obj):
        if isinstance(obj, pd.Series):
            return pd.to_datetime(obj).reset_index(drop=True)
        return pd.to_datetime(obj)


    def _get_total_pkgs(self):
        return sum(self.data['num_seats'])

    # ------------------ summary statistics ----------------
    def retention(self):
        '''Calculate YoY retention of subscribers'''
        ids_retained = self.customer_numbers.intersection(self.py_customer_numbers)
        retained_subs = len(ids_retained)
        total_subs_py = len(self.py_customer_numbers)
        return round(retained_subs / total_subs_py * 100, 2)

    def new(self):
        '''Calculate new subscribers (did not subscribe in prior year)'''
        new_customers = self.customer_numbers - self.py_customer_numbers
        data = self.data.copy()
        data = data.loc[data['customer_no'].isin(new_customers)]
        return sum(data['num_seats'])

    def avg_seats_per_pkg(self, definitions=pkg_definitions):
        '''Calculate avg seats per pkg'''
        data = self.data.copy()
        data['seats_per_pkg'] = data['pkg_desc'].map(definitions)
        data['total_seats_sold'] = data['seats_per_pkg'] * data['num_seats']
        return round(np.sum(data['total_seats_sold']) / self.total_pkgs, 1)
