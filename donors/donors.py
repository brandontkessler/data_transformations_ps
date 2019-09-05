import pandas as pd

from .helpers import donor_dtype

class Donors:
    '''
    A simplified process of importing and transforming Pacific Symphony donor
    data.

    Args:
        path        path to the data files (ex. '../../data/donor/')
        dtype       (optional) dtype provided to pandas for quicker data load
        start_yr    (optional) the starting year of file data (default='08')
    '''

    def __init__(self, path, dtype=donor_dtype, file_yr='08'):
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
        self.data = self.data.loc[self.data['keep']].reset_index()  # filter by keep=True
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
        

    def agg_by_fy(self):
        pass