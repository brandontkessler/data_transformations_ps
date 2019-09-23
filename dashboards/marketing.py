from .. import Subscriptions, Tickets

def mktg_builder(fy, to_date):
    MARKETING_GOAL = 3250389 + 2754275

    subs = Subscriptions(fy=fy)
    tix = Tickets(fys=[num for num in range(fy-1,fy+1)])

    to_date = tix._date_convert(to_date)

    # Plot Data
    tix.returning_singles_plt(to_date=to_date, fys=[fy])

    # Do everything else
    tix.keep_paid(inplace=True)
    tix.transform_price_type_group(inplace=True)

    three_concerts_cy_and_py = tix.minimum_purchases(
        series=['Classics', 'Pops', 'Summer'],
        fys=[fy-1, fy]
    )

    cy_data = tix.filter_fys(fys=[fy])
    revenue_td = cy_data.paid_amt.sum()
    tix_sold_td = cy_data.paid_amt.count()
    households_td = len(cy_data.summary_cust_id.drop_duplicates())

    clx_pops = tix.filter_series(data=cy_data, series=['Classics', 'Pops'])
    to_date = tix.filter_perf_dt(to_date=to_date, data=clx_pops)

    avg_tickets_per_concert_td = to_date.perf_dt.count() / len(to_date.perf_dt.drop_duplicates())

    kpis = {
        'capacity sold': round(avg_tickets_per_concert_td / tix.CAPACITY * 100, 1),
        '% of goal': round(revenue_td / MARKETING_GOAL * 100, 1),
        'prospects': three_concerts_cy_and_py,
        'households': households_td,
        'total subs': subs.total_pkgs,
        'tickets_sold': tix_sold_td
    }

    return kpis


def sub_builder(fy):
    '''Builds subscription dashboard KPIs

    Excluding the AB Experiment plot - This must get pulled separately
    '''
    subs = Subscriptions(fy=fy)
    tix = Tickets(fys=[num for num in range(fy-1,fy+1)])

    tix.transform_price_type_group(inplace=True)
    tix.keep_paid(inplace=True)

    three_concerts_cy_and_py = tix.minimum_purchases(
        series=['Classics', 'Pops', 'Summer']
    )

    three_concerts_cy = tix.minimum_purchases(
        series=['Classics', 'Pops', 'Summer'],
        fys=[fy]
    )

    kpis = {
        'total subs': subs.total_pkgs,
        'seats per sub': subs.avg_seats_per_pkg(),
        'retention': subs.retention(),
        'new': subs.new(),
        'three_concerts_current_and_py': three_concerts_cy_and_py,
        'three_concerts_current': three_concerts_cy
    }

    return kpis


def single_builder(fy, to_date):
    '''Builds single ticket dashboard KPIs
    '''
    SINGLE_GOAL = 2754275
    TICKETMASTER_REV = 178420.5
    TICKETMASTER_TIX = 4703

    tix = Tickets(fys=[num for num in range(fy-3,fy+1)])

    tix.keep_paid(inplace=True)
    tix.transform_price_type_group(inplace=True)

    three_concerts_cy_and_py = tix.minimum_purchases(
        series=['Classics', 'Pops', 'Summer'],
        fys=[fy-1, fy]
    )

    data = tix.data.copy()

    data = tix.filter_fys(fys=[fy], data=data)
    data = tix.drop_sub_sales(data=data)

    revenue_td, tix_sold_td = data.aggregate({'paid_amt': ['sum', 'count']}).paid_amt
    households_td = len(set(data.summary_cust_id))

    new_to_file, retained_new = tix.new_to_file(fy=fy, data=tix.data.copy())

    kpis = {
        '%_to_goal': round((revenue_td + TICKETMASTER_REV) / SINGLE_GOAL * 100, 1),
        'tickets sold': tix_sold_td + TICKETMASTER_TIX,
        'households': households_td,
        'new_to_file': len(new_to_file),
        'retained_new_to_file': len(retained_new),
        'three_concerts_current_and_py': three_concerts_cy_and_py
    }

    # Build plots
    tix.plot_singles_by_zone(to_date=to_date, fys=[fy])

    return kpis
