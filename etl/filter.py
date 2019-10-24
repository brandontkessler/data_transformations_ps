
def filter_individual_giving(data):
    mask = data.campaign.str.contains('Government|Foundation|Corporate', regex=True)
    data = data.loc[~mask].reset_index(drop=True)

    return data


def filter_fys(data, fys):
    '''filters out fiscal years from data frame

    Args:
    fys -- An iterable of fiscal years
           Example: [18, 19]
    '''
    mask = data.fy.isin(fys)
    data = data.loc[mask]

    return data


def filter_paid_only(data, column):
    data = data.loc[data[column] > 0].reset_index(drop=True)
    return data


def filter_by_list(data, filter_list, column_name, keep_in_list=True):
    '''filters data by a provided list and column name
    note: data must have been run through 'parse_campaign_fy' method to add fy column

    Args:
    filter_list -- A list of vals to filter on
    column_name -- Identify which column to filter
    keep_in_list -- If True, keep rows that match values in list
                    default: True

    '''
    mask = data[column_name].isin(filter_list)

    if keep_in_list:
        mask = ~mask

    data = data.loc[mask].reset_index(drop=True)

    return data


def filter_by_series(data, series):
    '''Filters to only include series provided

    Args:
    data -- Provide the dataframe to manipulate
    series -- Iterable consisting of the names of the series' to include
              Default: ['Classics', 'Pops', 'Summer']
    '''
    result = data[data['series'].isin(series)].reset_index(drop=True)
    return result


def filter_non_subs(data):
    current_subs = data.loc[
        (data['price_type_group'] == 'Subscription') |\
        (data['price_type_group'] == 'Flex')
    ]
    current_subs = set(current_subs['summary_cust_id'])

    result = data.loc[~data['summary_cust_id'].isin(current_subs)]
    return result


def filter_subs(data):
    current_subs = data.loc[
        (data['price_type_group'] == 'Subscription') |\
        (data['price_type_group'] == 'Flex')
    ]
    current_subs = set(current_subs['summary_cust_id'])

    result = data.loc[data['summary_cust_id'].isin(current_subs)]
    return result


def filter_before_date(data, col, to_date):
    result = data.loc[data[col] <= to_date]
    return result

def filter_by_date(data, col, date):
    result = data.loc[data[col] == to_date]
    return result


def filter_by_minimum_transactions(data, transaction_col, min_lim):
    '''All non-subscribers that have purchased the min_lim amount or more

    Args:
    transaction_col -- column representing transactions made
                       ex. 'perf_dt'
    min_lim -- minimum concert purchases to be included
               ex. if min_lim=3, only keep ids with purchases at >=3 concerts
    '''

    data = data.copy()
    data = data.loc[data.perf_dt >= min_lim]

    return data
