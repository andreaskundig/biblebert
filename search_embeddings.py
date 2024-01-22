import json
import faiss
import numpy as np
from book import get_lines, BOOKS
from pathlib import Path
from make_embeddings import get_model, save_embeddings_to_json
from typing import List, TypedDict

class EmbeddingData(TypedDict):
    ids: List[int]
    embeddings: List[List[float]]

book_path = Path("split/out")



def index_from_embeddings(embeddings):
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
    index = index_from_embeddings(data['embeddings'])
    target = '2:37'
    print(book_verses[target])
    print('='*50)
    similar_verses = find_similar_for_verse(target, data, index)
    for verse in similar_verses:
        print(book_verses[verse])
        print('-'*50)

def get_or_create_embeddings(book_index) -> EmbeddingData:
    embeddings_path = Path(f'embeddings/embeddings-{book_index}.json')
    if not embeddings_path.exists():
        model = get_model()
        save_embeddings_to_json(book_index, model)
    with open(embeddings_path) as file:
        return json.load(file)


#TODO alternate verses from two books
def book_dialog(book_idx_1, book_idx_2):
    book_indices = [book_idx_1, book_idx_2]
    data_list = [get_or_create_embeddings(idx) for idx in book_indices]
    indices = [index_from_embeddings(data['embeddings']) for data in data_list]
    book_titles = [BOOKS[book_idx_1], BOOKS[book_idx_2]]
    texts = [dict(get_lines(book_path / bt)) for bt in book_titles]
    # >>> texts[0]['1:1']
    # 'In the beginning God created the heaven and the earth.'
    target = "1:1" # list(texts[0].keys())[0]
    index = indices[1]
    data = data_list[0]
    current_book = 0
    similar_verses = find_similar_for_verse(target, data, index, 1)
    # >>> similar_verses
    # ['14:20']
    # TODO find index of 14:21 and search in genesis
    print(texts[1][similar_verses[0]])

# choosing first and last index
# genesis vs apocalypse
book_dialog(0, 66)
