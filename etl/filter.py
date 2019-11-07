
def filter_individual_giving(data):
    data = data.copy()
    mask = data.campaign.str.contains('Government|Foundation|Corporate', regex=True)
    data = data.loc[~mask].reset_index(drop=True)

    return data


def filter_fys(data, fys):
    '''filters out fiscal years from data frame

    Args:
    fys -- An iterable of fiscal years
           Example: [18, 19]
    '''
    data = data.copy()
    mask = data.fy.isin(fys)
    data = data.loc[mask].reset_index(drop=True)

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

    result = data.loc[~data['summary_cust_id'].isin(current_subs)].reset_index(drop=True)
    return result


def filter_subs(data):
    current_subs = data.loc[
        (data['price_type_group'] == 'Subscription') |\
        (data['price_type_group'] == 'Flex')
    ]
    current_subs = set(current_subs['summary_cust_id'])

    result = data.loc[data['summary_cust_id'].isin(current_subs)].reset_index(drop=True)
    return result

def filter_single_sales_only(data):
    single_sales = data.loc[
        (data['price_type_group'] == 'Single ') |\
        (data['price_type_group'] == 'Single') |\
        (data['price_type_group'] == 'Discount')
    ]

    return single_sales


def filter_before_date(data, col, to_date):
    data = data.copy()
    result = data.loc[data[col] <= to_date].reset_index(drop=True)
    return result

def filter_by_date(data, col, date):
    data = data.copy()
    result = data.loc[data[col] == to_date].reset_index(drop=True)
    return result

def filter_new_to_file(data):
    '''baseline is max year in data provided. All prior years are existing customers'''
    data = data.copy()
    baseline = max(data['fy'])

    current = data.loc[data['fy'] == baseline].reset_index(drop=True)
    prior = data.loc[data['fy'] != baseline].reset_index(drop=True)

    current_customers = set(current.summary_cust_id)
    existing_customers = set(prior.summary_cust_id)

    new_to_file = current_customers - existing_customers

    current = current.loc[current.summary_cust_id.isin(new_to_file)]
    current = current[['summary_cust_id', 'perf_dt']].drop_duplicates()
    current = current.groupby('summary_cust_id').agg({'perf_dt': 'nunique'}).reset_index()

    retained_new = current.loc[current.perf_dt > 1]

    return new_to_file, retained_new


def filter_by_minimum_transactions(data, groupby, transaction_col, min_lim):
    '''All non-subscribers that have purchased the min_lim amount or more

    Args:
    groupby -- column to group by ex. 'summary_cust_id'
    transaction_col -- column representing transactions made
                       ex. 'perf_dt'
    min_lim -- minimum concert purchases to be included
               ex. if min_lim=3, only keep ids with purchases at >=3 concerts
    '''

    data = data.copy()
    data = data.groupby(groupby).agg({transaction_col: 'nunique'}).reset_index()
    data = data.loc[data[transaction_col] >= min_lim].reset_index(drop=True)

    return data
