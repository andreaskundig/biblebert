#!/usr/bin/env python3
import unittest
from pathlib import Path
from data import data_from_file

class TestData(unittest.TestCase):
    def test_data_from_file(self):
        data = data_from_file(Path('embeddings/embeddings-0.json'))
        self.assertIsNotNone(data)
        self.assertEqual(len(data.ids), 1533)
        self.assertEqual(len(data.ids), len(data.embeddings))
