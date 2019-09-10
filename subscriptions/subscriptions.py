import pandas as pd

from .helpers.definitions import pkg_definitions

class Subscriptions:
    '''A class to simplify the process of managing subscription data.
    DATA USED FROM TESSITURA = "PS Package Order Listing"

    Args:
    fy              fiscal year in question (19, 20, etc.)
    path            path to data
                    Default: '../../data/sub/'
    '''

    def __init__(self, fy, path='../../data/sub/'):
        _cy_dfs = [] # current year
        _py_dfs = [] # prior year

        cy_tmp = pd.read_csv(path + f'fy{fy}.csv', encoding='ISO-8859-1')
        cy_tmp['fy'] = fy

        py_tmp = pd.read_csv(path + f'fy{fy-1}.csv', encoding='ISO-8859-1')
        py_tmp['fy'] = fy-1

        _cy_dfs.append(cy_tmp)
        _py_dfs.append(py_tmp)

        self.data = pd.concat(_cy_dfs, ignore_index=True)
        self.py_data = pd.concat(_py_dfs, ignore_index=True)
        self.fy = fy
        self.total_subs = sum(self.data['num_seats'])
        self.py_customer_numbers = set(self.py_data['customer_no'])
        self.customer_numbers = set(self.data['customer_no'])

    def retention(self):
        '''Calculate YoY retention of subscribers'''
        subs_both_fys = self.customer_numbers.intersection(self.py_customer_numbers)
        total_retained_subs = len(subs_both_fys)
        total_subs_py = len(self.py_customer_numbers)

        return round(total_retained_subs / total_subs_py * 100, 2)

    def new(self):
        '''Calculate new subscribers (did not subscribe in prior year)'''
        new_customers = self.customer_numbers - self.py_customer_numbers
        return len(new_customers)

    def total_seats(self, definitions=pkg_definitions):
        '''Calculate avg seats per pkg'''
        self.data['seats_per_pkg'] = self.data['pkg_desc'].map(definitions)
        self.data['total_seats_sold'] = self.data['seats_per_pkg'] * self.data['num_seats']
        return round(sum(self.data['total_seats_sold']) / self.total_subs, 1)
