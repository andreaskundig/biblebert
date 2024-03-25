from pathlib import Path
import json
import msgpack
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import Any, Union, Optional
from torch import Tensor
from numpy import ndarray
from book import get_lines


EmbeddingList = Union[list[Tensor], ndarray, Tensor]
Embedding = Union[ndarray, Tensor]
 
class Data:
    ids: list[str]
    embeddings: EmbeddingList
    faiss_index: Optional[faiss.IndexFlatL2] = None

    def __init__(self, ids: list[str], embeddings: EmbeddingList) -> None:
        self.ids = ids
        self.embeddings = embeddings

    def initialize_faiss(self):
        self.faiss_index = build_faiss_index(self.embeddings)

    def embedding_for_verse_id(self, verse_id) -> Embedding:
        index = self.verse_id_to_index(verse_id)
        return self.embeddings[index]

    def verse_id_to_index(self, verse_id) -> int:
        return self.ids.index(verse_id)

    def verse_index_to_id(self, verse_index) -> str:
        return self.ids[verse_index]

    def next_verse_id(self, verse_id: str) -> str:
        index = self.verse_id_to_index(verse_id)
        return self.ids[index+1]

    def find_similar_verse_ids(self, embedding: Embedding, k=10) -> list[str]:
        if not self.faiss_index:
            raise ValueError('faiss not initialized')
        _, I = self.faiss_index.search(np.array([embedding]), k)
        return [self.verse_index_to_id(ix) for ix in I[0]]


def build_faiss_index(embeddings) -> faiss.IndexFlatL2:
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings))
    return index

def data_from_book(book_path: Path, model: SentenceTransformer):
    ids = []
    lines = []
    for (id, line) in get_lines(book_path):
       ids.append(id)
       lines.append(line)
    embeddings = model.encode(lines)
    return Data(ids, embeddings)

def data_from_json(path: Path) -> Data:
    with open(path) as f:
        data = json.load(f)
        return Data(data['ids'], data['embeddings'])

def data_from_file(path: Path) -> Data:
    with open(path, 'rb') as f:
        byte_data = f.read()
        data = msgpack.unpackb(byte_data)
        return Data(data['ids'], data['embeddings'])

def save_data(data:Data, path: Path):
    with open(path, "wb") as fp:
        packed: Any = msgpack.packb({
            "ids": data.ids,
            "embeddings": [list(map(float, e)) for e in data.embeddings]
        })
        fp.write(packed)
