import os
import unittest

from etl.data_import import (ImportData, TicketImportStrategy,
    DonorImportStrategy, SubscriberImportStrategy, ModeOfSaleImportStrategy)
from etl.helpers import ticketing_dtype, donor_dtype

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestImportData(unittest.TestCase):
    def setUp(self):
        self.importer = ImportData()
        self.fp_ticket = os.path.join(THIS_DIR, 'test_data/ticket/')
        self.fp_donor = os.path.join(THIS_DIR, 'test_data/donor/')
        self.fp_subscriber = os.path.join(THIS_DIR, 'test_data/sub/')
        self.fp_mode_of_sale = os.path.join(THIS_DIR, 'test_data/mode_of_sale/')

    def tearDown(self):
        pass

    def test_send_data(self):
        tdata20 = self.importer.send_data(type='ticket', fys=20,
            path=self.fp_ticket)
        self.assertEqual(len(tdata20), 67)

        tdata_all = self.importer.send_data(type='ticket', fys=[19, 20],
            path=self.fp_ticket)
        self.assertEqual(len(tdata_all), 111)

        ddata = self.importer.send_data(type='donor', fys=13,
            path=self.fp_donor)
        self.assertEqual(len(ddata), 128)

        sdata20 = self.importer.send_data(type='subscriber', fys=20,
            path=self.fp_subscriber)
        self.assertEqual(len(sdata20), 30)

        sdata = self.importer.send_data(type='subscriber', fys=[19, 20],
            path=self.fp_subscriber)
        self.assertEqual(len(sdata), 88)

        mosdata = self.importer.send_data(type='mode_of_sale', fys=20, qtr=1,
            path=self.fp_mode_of_sale)
        self.assertEqual(len(mosdata), 26)

class TestTicketImportStrategy(unittest.TestCase):
    def setUp(self):
        self.ticket = TicketImportStrategy()
        self.fp = os.path.join(THIS_DIR, 'test_data/ticket/')

    def tearDown(self):
        pass

    def test_get_data(self):
        t20 = self.ticket.get_data(fys=20, path=self.fp, dtype=ticketing_dtype)
        self.assertEqual(len(t20), 67)

        t19 = self.ticket.get_data(fys=19, path=self.fp, dtype=ticketing_dtype)
        self.assertEqual(len(t19), 44)

        all = self.ticket.get_data(fys=[19, 20], path=self.fp, dtype=ticketing_dtype)
        self.assertEqual(len(all), 111)

    def test_import_data(self):
        t20 = self.ticket.import_file(fy=20, dtype=ticketing_dtype, path=self.fp)
        self.assertEqual(len(t20), 67)


class TestDonorImportStrategy(unittest.TestCase):
    def setUp(self):
        self.donor = DonorImportStrategy()
        self.fp = os.path.join(THIS_DIR, 'test_data/donor/')

    def tearDown(self):
        pass

    def test_get_data(self):
        data = self.donor.get_data(fys='13', path=self.fp, dtype=donor_dtype)
        self.assertEqual(len(data), 128)

        data2 = self.donor.get_data(fys=13, path=self.fp, dtype=donor_dtype)
        self.assertEqual(len(data2), 128)


class TestSubscriberImportStrategy(unittest.TestCase):
    def setUp(self):
        self.sub = SubscriberImportStrategy()
        self.fp = os.path.join(THIS_DIR, 'test_data/sub/')

    def tearDown(self):
        pass

    def test_get_data(self):
        data = self.sub.get_data(fys=19, path=self.fp, dtype=None)
        self.assertEqual(len(data), 58)

        data2 = self.sub.get_data(fys=[19, 20], path=self.fp, dtype=None)
        self.assertEqual(len(data2), 88)

class TestModeOfSaleImportStrategy(unittest.TestCase):
    def setUp(self):
        self.mos = ModeOfSaleImportStrategy()
        self.fp = os.path.join(THIS_DIR, 'test_data/mode_of_sale/')

    def tearDown(self):
        pass

    def test_get_data(self):
        data = self.mos.get_data(fys=20, path=self.fp, qtr=1)
        self.assertEqual(len(data), 26)
