import os
import unittest

import datetime as dt
import pandas as pd

from etl.data_import import (ImportData, TicketImportStrategy,
    DonorImportStrategy, SubscriberImportStrategy, PrepData)
from etl.helpers import ticketing_dtype, donor_dtype

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestImportData(unittest.TestCase):
    def setUp(self):
        self.importer = ImportData()
        self.fp_ticket = os.path.join(THIS_DIR, 'test_data/ticket/')
        self.fp_donor = os.path.join(THIS_DIR, 'test_data/donor/')
        self.fp_subscriber = os.path.join(THIS_DIR, 'test_data/sub/')

    def tearDown(self):
        pass

    def test_send_data(self):
        tdata20 = self.importer.send_data(type='ticket', fys=20, path=self.fp_ticket)
        self.assertEqual(len(tdata20), 67)

        tdata_all = self.importer.send_data(type='ticket', fys=[19, 20], path=self.fp_ticket)
        self.assertEqual(len(tdata_all), 111)

        ddata = self.importer.send_data(type='donor', fys=13, path=self.fp_donor)
        self.assertEqual(len(ddata), 128)

        sdata20 = self.importer.send_data(type='subscriber', fys=20, path=self.fp_subscriber)
        self.assertEqual(len(sdata20), 30)

        sdata = self.importer.send_data(type='subscriber', fys=[19, 20], path=self.fp_subscriber)
        self.assertEqual(len(sdata), 88)


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



class TestPrepData(unittest.TestCase):
    def setUp(self):
        self.prep = PrepData()

    def tearDown(self):
        pass

    def test_date_convert(self):
        conv = self.prep.date_convert('11-12-2019')
        self.assertIsInstance(conv, dt.date)

        conv2 = self.prep.date_convert('November 5, 2013')
        self.assertIsInstance(conv2, dt.date)
