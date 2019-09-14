import math

price_type_group_mapper = {
    'Subscription': 'Subscription',
    'Single ': 'Single',
    'Flex': 'Subscription',
    'Discount': 'Single',
    'Comp': 'Comp'
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
