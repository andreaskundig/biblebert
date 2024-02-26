#!/usr/bin/env python3
import unittest
from pathlib import Path
from data import data_from_file, data_from_book, save_data
from data import data_from_json
from make_embeddings import get_model

MODEL = get_model()

class TestData(unittest.TestCase):
    def test_data_from_json(self):
        data = data_from_json(Path('embeddings/embeddings-0.json'))
        self.assertIsNotNone(data)
        self.assertEqual(len(data.ids), 1533)
        self.assertEqual(len(data.ids), len(data.embeddings))

    def test_data_from_book_lines(self):
        book_path = Path('tests/test-book.txt')
        data = data_from_book(book_path, MODEL)
        self.assertEqual(len(data.embeddings), 10)

        save_data(data, Path('tests/data-test.bin'))
        data_2 = data_from_file(Path('tests/data-test.bin'))
        self.assertEqual(len(data_2.embeddings), 10)
