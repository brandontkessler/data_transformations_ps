
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
