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

        tmp_path = Path('tests/tmp/data-test.mpk')
        save_data(data, tmp_path)
        data_2 = data_from_file(tmp_path)
        self.assertEqual(len(data_2.embeddings), 10)

    def test_faiss_index(self):
        data_path = Path('tests/data-test.mpk')
        data = data_from_file(data_path)
        self.assertEqual(len(data.embeddings), 10)
        self.assertIsNone(data.faiss_index)
        data.initialize_faiss()
        self.assertIsNotNone(data.faiss_index)

        emb = data.embeddings[8]
        verse_id = data.verse_index_to_id(8)
        found_verse_ids = data.find_similar_verse_ids(emb, 1)
        self.assertEqual(1, len(found_verse_ids))
        self.assertEqual(verse_id, found_verse_ids[0])
