import json
import faiss
import numpy as np
from book import get_lines, BOOKS
from pathlib import Path


book_path = Path("split/out")



def init_index(embeddings):
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings))
    return index


def find_similar_for_verse(verse, data, index, k=10):
    # k nearest neighbours
    ids = data["ids"]
    idx = ids.index(verse)
    embedding = data["embeddings"][idx]
    _, I = index.search(np.array([embedding]), k)
    # Now find the content IDs for the results
    return [ids[ix] for ix in I[0]]

def test():
    #setup
    book_verses = dict(get_lines(book_path / BOOKS[10]))
    with open('embeddings.json') as f:
        data = json.load(f)
    index = init_index(data['embeddings'])
    target = '2:37'
    print(book_verses[target])
    print('='*50)
    similar_verses = find_similar_for_verse(target, data, index)
    for verse in similar_verses:
        print(book_verses[verse])
        print('-'*50)

#TODO alternate verses from two books
def book_dialog(book_idx_1, book_idx_2):
    book_indices = [book_idx_1, book_idx_2]
    files = [f'embeddings-{idx}.json' for idx in book_indices]
    embeddings = [json.load(open(file)) for file in files]
    book_titles = [BOOKS[book_idx_1], BOOKS[book_idx_2]]
    texts = [get_lines(book_path / bt) for bt in book_titles]
    current_verse = "1:1"
    current_book = 0

test()
