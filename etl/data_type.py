from .exception import UnexpectedDataType
from .data_import import ImportData

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
            raise UnexpectedDataType(f'UnexpectedType: type must be: {options}')

class PSData:
    def __init__(self, object):
        self.type = object()
        self.raw = None
        self.working = None

    def get_data(self, fys, path):
        import_data = ImportData()
        self.raw = import_data.send_data(type=self.type._type, fys=fys, path=path)
        self.working = self.raw.copy()
        return self.working


class Ticket:
    def __init__(self):
        self._type = 'ticket'
        self._capacity = 1750

class Donor:
    def __init__(self):
        self._type = 'donor'

class Subscriber:
    def __init__(self):
        self._type = 'subscriber'

class ModeOfSale:
    def __init__(self):
        self._type = 'mode_of_sale'
