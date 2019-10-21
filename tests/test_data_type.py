import os
import unittest

from etl.data_type import (DataFactory, PSData, Ticket, Donor, Subscriber,
    ModeOfSale)
from etl.exception import UnexpectedDataType


THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestDataFactory(unittest.TestCase):
    def setUp(self):
        self.factory = DataFactory()

    def tearDown(self):
        pass

    def test_create_data_type(self):
        t = self.factory.create_data_type('ticket')
        self.assertEqual(t.type._type, 'ticket')

        d = self.factory.create_data_type('donor')
        self.assertEqual(d.type._type, 'donor')

        s = self.factory.create_data_type('subscriber')
        self.assertEqual(s.type._type, 'subscriber')

        mos = self.factory.create_data_type('mode_of_sale')
        self.assertEqual(mos.type._type, 'mode_of_sale')

        with self.assertRaises(UnexpectedDataType):
            self.factory.create_data_type('bad_type')


class TestPSData(unittest.TestCase):
    def setUp(self):
        self.ticket = PSData(Ticket)
        self.donor = PSData(Donor)
        self.subscriber = PSData(Subscriber)
        self.mode_of_sale = PSData(ModeOfSale)
        self.fp_ticket = os.path.join(THIS_DIR, 'test_data/ticket/')
        self.fp_donor = os.path.join(THIS_DIR, 'test_data/donor/')
        self.fp_subscriber = os.path.join(THIS_DIR, 'test_data/sub/')
        self.fp_mode_of_sale = os.path.join(THIS_DIR, 'test_data/mode_of_sale/')

    def tearDown(self):
        pass

    def test_get_data(self):
        self.ticket.get_data(fys=19, path=self.fp_ticket)
        self.assertEqual(len(self.ticket.raw), 44)

        self.ticket.get_data(fys=[20, 19], path=self.fp_ticket)
        self.assertEqual(len(self.ticket.raw), 111)

        self.donor.get_data(fys=13, path=self.fp_donor)
        self.assertEqual(len(self.donor.raw), 128)

        self.subscriber.get_data(fys=20, path=self.fp_subscriber)
        self.assertEqual(len(self.subscriber.raw), 30)

        self.subscriber.get_data(fys=[19, 20], path=self.fp_subscriber)
        self.assertEqual(len(self.subscriber.raw), 88)

        self.mode_of_sale.get_data(fys=20, path=self.fp_mode_of_sale, qtr=1)
        self.assertEqual(len(self.mode_of_sale.raw), 26)
