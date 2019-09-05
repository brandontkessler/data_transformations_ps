import numpy as np

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
