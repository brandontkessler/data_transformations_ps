from .decorators import build_operator

def basic_aggregator(data, grp_by, col_to_agg, method, new_col_names=None):
    '''aggregates a single column and method

    grp_by can be a single column or list

    example:
    grp = ['customer_id', 'name']
    basic_aggregator(data, grp, 'paid_amt', 'sum')
    '''

    aggregated = data.groupby(grp_by).agg({
        col_to_agg: method
    }).reset_index()

    if new_col_names:
        aggregated.columns = new_col_names

    return aggregated


def complex_aggregator(data, grp_by, aggregator, new_col_names=None):
    '''aggregates pandas df info based on a provided aggregator

    grp_by can be a single column or list of columns
    aggregator is a dictionary

    example:
    grp = ['customer_id', 'name']
    aggregator = {
        'amount_paid': ['sum', 'count'],
        'amount_owed': 'sum'
    }
    complex_aggregator(data, grp, aggregator)
    '''

    aggregated = data.groupby(grp_by).agg(aggregator).reset_index()

    if new_col_names:
        aggregated.columns = new_col_names

    return aggregated

@build_operator
def threshold_aggregator(data, threshold, greater_than=True, equal_to=True,
                        additional_agg=None):
    '''Aggregates data by summary_cust_id, fy by per year, donor thresholds

    Args:
    threshold -- amount at which to filter on (ex. 10000)
    greater_than -- filter above or below threshold
                           default: True
    equal_to -- filter equal to thresh
                       default: True
    additional_agg -- additional columns and methods to aggregate on:
                example: {
                    'transactions': ['sum', 'count'],
                    'payments': ['sum', 'count'],
                    'returns': 'sum'
                }

    Example:
    Given a threshold of 10000, greater_than=False and equal_to=True, data will
    be filtered less than or equal to 10000 total donation_amt per yr
    '''
    aggregator = {'gift_plus_pledge': 'sum'}
    aggregator.update(additional_agg or {})

    grp = ['summary_cust_id', 'fy']
    data = complex_aggregator(data, grp, aggregator)
    mask = kwargs.get('mask')

    data = data.loc[mask].reset_index(drop=True)
    return data
