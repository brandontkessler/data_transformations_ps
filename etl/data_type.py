from .exception import UnexpectedDataType
from .data_import import ImportData
from .data_prep import PrepDataFactory
from .analysis import TierAnalysis

class DataFactory:
    '''Factory used to create the data type necessary for analysis'''

    def __init__(self):
        self._factory_map = {
            'ticket': Ticket,
            'donor': Donor,
            'subscriber': Subscriber,
            'mode_of_sale': ModeOfSale
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
        self.preparer = self.prep_factory.get_preparer(self.type._type)()


    def get_data(self, fys, path, qtr=None):
        '''qtr is only used for ModeOfSale (1, 2, 3, or 4)'''
        import_data = ImportData()

        if self.type._type == 'mode_of_sale' and qtr is None:
            raise Exception('qtr arg must contain an integer of 1, 2, 3, or 4.')


        self.raw = import_data.send_data(type=self.type._type, fys=fys,
            path=path, qtr=qtr)

        self.working = self.prep_data(self.raw)

        if self.type._type == 'subscriber':
            self.raw_prior = import_data.send_data(type=self.type._type,
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

class Donor:
    def __init__(self):
        self._type = 'donor'
        self.tier_analysis = TierAnalysis()

class Subscriber:
    def __init__(self):
        self._type = 'subscriber'

class ModeOfSale:
    def __init__(self):
        self._type = 'mode_of_sale'
        self._qtr = None
