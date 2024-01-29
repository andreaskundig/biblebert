import json
import faiss
import numpy as np
from book import get_lines, BOOKS
from pathlib import Path
from make_embeddings import get_model, save_embeddings_to_json
from typing import List, TypedDict, Dict

class EmbeddingData(TypedDict):
    ids: List[int]
    embeddings: List[List[float]]
    faiss_index: faiss.IndexFlatL2
    title: str
    verses: Dict[str, str]

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

    book_title = BOOKS[book_index]
    data['title'] = book_title
    data['verses'] = dict(get_lines(book_path / book_title))
    return data

def find_next_verse_id(verse1_id, data1, data2):
    embedding = verse_id_to_embedding(data1, verse1_id)
    [ verse2_id ] = find_similar_verse_ids(data2, embedding, 1)
    verse2_index = verse_id_to_index(data2, verse2_id)
    verse2_ids = data2['ids']
    if  verse2_index + 1 >= len(verse2_ids):
        return None
    return verse2_ids[verse2_index+1]

def print_verse(data, verse_id):
    verse = data['verses'][verse_id]
    print(f'{verse_id} {verse}')

#TODO alternate verses from two books
def book_dialog(book_idx_1, book_idx_2):
    book_indices = [book_idx_1, book_idx_2]
    data_list = [get_or_create_embeddings(idx) for idx in book_indices]

    verse1_id = "1:1"
    print_verse(data_list[0], verse1_id)

    verse2_id = find_next_verse_id(verse1_id, *data_list)
    print_verse(data_list[1], verse2_id)

# choosing first and last index
# genesis vs apocalypse
book_dialog(0, 66)
