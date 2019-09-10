import pandas as pd

from .helpers import donor_dtype

class Donors:
    '''
    A simplified process of importing and transforming Pacific Symphony donor
    data.

    Args:
        path        path to the data files
                    default: '../../data/donor/'
        dtype       dtype provided to pandas for quicker data load
                    default: dtype provided by .helpers.donor_dtype
        file_yr     the starting year of file data
                    default: '08'
    '''

    def __init__(self, path='../../data/donor/', dtype=donor_dtype, file_yr='08'):
        self._path = path
        self._dtype = dtype
        self._file = f'donors_fy{file_yr}-present.csv'

        self.data = pd.read_csv(path + self._file,
                                encoding='ISO-8859-1',
                                dtype=self._dtype)


    def parse_campaign_fy(self):
        '''parses the campaign year into a new column called 'fy'

        Returns:
        self
        '''

        fy = self.data.campaign.str[6:8]
        self.data['fy'] = fy

        filter_mask = {fy: False for fy in self.data['fy'].drop_duplicates()}
        for fy, boolean in filter_mask.items():
            try:
                int(fy[0])
                filter_mask[fy] = True
            except:
                continue

        self.data['keep'] = self.data['fy'].map(filter_mask)        # map the filter mask
        self.data = self.data.loc[self.data['keep']].reset_index(drop=True)
        self.data.drop(columns=['keep'], inplace=True)              # drop keeps col
        self.data = self.data.astype({'fy': 'int64'})               # convert to int

        return self


    def filter_fys(self, fys):
        '''filters out fiscal years from data frame

        Args:
        fys         An iterable of fiscal years
                    Example: [18, 19]

        Returns:
        self
        '''

        mask = self.data.fy.isin(fys)
        self.data = self.data.loc[mask]

        return self


    def filter_by_list(self, filter_list, column_name, keep_in_list=True):
        '''filters data by a provided list and column name
        note: data must have been run through 'parse_campaign_fy' method to add fy column

        Args:
        filter_list             A list of boolean vals to filter on
        column_name             Identify which column to filter on
        keep_in_list            If True, keep rows that match values in list
                                default: True

        Returns:
        self
        '''

        mask = self.data[column_name].isin(filter_list)

        if keep_in_list:
            self.data = self.data.loc[mask].reset_index(drop=True)
        else:
            self.data = self.data.loc[~mask].reset_index(drop=True)

        return self


    def box_circle_list(self, fy=None):
        '''Given the current dataframe, isolate a list of box circle members

        Args:
        fy              Extract box circle for the given fy only
                        default: None
        '''

        tmp = self.data.copy()

        if fy:
            fy_mask = tmp.fy == fy
            tmp = tmp.loc[fy_mask]

        mask = ['Box Circle' in i for i in tmp.campaign]
        box = tmp.loc[mask][['summary_cust_id']]

        return list(set(box['summary_cust_id']))


    def agg_by_amount_per_yr(self, threshold=None, greater_than_thresh=True,
                             equal_to_thresh=True, **kwargs):
        '''Aggregates data by summary_cust_id

        Args:
        threshold               amount at which to filter on (ex. 10000)
                                default: None
        greater_than_thresh     filter above or below threshold
                                default: True
        equal_to_thresh         filter equal to thresh
                                default: True
        **kwargs                additional columns to include in agg
                                ex. cont_dt=['max', 'min']


        Example:
        Given a threshold of 10000, greater_than_thresh=False and equal_to_thresh=True,\
            data will be filtered less than or equal to 10000

        Returns:
        self                    dataframe consists only of summary_cust_id, fy, gift_plus_pledge total
        '''

        aggregator = {'gift_plus_pledge': 'sum'}
        for key, val in kwargs.items():
            aggregator[key] = val

        self.data = self.data.groupby(['summary_cust_id', 'fy']).agg(aggregator).reset_index()

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
                mask = self.data.gift_plus_pledge >= threshold
            elif operator == 'greater_than':
                mask = self.data.gift_plus_pledge > threshold
            elif operator == 'less_equal':
                mask = self.data.gift_plus_pledge <= threshold
            elif operator == 'less_than':
                mask = self.data.gift_plus_pledge < threshold
            else:
                raise Exception('There is an error with the operator')

            self.data = self.data.loc[mask].reset_index(drop=True)
            return self

        return self
