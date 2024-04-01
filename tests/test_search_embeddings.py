import unittest
import json
import numpy as np
from pathlib import Path
# from make_embeddings import get_model
from book import Book
from search_embeddings import build_faiss_index
from data import data_from_json, data_from_file

class TestSearch(unittest.TestCase):
    def test_search_json(self):
        # model = get_model()

        #data0 = json.load(f0)
        data0 = data_from_json(Path('embeddings/embeddings-0.json'))
        faiss_index0 = build_faiss_index(data0.embeddings)
        embedding0_index = 15
        embedding0 = data0.embeddings[embedding0_index]
        [D00], [I00] = faiss_index0.search(np.array([embedding0]), 5)

        self.assertEqual(embedding0_index, I00[0])
        self.assertEqual(0, D00[0])
        # print(f'I {I0}')
        # print(f'D {D0}')

        _, [I01] = faiss_index0.search(np.array([embedding0]), 5)
        self.assertListEqual(list(I00), list(I01))

        data1 = data_from_json(Path('embeddings/embeddings-66.json'))
        embedding1 = data1.embeddings[5]

        _, [I10] = faiss_index0.search(np.array([embedding1]), 5)
        _, [I11] = faiss_index0.search(np.array([embedding1]), 5)
        self.assertListEqual(list(I10), list(I11))

    def test_search(self):
        # model = get_model()

        #data0 = json.load(f0)
        book0 = Book(66)
        book0.init_embeddings()
        data0 = book0.data
        embedding0_index = 15
        embedding0 = data0.embeddings[embedding0_index]
        verse_ids_00 = data0.find_similar_verse_ids(embedding0, 5)
        I00 = data0.verse_id_to_index(verse_ids_00[0])
        # _, [I00] = faiss_index0.search(np.array([embedding0]), 5)

        self.assertEqual(embedding0_index, I00)
        # self.assertEqual(0, D00[0])
        # print(f'I {I0}')
        # print(f'D {D0}')

        verse_ids_01 = data0.find_similar_verse_ids(embedding0, 5)
        # _, [I01] = faiss_index0.search(np.array([embedding0]), 5)

        self.assertListEqual(verse_ids_00, verse_ids_01)

        book1 = Book(0)
        book1.init_embeddings()
        data1 = book1.data
        embedding1 = data1.embeddings[5]
        # data1.initialize_faiss()

        verse_ids_10 = data0.find_similar_verse_ids(embedding1, 5)
        verse_ids_11 = data0.find_similar_verse_ids(embedding1, 5)
        self.assertListEqual(verse_ids_10, verse_ids_11)

    def test_ping_pong(self):
        datas = []
        for index in [0,66]:
            book = Book(index)
            book.init_embeddings()
            datas.append(book.data)

        src_idx, tgt_idx = 0, 1
        v_1_1_b0 = "1:1"
        # while True:
        src, tgt = datas[src_idx], datas[tgt_idx]
        assert src is not None and tgt is not None
        verse_idx = src.verse_id_to_index(v_1_1_b0)
        v_1_2_b0 = src.next_verse_id(v_1_1_b0)
        self.assertEqual(v_1_2_b0, "1:2")
        emb_v_1_2_b0 = src.embedding_for_verse_id(v_1_2_b0)
        v_b1 = tgt.find_similar_verse_ids(emb_v_1_2_b0, 5)[0]
        v_b1_again = tgt.find_similar_verse_ids(emb_v_1_2_b0, 5)[0]
        self.assertEqual(v_b1, v_b1_again)

    
if __name__ == '__main__':
    unittest.main()
