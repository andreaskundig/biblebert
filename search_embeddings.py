import json
import itertools
import faiss
import numpy as np
from book import get_lines, BOOKS
from pathlib import Path
from make_embeddings import get_model, save_embeddings_to_json
from typing import List, TypedDict, Dict
from data import build_faiss_index, Data

class EmbeddingData(TypedDict):
    ids: List[int]
    embeddings: List[List[float]]
    faiss_index: faiss.IndexFlatL2
    title: str
    verses: Dict[str, str]

book_path = Path("split/out")

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

def find_similar_verse_indices(verse1_id, data1, data2, k=1):
    embedding = verse_id_to_embedding(data1, verse1_id)
    verse2_ids = find_similar_verse_ids(data2, embedding, k)
    return [verse_id_to_index(data2, id) for id in verse2_ids]

def find_next_verse_ids(verse1_id, data1, data2, k=1):
    v2_indices = find_similar_verse_indices(verse1_id, data1, data2, k)
    verse2_ids = data2['ids']
    v2_count = len(verse2_ids)
    return [verse2_ids[idx+1] for idx in v2_indices
                        if idx+1 < v2_count]

def print_verse(data, verse_id):
    print(f'{verse_id} {verseid_to_verse(data, verse_id)}')

def verseid_to_verse(data, verse_id):
    return data['verses'][verse_id]

def ping_pong(verse1_id, data_1, data_2, k=10):
    data_list = [data_1, data_2]
    verse_id = verse1_id
    consumed_verses = [{verse_id}, set()]
    idx1, idx2 = 0, 1
    while True:
        verse = verseid_to_verse(data_list[idx1], verse_id)
        yield verse_id, verse
        verse_ids = find_next_verse_ids(verse_id, data_list[idx1],
                                        data_list[idx2], k)
        valid_ids = list(set(verse_ids) - consumed_verses[idx2])
        if len(valid_ids) == 0:
            return
        verse_id = valid_ids[0]
        consumed_verses[idx2].add(verse_id)
        idx1, idx2 = idx2, idx1

def ping_pong1(verse1_id:str, data_1: Data, data_2: Data, k=10):
    datas = [data_1, data_2]
    src_idx, tgt_idx = 0, 1
    verse_id = verse1_id
    consumed_verses = [{verse_id}, set()]
    while True:
        source, target = datas[src_idx], datas[tgt_idx]
        target_consumed = consumed_verses[tgt_idx]
        yield verse_id, source.verse_id_to_index(verse_id), 0
        try:
            next_verse_id = source.next_verse_id(verse_id)
        except:
            return
        searched_embedding = source.embedding_for_verse_id(next_verse_id)
        target_verse_ids = target.find_similar_verse_ids(
            searched_embedding, 5)
        valid_target_ids = list(set(target_verse_ids) - target_consumed)
        if len(valid_target_ids) == 0:
            return
        verse_id = valid_target_ids[0]
        target_consumed.add(verse_id)
        src_idx, tgt_idx = tgt_idx, src_idx

def init_data(book_idx_1, book_idx_2):
    book_indices = [book_idx_1, book_idx_2]
    return [get_or_create_embeddings(idx) for idx in book_indices]

#TODO alternate verses from two books
def book_dialog(book_idx_1, book_idx_2):

    data_list = init_data(book_idx_1, book_idx_2)

    generator = ping_pong('1:1', data_list[0], data_list[1], 10)
    result = list(itertools.islice(generator, 20))
    for r in result:
        print(f'{r[0]} {r[1]}')

if __name__ == '__main__':
    # choosing first and last index
    # genesis vs apocalypse
    book_dialog(0, 66)
