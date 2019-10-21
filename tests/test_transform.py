import unittest
import datetime as dt
from etl import transform

class TestTransform(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_date_convert(self):
        conv = transform.date_convert('11-12-2019')
        self.assertIsInstance(conv, dt.date)

        conv2 = transform.date_convert('November 5, 2013')
        self.assertIsInstance(conv2, dt.date)
