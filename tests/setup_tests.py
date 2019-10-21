import os
from etl.data_type import DataFactory

class SetupTests:
    def __init__(self):
        self.this_dir = os.path.dirname(os.path.abspath(__file__))

    def prep_test_data(self):
        self.factory = DataFactory()

        self.ticket = self.factory.create_data_type('ticket')
        self.donor = self.factory.create_data_type('donor')
        self.subscriber = self.factory.create_data_type('subscriber')
        self.mode_of_sale = self.factory.create_data_type('mode_of_sale')

        self.fp_ticket = os.path.join(self.this_dir, 'test_data/ticket/')
        self.fp_donor = os.path.join(self.this_dir, 'test_data/donor/')
        self.fp_subscriber = os.path.join(self.this_dir, 'test_data/sub/')
        self.fp_mode_of_sale = os.path.join(self.this_dir, 'test_data/mode_of_sale/')

        self.ticket.get_data(fys=[19, 20], path=self.fp_ticket)
        self.donor.get_data(fys=13, path=self.fp_donor)
        self.subscriber.get_data(fys=[19, 20], path=self.fp_subscriber)
        self.mode_of_sale.get_data(fys=20, path=self.fp_mode_of_sale, qtr=1)
