import unittest
import datetime as dt
from etl.data_prep import PrepDataFactory, PrepTicketData
from tests.setup_tests import SetupTests

class TestDataPrep(unittest.TestCase):
    def setUp(self):
        self.setup = SetupTests()
        self.setup.prep_test_data()
        self.tdata = self.setup.ticket.raw
        self.ddata = self.setup.donor.raw
        self.sdata = self.setup.subscriber.raw
        self.mosdata = self.setup.mode_of_sale.raw

        self.prep_factory = PrepDataFactory()

    def tearDown(self):
        pass

    def test_prep_tickets(self):
        prep = PrepTicketData()
        prepared_data = prep.prepare_data(self.tdata, full=True)

        self.assertTrue(isinstance(prepared_data['perf_dt'][0], dt.date))
        self.assertTrue(isinstance(prepared_data['order_dt'][0], dt.date))
