import pandas as pd
import datetime as dt

from .helpers import concert_mapper_fy20, price_type_group_mapper


def date_convert(obj):
    try:
        return pd.to_datetime(obj)
    except:
        pass

    try:
        # Try to match against poor date entries like:
        # '11/18/2013 15:31:18:733' to convert to: '11/18/2013'
        separated = obj.split(' ')[0]
        return pd.to_datetime(separated)
    except:
        raise ValueError(f"There is a problem with {obj}")


def add_dow(pd_series):
    return pd_series.transform(lambda x: x.strftime("%A"))


def convert_to_fy(date_obj):
    month_check = int(date_obj.strftime('%m'))
    year = int(date_obj.strftime('%y'))

    if month_check < 7:
        return year

    return year + 1


def add_concert_number(data):
    data = data.copy()
    concert_mapper_datetime = {pd.to_datetime(k): v for k,v in concert_mapper_fy20.items()}
    data['performance'] = data['perf_dt'].map(concert_mapper_datetime)
    data = data[pd.notnull(data['performance'])].reset_index(drop=True)

    # order/number performances
    ordered_perfs = data.sort_values('perf_dt')['performance'].drop_duplicates()
    numbered = {perf: num+1 for num,perf in enumerate(ordered_perfs)}

    # map numbered to performances
    data['perf_number'] = data['performance'].map(numbered)

    return data


def transform_price_type_group(data):
    data = data.copy()
    data['price_type_group'] = data['price_type_group'].map(price_type_group_mapper)
    return data



def donor_convert_cont_dt_to_monday(date):
    date = pd.to_datetime(date)
    if date < pd.to_datetime('7/1/2019'):
        date = pd.to_datetime('7/1/2019')
    return date - dt.timedelta(date.weekday())
