import pandas as pd

from .helpers import ticketing_dtype, donor_dtype

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
            }
        }

    def send_data(self, type, fys, path):
        data_type = self.type_map[type]
        dtype = data_type.get('dtype')
        strategy = data_type['strategy']()
        return strategy.get_data(fys=fys, path=path, dtype=dtype)


class TicketImportStrategy:
    '''Strategy for importing ticket data'''
    def get_data(self, fys, path=None, dtype=None):
        if isinstance(fys, int):
            fys = [fys]

        fp = path or '../../data/ticket/'
        data_gen = (self.import_file(fy=fy, path=fp, dtype=dtype) for fy in fys)
        data = pd.concat(data_gen, ignore_index=True)
        return data

    def import_file(self, fy, path, dtype=None):
        file = path + f'fy{str(fy)}_all.csv'
        df = pd.read_csv(file, dtype=dtype, skiprows=3)
        return df


class DonorImportStrategy:
    '''Strategy for importing donor data'''
    def get_data(self, fys, path=None, dtype=None):
        '''Gets donor data
        args:
            fys -> singular fiscal year for base of file ex. '08' or 13
        '''
        fp = path or '../../data/donor/'
        file = f"donors_fy{fys}-present.csv"
        data = pd.read_csv(fp + file, encoding='ISO-8859-1', dtype=dtype)
        return data


class SubscriberImportStrategy:
    '''Strategy for import subscriber data'''
    def get_data(self, fys, path=None, dtype=None):
        if isinstance(fys, int):
            fys = [fys]

        fp = path or '../../data/ticket/'
        data_gen = (self.import_file(fy=fy, path=fp) for fy in fys)
        data = pd.concat(data_gen, ignore_index=True)
        return data

    def import_file(self, fy, path):
        data = pd.read_csv(path + f'fy{fy}.csv', encoding='ISO-8859-1')
        return data


class PrepData:

    def date_convert(self, obj):
        if isinstance(obj, pd.Series):
            return pd.to_datetime(obj).reset_index(drop=True)
        return pd.to_datetime(obj)
