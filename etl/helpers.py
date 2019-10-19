import numpy as np
import math

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
