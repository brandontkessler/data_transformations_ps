import pandas as pd
from . import transform, filter
from .helpers import internal_ids
from .decorators import cache_working_data, check_working_cache, timer


class PrepDataFactory:
    def __init__(self):
        self.mapper = {
            'ticket': PrepTicketData,
            'donor': PrepDonorData,
            'subscriber': PrepSubscriberData,
            'mode_of_sale': PrepModeOfSaleData,
            'attribute': PrepAttributeData
        }

    def get_preparer(self, type):
        return self.mapper.get(type)


class PrepTicketData:
    @timer
    @check_working_cache
    @cache_working_data
    def prepare_data(self, dataframe, full, type):
        '''Prepares the ticketing data for analysis

        args:
            data -> Data to be prepared (typically raw data from PSData Object)
            full -> Boolean. Removes internal ids and unsold
        '''
        data = dataframe.copy()

        data['dow'] = transform.add_dow(data['perf_dt'])
        data['series'] = self.add_series_name(data['season_desc'])
        data['fy'] = data['perf_dt'].map(transform.convert_to_fy)
        data['price_zone'] = data['zone_desc'].map(self.zone_mapper)

        if full:
            data = data[pd.notnull(data['summary_cust_id'])]\
                .reset_index(drop=True)
            data = data[~data['summary_cust_id'].isin(internal_ids)]\
                .reset_index(drop=True)

        return data

    @staticmethod
    def zone_mapper(zone):
        if zone[:5] == 'Price':
            return zone[:7]
        elif 'Box' in zone:
            return 'Price B'
        elif 'Accessible' in zone:
            return zone[11:]
        else:
            return zone

    @staticmethod
    def add_series_name(pd_series):
        return pd_series.transform(lambda x: x.split(" ")[-1])



class PrepDonorData:
    @timer
    @check_working_cache
    @cache_working_data
    def prepare_data(self, dataframe, full, type):
        data = dataframe.copy()

        if full:
            data['fy'] = data['campaign'].str[6:8]
            fy_mapper = self.fy_mapper_builder(data)
            data = self.parse_campaign_fy(data, fy_mapper)

        return data


    @staticmethod
    def parse_campaign_fy(data, fy_mapper):
        '''parses the campaign year into a new column called "fy"'''
        mask = data['fy'].map(fy_mapper) # map the fys
        data = data.loc[mask].reset_index(drop=True)
        data = data.astype({'fy': 'int64'}) # convert to int
        return data


    @staticmethod
    def fy_mapper_builder(data):
        fy_mapper = {fy: False for fy in data['fy'].drop_duplicates()}
        for fy in fy_mapper.keys():
            try:
                int(fy[0])
                fy_mapper[fy] = True
            except:
                continue
        return fy_mapper


class PrepSubscriberData:
    @timer
    def prepare_data(self, dataframe, full, type):
        data = dataframe.copy()
        data['fy'] = data['season_desc'].map(self.parse_fy)
        data = filter.filter_paid_only(data, 'tot_due_amt')
        return data

    @staticmethod
    def parse_fy(description):
        if 'Summer' in description:
            fy = int(description.split(' ')[1][2:]) + 1
        else:
            fy = int(description.split('-')[1][:2])
        return fy


class PrepModeOfSaleData:
    @timer
    @check_working_cache
    @cache_working_data
    def prepare_data(self, dataframe, full, type):
        data = dataframe.copy()
        data['season'] = [season.split(' ')[2] for season in data['season']]
        data['ordered'] = data['ps_num_ord'] + data['cs_num_ord']
        data['paid'] = data['ps_tot_paid_amt'] + data['cs_tot_paid_amt']

        if full:
            data = self.fix_mos_desc(data)

        return data

    @staticmethod
    def fix_mos_desc(data):
        mapper = {
            'OC Box Office': 'OC Box Office',
            'OC Donor Relations': 'OC Box Office',
            'OC House': 'OC Box Office',
            'OC Mobile': 'OC Box Office'
        }

        data['mos_desc'] = data['mos_desc'].replace(mapper)
        data['mos_desc'] = data['mos_desc'].replace({'OC': 'SCFTA'}, regex=True)
        return data

class PrepAttributeData:
    @timer
    @check_working_cache
    @cache_working_data
    def prepare_data(self, dataframe, full, type):
        data = dataframe.copy()
        return data
