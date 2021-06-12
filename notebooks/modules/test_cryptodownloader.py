#!/usr/bin/env python3

import unittest

import cryptodownloader

#run with python -m unittest test_cryptodownloader
class TestCryptoDatasets(unittest.TestCase):

    def test_downloadIntranet1(self):
        df = cryptodownloader.downloadIntraday('BTC', 'USD', 1622332350, 1622512350, minutesAggregate=1)
        self.assertEqual(0, len(df[df.duplicated()]))
        self.assertEqual(4000, len(df))


