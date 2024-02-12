import unittest
import json
import numpy as np
from pathlib import Path
# from make_embeddings import get_model
from search_embeddings import build_faiss_index

class TestSum(unittest.TestCase):

    def test_search(self):
        embeddings0_path = Path('embeddings/embeddings-0.json')
        embeddings1_path = Path('embeddings/embeddings-66.json')
        # model = get_model()

        with open(embeddings0_path) as f0, open(embeddings1_path) as f1:
            data0 = json.load(f0)
            embeddings0 =  data0['embeddings']
            faiss_index0 = build_faiss_index(embeddings0)
            embedding0_index = 15
            embedding0 = embeddings0[embedding0_index]
            [D00], [I00] = faiss_index0.search(np.array([embedding0]), 5)

            self.assertEqual(embedding0_index, I00[0])
            self.assertEqual(0, D00[0])
            # print(f'I {I0}')
            # print(f'D {D0}')

            _, [I01] = faiss_index0.search(np.array([embedding0]), 5)
            self.assertListEqual(list(I00), list(I01))

            data1 = json.load(f1)
            embeddings1 =  data1['embeddings']
            embedding1 = embeddings1[5]

            _, [I10] = faiss_index0.search(np.array([embedding1]), 5)
            _, [I11] = faiss_index0.search(np.array([embedding1]), 5)
            self.assertListEqual(list(I10), list(I11))

    def test_list_int(self):
        """
        Test that it can sum a list of integers
        """
        data = [1, 2, 3]
        result = sum(data)
        self.assertEqual(result, 6)

if __name__ == '__main__':
    unittest.main()
