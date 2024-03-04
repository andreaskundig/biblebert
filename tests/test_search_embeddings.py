import unittest
import json
import numpy as np
from pathlib import Path
# from make_embeddings import get_model
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
        data0 = data_from_file(Path('embeddings/embeddings-0.mpk'))
        data0.initialize_faiss()
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

        data1 = data_from_file(Path('embeddings/embeddings-40.mpk'))
        embedding1 = data1.embeddings[5]
        # data1.initialize_faiss()

        verse_ids_10 = data0.find_similar_verse_ids(embedding1, 5)
        verse_ids_11 = data0.find_similar_verse_ids(embedding1, 5)
        self.assertListEqual(verse_ids_10, verse_ids_11)


if __name__ == '__main__':
    unittest.main()
