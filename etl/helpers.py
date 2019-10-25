import numpy as np
import math

date_columns = {
    'ticket': ['perf_dt', 'order_dt'],
    'donor': ['cont_dt', 'trn_dt'],
    'subscriber': ['order_dt']
}

ticketing_dtype = {
    'perf_code': object,
    'perf_no': np.int64,
    'perf_dt': object,
    'zone_no': np.int64,
    'zone_desc': object,
    'section': object,
    'row': object,
    'seat': np.int64,
    'home_price': np.float64,
    'paid_amt': np.float64,
    'fee_amt': np.float64,
    'seat_status': np.int64,
    'seat_status_desc': object,
    'customer_no': np.float64,
    'order_no': np.float64,
    'order_dt': object,
    'price_type_group_id': np.float64,
    'price_type_group': object,
    'pd_up': object,
    'season': np.int64,
    'season_desc': object,
    'summary_cust_id': np.float64,
    'summary_cust_name': object,
    'attended': object
}


donor_dtype = {
    'trn_count': np.dtype('int64'),
    'contribution_amt': np.dtype('float64'),
    'pledge': np.dtype('float64'),
    'pledge_payment': np.dtype('float64'),
    'gift': np.dtype('float64'),
    'gift_plus_pledge': np.dtype('float64'),
    'restricted': np.dtype('float64'),
    'write_off': np.dtype('float64'),
    'total_received': np.dtype('float64'),
    'batch_no': np.dtype('int64'),
    'ref_no': np.dtype('int64'),
    'fund_no': np.dtype('int64'),
    'fund_desc': np.dtype('O'),
    'fyear': np.dtype('float64'),
    'campaign_no': np.dtype('int64'),
    'campaign': np.dtype('O'),
    'cont_designation_id': np.dtype('int64'),
    'cont_designation': np.dtype('O'),
    'channel_id': np.dtype('int64'),
    'channel_desc': np.dtype('O'),
    'pmt_method_id': np.dtype('float64'),
    'pmt_method': np.dtype('float64'),
    'pledge_pmt_amt': np.dtype('float64'),
    'gift_pmt_amt': np.dtype('float64'),
    'pmt_count': np.dtype('int64'),
    'customer_no': np.dtype('int64'),
    'lname': np.dtype('O'),
    'fname': np.dtype('O'),
    'creditee_type': np.dtype('float64'),
    'creditee_type_desc': np.dtype('O'),
    'creditee_no': np.dtype('float64'),
    'creditee_name': np.dtype('O'),
    'resolved_cust_type': np.dtype('int64'),
    'resolved_cust_id': np.dtype('int64'),
    'resolved_cust_name': np.dtype('O'),
    'summary_cust_id': np.dtype('int64'),
    'summary_cust_name': np.dtype('O'),
    'summary_sort': np.dtype('O'),
    'display_name': np.dtype('O'),
    'sort_name': np.dtype('O'),
    'cont_dt': np.dtype('O'),
    'cont_fy': np.dtype('int64'),
    'cont_fy_month': np.dtype('O'),
    'cont_cy': np.dtype('int64'),
    'cont_cy_month': np.dtype('O'),
    'trn_dt': np.dtype('O'),
    'trn_fy': np.dtype('int64'),
    'trn_fy_month': np.dtype('O'),
    'trn_cy': np.dtype('int64'),
    'trn_cy_month': np.dtype('O'),
    'posted_dt': np.dtype('O'),
    'post_fy': np.dtype('float64'),
    'post_fy_month': np.dtype('O'),
    'post_cy': np.dtype('float64'),
    'post_cy_month': np.dtype('O'),
    'ps_sol': np.dtype('O'),
    'res_ps_sol': np.dtype('O'),
    'sum_ps_sol': np.dtype('O'),
    'gl_no': np.dtype('O'),
    'gl_natural': np.dtype('int64'),
    'gl_sub_dept': np.dtype('int64'),
    'appeal': np.dtype('O'),
    'source_id': np.dtype('float64'),
    'source_name': np.dtype('O'),
    'notes': np.dtype('O'),
    'fund_super_grp': np.dtype('O'),
    'fund_category': np.dtype('O'),
    'fund_sub_cate': np.dtype('O'),
    'fund_type': np.dtype('O'),
    'fund_flag_1': np.dtype('O'),
    'fund_flag_2': np.dtype('O'),
    'fund_flag_3': np.dtype('O'),
    'fund_flag_4': np.dtype('O'),
    'fund_flag_5': np.dtype('O'),
    'budget_this_yr': np.dtype('float64'),
    'budget_last_yr': np.dtype('float64'),
    'mgmt_this_yr': np.dtype('O'),
    'mgmt_last_yr': np.dtype('O'),
    'board_flag': np.dtype('int64'),
    'vol_flag': np.dtype('int64'),
    'sym100_flag': np.dtype('int64'),
    'ps_tribute': np.dtype('O'),
    'ps_honorarium': np.dtype('O')
}


# Known group sales IDs
group_sales_ids = [
    44417
]


# Known internal IDs
internal_ids = [
    0,                 # Unknown IDs
    2700674,           # Terry Dwyer
    955085,            # PSO Comps
    3141490,           # Symphony Shop
    91013,             # PSO Orchestra Members
    118401,            # PSO Prez - JF
    91006,             # PSO Artist Comps
    3328612,           # Development Guest
    925728,            # Kurt Mortenson (Internal)
    2010347,           # Goldstar
    2437127,           # Lorraine Caukin (Internal)
    2515897,           # Gregory Pierre Cox (internal)
    3080718,           # Gary Good
    91015,             # PSO Press
    120696             # Carl St. Clair
]


price_type_group_mapper = {
    'Subscription': 'Subscription',
    'Single ': 'Single',
    'Flex': 'Subscription',
    'Discount': 'Single',
    'Comp': 'Comp'
}

# Sub package definitions
pkg_definitions = {
    'PS 2019 Summer': 3,
    '19-20 Connections': 4,
    'Pops Fri 7': 7,
    'Pops Sat 7': 7,
    'Clx Thu 12': 12,
    'Clx Sat 12': 12,
    'Clx Fri 12': 12,
    '19-20 Family 10:00am': 5,
    'Clx Sat Romantic 6': 6,
    'PS 19-20 Pops CYO 4': 4,
    '19-20 Family 11:30am': 5,
    'Clx Thu Romantic 6': 6,
    'Clx Fri Romantic 6': 6,
    '19-20 Cafe Ludwig': 3,
    'Clx Thu Escapes 6': 6,
    'PS 19-20 Flex 4A': 4,
    'Clx Sat Escapes 6': 6,
    'PS 19-20 Flex 4B Lux': 4,
    'PS 19-20 Pedals and Pipes': 3,
    'Clx Fri Escapes 6': 6,
    'PS 19-20 Flex 3A': 3,
    'PS 19-20 Classics CYO 6': 6
}


donor_tier_mapper = {
    '1': (1.0, 99.99),
    '2': (100.0, 299.99),
    '3': (300.0, 499.99),
    '4': (500.0, 999.99),
    '5': (1000.0, 2499.99),
    '6': (2500.0, 4999.99),
    '7': (5000.0, 9999.99),
    '8': (10000.0, 19999.99),
    '9': (20000.0, 29999.99),
    '10': (30000.0, 49999.99),
    '11': (50000.0, 99999.99),
    '12': (100000.0, math.inf)
}

concert_mapper_fy20 = {
    '7/4/2019 20:00': 'PS Hotel California',
    '8/17/2019 20:00': 'PS Star Wars in Concert',
    '9/7/2019 20:00': 'PS Tchaikovsky Spectacular',
    '9/26/2019 20:00': 'Carmina Burana',
    '9/27/2019 20:00': 'Carmina Burana',
    '9/28/2019 20:00': 'Carmina Burana',
    '9/29/2019 15:00': 'O Fortuna',
    '10/17/2019 20:00': "Tchaikovsky's Pathetique",
    '10/18/2019 20:00': "Tchaikovsky's Pathetique",
    '10/19/2019 10:00': 'Dia de los Muertos Celebration',
    '10/19/2019 11:30': 'Dia de los Muertos Celebration',
    '10/19/2019 20:00': "Tchaikovsky's Pathetique",
    '10/27/2019 15:00': 'Beethoven & Brahms',
    '11/1/2019 20:00': 'Sondheim & Lloyd Webber',
    '11/2/2019 20:00': 'Sondheim & Lloyd Webber',
    '11/14/2019 20:00': 'Rhapsody in Blue',
    '11/15/2019 20:00': 'Rhapsody in Blue',
    '11/16/2019 20:00': 'Rhapsody in Blue',
    '12/5/2019 20:00': "Beethoven's Seventh",
    '12/6/2019 20:00': "Beethoven's Seventh",
    '12/7/2019 10:00': 'Nutcracker for Kids',
    '12/7/2019 11:30': 'Nutcracker for Kids',
    '12/7/2019 20:00': "Beethoven's Seventh",
    '12/17/2019 19:30': 'Holiday Organ Spectacular',
    '12/20/2019 20:00': 'Christmas w/ Marie Osmond',
    '12/21/2019 20:00': 'Christmas w/ Marie Osmond',
    '1/16/2020 20:00': "Beethoven's Violin Concerto",
    '1/17/2020 20:00': "Beethoven's Violin Concerto",
    '1/18/2020 10:00': 'Opera for Kids: Elixir of Love',
    '1/18/2020 11:30': 'Opera for Kids: Elixir of Love',
    '1/18/2020 20:00': "Beethoven's Violin Concerto",
    '2/6/2020 20:00': 'Lefèvre Plays Ravel',
    '2/7/2020 20:00': 'Lefèvre Plays Ravel',
    '2/8/2020 20:00': 'Lefèvre Plays Ravel',
    '2/9/2020 15:00': "Ravel's Piano Concerto",
    '2/14/2020 20:00': "Valentine's with Chris Botti",
    '2/15/2020 20:00': "Valentine's with Chris Botti",
    '2/16/2020 15:00': 'Janácek & Schumann',
    '2/27/2020 20:00': 'Hadlich Plays Paganini',
    '2/28/2020 20:00': 'Hadlich Plays Paganini',
    '2/29/2020 10:00': 'Peter and the Wolf',
    '2/29/2020 11:30': 'Peter and the Wolf',
    '2/29/2020 20:00': 'Hadlich Plays Paganini',
    '3/1/2020 15:00': 'Organ Superstar David Higgs',
    '3/13/2020 20:00': 'Pink Martini',
    '3/14/2020 20:00': 'Pink Martini',
    '3/19/2020 20:00': "Beethoven's Piano Concertos",
    '3/20/2020 20:00': "Beethoven's Piano Concertos",
    '3/21/2020 20:00': "Beethoven's Piano Concertos",
    '3/22/2020 15:00': "Beethoven's Emperor",
    '4/3/2020 20:00': 'The Texas Tenors',
    '4/4/2020 20:00': 'The Texas Tenors',
    '4/23/2020 20:00': 'Otello',
    '4/25/2020 20:00': 'Otello',
    '4/28/2020 20:00': 'Otello',
    '5/1/2020 20:00': 'Music of the Rolling Stones',
    '5/2/2020 20:00': 'Music of the Rolling Stones',
    '5/7/2020 20:00': 'Yang Plays Rachmaninoff',
    '5/8/2020 20:00': 'Yang Plays Rachmaninoff',
    '5/9/2020 20:00': 'Yang Plays Rachmaninoff',
    '5/10/2020 15:00': "Beethoven's Razumovsky Quartet",
    '5/10/2020 19:00': 'The Hunchback of Notre Dame',
    '5/28/2020 20:00': 'Tao Plays Mozart',
    '5/29/2020 20:00': 'Tao Plays Mozart',
    '5/30/2020 10:00': 'John Williams: Maestro of the',
    '5/30/2020 11:30': 'John Williams: Maestro of the',
    '5/30/2020 20:00': 'Tao Plays Mozart',
    '5/31/2020 15:00': "Brahms' Symphony No. 4",
    '6/5/2020 20:00': 'Star Wars vs. Star Trek',
    '6/6/2020 20:00': 'Star Wars vs. Star Trek',
    '6/11/2020 20:00': 'Symphony of a Thousand',
    '6/12/2020 20:00': 'Symphony of a Thousand',
    '6/13/2020 20:00': 'Symphony of a Thousand'
}


cached_dtypes = {
    'ticket': {
        'perf_code':               object,
        'perf_no':               np.int64,
        'perf_dt':                 object,
        'zone_no':               np.int64,
        'zone_desc':               object,
        'section':                 object,
        'row':                     object,
        'seat':                  np.int64,
        'home_price':          np.float64,
        'paid_amt':            np.float64,
        'fee_amt':             np.float64,
        'seat_status':           np.int64,
        'seat_status_desc':        object,
        'customer_no':         np.float64,
        'order_no':            np.float64,
        'order_dt':                object,
        'price_type_group_id': np.float64,
        'price_type_group':        object,
        'pd_up':                   object,
        'season':                np.int64,
        'season_desc':             object,
        'summary_cust_id':     np.float64,
        'summary_cust_name':       object,
        'attended':                object,
        'dow':                     object,
        'series':                  object,
        'fy':                    np.int64,
        'price_zone':              object,
    },
    'donor': {}
}
