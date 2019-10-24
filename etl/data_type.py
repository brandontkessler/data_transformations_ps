from .exception import UnexpectedDataType
from .data_import import ImportData
from .data_prep import PrepDataFactory
from .analysis import TierAnalysis, PreConcertSegmentation
from .plot import PlotFactory
from . import filter, transform

class DataFactory:
    '''Factory used to create the data type necessary for analysis'''

    def __init__(self):
        self._factory_map = {
            'ticket': Ticket,
            'donor': Donor,
            'subscriber': Subscriber,
            'mode_of_sale': ModeOfSale,
            'attribute': Attribute
        }

    def create_data_type(self, type):
        try:
            return PSData(self._factory_map[type])
        except:
            options = list(self._factory_map.keys())
            raise UnexpectedDataType(f'{type} must match one of: {options}')

class PSData:
    prep_factory = PrepDataFactory()

    def __init__(self, object):
        self.type = object()
        self.raw = None
        self.working = None
        self.raw_prior = None
        self.working_prior = None
        self.preparer = self.prep_factory.get_preparer(self.type._type)()


    def get_data(self, fys, path=None, qtr=None):
        '''qtr is only used for ModeOfSale (1, 2, 3, or 4)'''
        importer = ImportData()

        if self.type._type == 'mode_of_sale' and qtr is None:
            raise Exception('qtr arg must contain an integer of 1, 2, 3, or 4.')

        self.raw = importer.send_data(type=self.type._type, fys=fys,
            path=path, qtr=qtr)

        self.working = self.prep_data(self.raw)

        if self.type._type == 'subscriber' and isinstance(fys, int):
            self.raw_prior = importer.send_data(type=self.type._type,
                fys=fys-1, path=path, qtr=qtr)

            self.working_prior = self.prep_data(self.raw_prior)

        return

    def prep_data(self, data, full=True):
        '''prepares data for analysis

        args:
            full -> Boolean. Use True for full prep
        '''
        return self.preparer.prepare_data(data, full)



class Ticket:
    def __init__(self):
        self._type = 'ticket'
        self._capacity = 1750
        self.ticket_plots = PlotFactory('ticket_plots').plotter()
        self.filters = {
            'fys': filter.filter_fys,
            'paid': filter.filter_paid_only,
            'series': filter.filter_by_series,
            'non_subs': filter.filter_non_subs,
            'before_date': filter.filter_before_date,
            'min_transactions': filter.filter_by_minimum_transactions
        }
        self.transform = {
            'price_type_group': transform.transform_price_type_group
        }
        self.pre_concert = PreConcertSegmentation

class Donor:
    def __init__(self):
        self._type = 'donor'
        self.tier_analysis = TierAnalysis()
        self.filters = {
            'fys': filter.filter_fys
        }

    @staticmethod
    def get_box_circle(data, fy=None):
        '''Given the current dataframe, isolate a list of box circle members

        Args:
        fy -- Extract box circle for the given fy only
              default: None
        '''
        tmp = data.copy()

        if fy:
            fy_mask = tmp.fy == fy
            tmp = tmp.loc[fy_mask]

        mask = ['Box Circle' in campaign for campaign in tmp.campaign]
        box = tmp.loc[mask][['summary_cust_id']]

        return list(set(box['summary_cust_id']))

    @staticmethod
    def get_high_cap_prospects(data, fy, attribute_data_path=None):
        '''Categorizes prospects that are NOT current donors

        Capacity Ratings:
        We assume group 3 and lower is 'high capacity': $250,000+ over 5 years

        Args:
        fy - fiscal year of analysis in question
        min_years_of_donating - if provided, exclude donors that haven't donated

        attribute_data_path - path to attribute_data
                              default: '../../data/attribute/'
        '''
        attr = PSData(Attribute)
        attr.get_data(fys=None, path=attribute_data_path)

        mask = attr.working.key_value.map(lambda e: e[:3] in attr.type._high_capacity_group)
        high_cap = attr.working.loc[mask].reset_index(drop=True)

        unique_current_donors = set(self.filters['fys'](data=data, fys=[fy-1, fy])['customer_no'])

        mask_existing_donors = ~high_cap.customer_no.isin(unique_current_donors)
        high_cap = set(high_cap.loc[mask_existing_donors]['customer_no'])

        return high_cap


class Subscriber:
    def __init__(self):
        self._type = 'subscriber'

    @staticmethod
    def get_total_pkgs(data):
        return sum(data['num_seats'])

    # ------------------ summary statistics ----------------
    # def retention(self):
    #     '''Calculate YoY retention of subscribers'''
    #     ids_retained = self.customer_numbers.intersection(self.py_customer_numbers)
    #     retained_subs = len(ids_retained)
    #     total_subs_py = len(self.py_customer_numbers)
    #     return round(retained_subs / total_subs_py * 100, 2)
    #
    # def new(self):
    #     '''Calculate new subscribers (did not subscribe in prior year)'''
    #     new_customers = self.customer_numbers - self.py_customer_numbers
    #     data = self.data.copy()
    #     data = data.loc[data['customer_no'].isin(new_customers)]
    #     return sum(data['num_seats'])
    #
    # def avg_seats_per_pkg(self, definitions=pkg_definitions):
    #     '''Calculate avg seats per pkg'''
    #     data = self.data.copy()
    #     data['seats_per_pkg'] = data['pkg_desc'].map(definitions)
    #     data['total_seats_sold'] = data['seats_per_pkg'] * data['num_seats']
    #     return round(np.sum(data['total_seats_sold']) / self.total_pkgs, 1)



class ModeOfSale:
    def __init__(self):
        self._type = 'mode_of_sale'
        self._qtr = None

class Attribute:
    def __init__(self):
        self._type = 'attribute'
        self._high_capacity_group = ['3 -', '2 -', '1 -']
