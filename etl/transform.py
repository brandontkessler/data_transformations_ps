import pandas as pd


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
