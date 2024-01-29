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
    faiss_index: faiss.IndexFlatL2

book_path = Path("split/out")



def build_faiss_index(embeddings):
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings))
    return index

def verse_id_to_embedding(data, verse_id):
    verse_index = verse_id_to_index(data, verse_id )
    return data["embeddings"][verse_index]

def verse_id_to_index(data, verse_id):
    return data['ids'].index(verse_id)

def verse_index_to_id(data, verse_index):
    return data["ids"][verse_index]

def find_similar_verse_ids(data: EmbeddingData, embedding, k=10):
    faiss_index: faiss.IndexFlatL2 = data['faiss_index']
    _, I = faiss_index.search(np.array([embedding]), k)
    return [verse_index_to_id(data, ix) for ix in I[0]]

def get_or_create_embeddings(book_index) -> EmbeddingData:
    embeddings_path = Path(f'embeddings/embeddings-{book_index}.json')
    if not embeddings_path.exists():
        model = get_model()
        save_embeddings_to_json(book_index, model)
    with open(embeddings_path) as file:
        data = json.load(file)
        data['faiss_index'] = build_faiss_index(data['embeddings'])
        return data

def find_next_verse_id(verse1_id, data1, data2):
    embedding = verse_id_to_embedding(data1, verse1_id)
    [ verse2_id ] = find_similar_verse_ids(data2, embedding, 1)
    verse2_index = verse_id_to_index(data2, verse2_id)
    verse2_ids = data2['ids']
    if  verse2_index + 1 >= len(verse2_ids):
        return None
    return verse2_ids[verse2_index+1]

#TODO alternate verses from two books
def book_dialog(book_idx_1, book_idx_2):
    book_indices = [book_idx_1, book_idx_2]
    data_list = [get_or_create_embeddings(idx) for idx in book_indices]
    book_titles = [BOOKS[book_idx_1], BOOKS[book_idx_2]]
    texts = [dict(get_lines(book_path / bt)) for bt in book_titles]
    verse1_id = "1:1"
    verse1 = texts[0][verse1_id]
    print(f'{verse1_id} {verse1}')
    verse2_id = find_next_verse_id(verse1_id, *data_list)
    verse2 = texts[1][verse2_id]
    print(f'{verse2_id} {verse2}')

# choosing first and last index
# genesis vs apocalypse
book_dialog(0, 66)
