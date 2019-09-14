from itertools import chain

from . import Tickets
from ..helper import opera_dates_19

class Classics(Tickets):

    def add_concert_numbers_clx(self, fy, data=None, inplace=False):
        '''Adds the appropriate concert number for each date of concert'''
        data = self._check_data(data)
        data = self.filter_series(data=data, series=['Classics'])
        data = self.filter_fy(fy=fy, data=data)

        concert_dates = {dt for dt in data.perf_dt}
        concert_numbers = chain.from_iterable([[i]*3 for i in range(1,13)])
        concert_mapper = dict(zip(sorted(concert_dates), concert_numbers))

        data['concert_number'] = data['perf_dt'].map(concert_mapper)
        return self._inplace(inplace, data)


    def remove_opera(self, opera_dates=opera_dates_19, data=None, inplace=False):
        '''Removes dates of opera

        Args:
        opera_dates -- iterable of dates of the opera in the form of 'yyyy-mm-dd'
                       default: opera dates for fy19
        '''
        data = self._check_data(data)

        data['tmp'] = data.perf_dt.map(lambda x: x.strftime('%Y-%m-%d'))
        data = data.loc[~data.tmp.isin(opera_dates)].reset_index(drop=True)
        data.drop(columns=['tmp'], inplace=True)

        return self._inplace(inplace, data)
