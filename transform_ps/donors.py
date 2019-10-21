import pandas as pd

from .base_donors import _DonorBase
from .decorators import check_data, inplace


class Donors(_DonorBase):
    '''
    A simplified process of importing and transforming Pacific Symphony donor
    data.

    Args:
        path -- path to the data files
                default: '../../data/donor/'
        dtype -- dtype provided to pandas for quicker data load
                 default: dtype provided by .helpers.donor_dtype
        file_yr -- the starting year of file data
                   default: '08'
    '''
    # ---------------- common filters ---------------------
    @check_data
    @inplace
    def filter_fys(self, fys, *, data=None, inplace=False):
        '''filters out fiscal years from data frame

        Args:
        fys -- An iterable of fiscal years
               Example: [18, 19]

        '''
        mask = data.fy.isin(fys)
        data = data.loc[mask]

        return data


    @check_data
    @inplace
    def filter_by_list(self, filter_list, column_name, keep_in_list=True,
                       *, data=None, inplace=False):
        '''filters data by a provided list and column name
        note: data must have been run through 'parse_campaign_fy' method to add fy column

        Args:
        filter_list -- A list of boolean vals to filter on
        column_name -- Identify which column to filter on
        keep_in_list -- If True, keep rows that match values in list
                        default: True

        '''
        mask = data[column_name].isin(filter_list)

        if keep_in_list:
            mask = ~mask

        data = data.loc[mask].reset_index(drop=True)

        return data


    #  ---------- rare usage filters ---------------
    @check_data
    @inplace
    def individual_giving(self, *, data=None, inplace=False):
        mask = data.campaign.str.contains('Government|Foundation|Corporate', regex=True)
        data = data.loc[~mask].reset_index(drop=True)

        return data


    def box_circle_list(self, fy=None):
        '''Given the current dataframe, isolate a list of box circle members

        Args:
        fy -- Extract box circle for the given fy only
              default: None
        '''

        tmp = self.data.copy()

        if fy:
            fy_mask = tmp.fy == fy
            tmp = tmp.loc[fy_mask]

        mask = ['Box Circle' in campaign for campaign in tmp.campaign]
        box = tmp.loc[mask][['summary_cust_id']]

        return list(set(box['summary_cust_id']))

    @check_data
    @inplace
    def agg_by_amount_per_yr(self, *, threshold=None, greater_than_thresh=True,
                             equal_to_thresh=True, data=None, inplace=False,
                             **kwargs):
        '''Aggregates data by summary_cust_id

        Args:
        threshold -- amount at which to filter on (ex. 10000)
                     default: None
        greater_than_thresh -- filter above or below threshold
                               default: True
        equal_to_thresh -- filter equal to thresh
                           default: True
        **kwargs -- additional columns to include in agg
                    ex. cont_dt=['max', 'min']

        Example:
        Given a threshold of 10000, greater_than_thresh=False and equal_to_thresh=True,\
            data will be filtered less than or equal to 10000

        '''
        aggregator = {'gift_plus_pledge': 'sum'}
        for key, val in kwargs.items():
            aggregator[key] = val

        data = data.groupby(['summary_cust_id', 'fy']).agg(aggregator).reset_index()

        if greater_than_thresh and equal_to_thresh:
            operator = 'greater_equal'
        elif greater_than_thresh and not equal_to_thresh:
            operator = 'greater_than'
        elif not greater_than_thresh and equal_to_thresh:
            operator = 'less_equal'
        elif not greater_than_thresh and not equal_to_thresh:
            operator = 'less_than'
        else:
            raise Exception('There was an error building the operator')


        if threshold:
            if operator == 'greater_equal':
                mask = data.gift_plus_pledge >= threshold
            elif operator == 'greater_than':
                mask = data.gift_plus_pledge > threshold
            elif operator == 'less_equal':
                mask = data.gift_plus_pledge <= threshold
            elif operator == 'less_than':
                mask = data.gift_plus_pledge < threshold
            else:
                raise Exception('There is an error with the operator')

            data = data.loc[mask].reset_index(drop=True)
            return data

        return data


    def high_cap_prospects(self, fys):
        '''Categorizes prospects that are not already donors

        Capacity Ratings:
        We assume group 3 and lower is 'high capacity': $250,000+ over 5 years
        '''
        path = f'{self._path}../attribute/'
        file = 'capacity_rating.csv'
        high_capacity_group = ['3 -', '2 -', '1 -']

        attribute_data = pd.read_csv(path + file, skiprows=7)[['customer_no', 'key_value']]

        mask = attribute_data.key_value.map(lambda e: e[:3] in high_capacity_group)
        high_cap = attribute_data.loc[mask].reset_index(drop=True)

        two_yr_donors = self.filter_fys(fys=fys, inplace=False)
        unique_donors = set(two_yr_donors.customer_no)

        mask_existing_donors = ~high_cap.customer_no.isin(unique_donors)
        self.high_cap = set(high_cap.loc[mask_existing_donors]['customer_no'])

        return self.high_cap