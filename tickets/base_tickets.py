import pandas as pd

from ..helper import internal_ids, ticketing_dtype


class _BaseTickets:
    '''Base Class for working with PS ticketing data

    Args:
        fys -- a list of integers representing fiscal years (ie. 19)
        path -- path to the data files
                default: '../../data/ticket/'
        dtype -- dtype provided to pandas for quicker data load
                 default: ticketing_dtype
        drop_nan -- If True, drops all summary_cust_id with NA as ID
                    default: True
    '''

    CAPACITY = 1750

    def __init__(self,
                 fys,
                 path='../../data/ticket/',
                 dtype=ticketing_dtype,
                 drop_nan=True,
                 drop_internal_ids=True):
        self.fys = fys
        self._path = path
        self._dtype = dtype
        self.data = self._build_dataset(drop_nan=drop_nan,
                                        drop_internal_ids=drop_internal_ids)

    # --------------------- magic methods ------------------
    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return f"Tickets(fys='{self.fys}')"

    # --------------------- constructor methods ------------------
    def _build_dataset(self, drop_nan, drop_internal_ids):
        data_gen = (self._import_data(fy) for fy in self.fys)
        data = pd.concat(data_gen, ignore_index=True)

        if drop_nan:
            data = self._drop_na_ids(data)
        if drop_internal_ids:
            data = self._drop_internal_ids(data)

        return data

    def _import_data(self, fy):
        file = self._path + f'fy{str(fy)}_all.csv'
        df = pd.read_csv(file, skiprows=3, dtype=self._dtype)
        df['perf_dt'] = self._date_convert(df['perf_dt'])
        df['order_dt'] = self._date_convert(df['order_dt'])
        df['dow'] = self._add_dow(df['perf_dt'])
        df['series'] = self._add_series_name(df['season_desc'])
        df['fy'] = fy
        return df

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

    # --------------------- utility methods ------------------
    def _inplace(self, inplace, data):
        if inplace:
            self.data = data
        else:
            return data

    def _check_series(self, series):
        options = ['Classics', 'Pops','Family', 'Summer', 'Specials',
                   'Connections', 'Organ', 'Chamber']

        check = all([s in options for s in series])
        msg = f'Series must only include: {options}'
        if not check:
            raise ValueError(msg)

    def _check_data(self, data):
        if data is None:
            data = self.data
        return data
