import numpy as np

bad_ids = [
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
