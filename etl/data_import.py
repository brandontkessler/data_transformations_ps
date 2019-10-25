import pandas as pd

from .helpers import ticketing_dtype, donor_dtype, date_columns
from .decorators import check_fys_is_int
from . import transform

class ImportData:
    '''Imports data required from data types

    args:
        type -> confirms the data type in question to use the matching strategy
    '''

    def __init__(self):
        self.type_map = {
            'ticket': {
                'strategy': TicketImportStrategy,
                'dtype': ticketing_dtype
            },
            'donor': {
                'strategy': DonorImportStrategy,
                'dtype': donor_dtype
            },
            'subscriber': {
                'strategy': SubscriberImportStrategy
            },
            'mode_of_sale': {
                'strategy': ModeOfSaleImportStrategy
            },
            'attribute': {
                'strategy': AttributeImportStrategy
            }
        }

    def send_data(self, type, fys, path, qtr=None):
        data_type = self.type_map[type]
        dtype = data_type.get('dtype')
        strategy = data_type['strategy']()
        data = strategy.get_data(fys=fys, path=path, dtype=dtype, qtr=qtr)
        return data


class TicketImportStrategy:
    '''Strategy for importing ticket data'''
    @check_fys_is_int
    def get_data(self, fys, path=None, dtype=None, qtr=None):
        fp = path or '../../data/ticket/'
        data_gen = (self.import_file(fy=fy, path=fp, dtype=dtype) for fy in fys)
        data = pd.concat(data_gen, ignore_index=True)
        return data

    def import_file(self, fy, path, dtype=None):
        file = path + f'fy{str(fy)}_all.csv'
        df = pd.read_csv(file, dtype=dtype, skiprows=3, parse_dates=date_columns.get('ticket'))
        return df


class DonorImportStrategy:
    '''Strategy for importing donor data'''
    def get_data(self, fys, path=None, dtype=None, qtr=None):
        '''Gets donor data
        args:
            fys -> singular fiscal year for base of file ex. '08' or 13
        '''
        fp = path or '../../data/donor/'
        file = f"donors_fy{fys}-present.csv"
        data = pd.read_csv(fp + file, encoding='ISO-8859-1', dtype=dtype,
            parse_dates=date_columns.get('donor'), date_parser=transform.date_convert)

        return data


class SubscriberImportStrategy:
    '''Strategy for import subscriber data'''
    @check_fys_is_int
    def get_data(self, fys, path=None, dtype=None, qtr=None):
        fp = path or '../../data/sub/'
        data_gen = (self.import_file(fy=fy, path=fp) for fy in fys)
        data = pd.concat(data_gen, ignore_index=True)
        return data

    def import_file(self, fy, path):
        data = pd.read_csv(path + f'fy{fy}.csv', encoding='ISO-8859-1',
            parse_dates=date_columns.get('subscriber'))
        return data


class ModeOfSaleImportStrategy:
    '''Strategy for importing mode of sale data'''
    def get_data(self, fys, qtr, path=None, dtype=None):
        fp = path or '../../data/mode_of_sale/'
        data = pd.read_csv(f'{fp}q{qtr}_{fys}.csv')
        return data


class AttributeImportStrategy:
    '''Strategy for importing attribute data'''
    def get_data(self, file_name=None, path=None, *args, **kwargs):
        fp = path or '../../data/attribute/'
        file = file_name or 'capacity_rating.csv'
        data = pd.read_csv(fp + file, skiprows=7)[['customer_no', 'key_value']]

        return data
