import pandas as pd

from .helpers import ticketing_dtype, group_sales_ids, internal_ids

class _BaseTickets:
    '''Base Class for working with PS ticketing data

    Args:
        fys -- a list of integers representing fiscal years (ie. 19)
        path -- path to the data files
                default: '../../data/ticket/'
        drop_nan -- If True, drops all summary_cust_id with NA as ID
                    default: True
    '''

    CAPACITY = 1750
    DTYPE = ticketing_dtype

    DEFAULT_PATH = '../../data/ticket/'

    def __init__(self,
                 fys,
                 path=None,
                 drop_nan=True,
                 drop_internal_ids=True):
        self._fys = fys
        self._path = path or self.DEFAULT_PATH
        self._concert_mapper = self._get_concert_mapper()

        self.data = self._build_dataset(drop_nan=drop_nan,
                                        drop_internal_ids=drop_internal_ids)

    # --------------------- magic methods ------------------
    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return f"Tickets(fys='{self._fys}')"

    def __str__(self):
        return f'{self.data.columns}'

    # --------------------- constructor methods ------------------
    def _build_dataset(self, drop_nan, drop_internal_ids):

        data_gen = map(self._import_data, self._fys)
        data = pd.concat(data_gen, ignore_index=True)

        if drop_nan:
            data = self._drop_na_ids(data)
        if drop_internal_ids:
            data = self._drop_internal_ids(data)

        data['price_zone'] = self._get_price_zones(data['zone_desc'])

        return data

    def _import_data(self, fy):
        file = self._path + f'fy{str(fy)}_all.csv'
        df = pd.read_csv(file, skiprows=3, dtype=self.DTYPE)
        df['perf_dt'] = self._date_convert(df['perf_dt'])
        df['order_dt'] = self._date_convert(df['order_dt'])
        df['dow'] = self._add_dow(df['perf_dt'])
        df['series'] = self._add_series_name(df['season_desc'])
        df['fy'] = fy
        return df

    def _get_concert_mapper(self):
        df = pd.read_csv(self._path + f'../performance/fy{max(self._fys)}.csv',
                         encoding='ISO-8859-1',
                         index_col='perf_dt')
        df.index = self._date_convert(df.index)
        return df.to_dict().get('performance')

    def _date_convert(self, obj):
        if isinstance(obj, pd.Series):
            return pd.to_datetime(obj).reset_index(drop=True)
        return pd.to_datetime(obj)

    def _add_dow(self, pd_series):
        return pd_series.transform(lambda x: x.strftime("%A"))

    def _add_series_name(self, pd_series):
        return pd_series.transform(lambda x: x.split(" ")[-1])

    def _drop_na_ids(self, data):
        data = data[pd.notnull(data['summary_cust_id'])].reset_index(drop=True)
        return data

    def _drop_internal_ids(self, data):
        data = data[~data['summary_cust_id'].isin(internal_ids)].reset_index(drop=True)
        return data

    def _drop_group_sales_ids(self, data):
        data = data[~data['summary_cust_id'].isin(group_sales_ids)].reset_index(drop=True)
        return data

    def _map_zones(self, zone):
        if zone[:5] == 'Price':
            return zone[:7]
        elif 'Box' in zone:
            return 'Price B'
        elif 'Accessible' in zone:
            return zone[11:]
        else:
            return zone

    def _get_price_zones(self, data):
        data = data.map(self._map_zones)
        return data