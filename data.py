from pathlib import Path
import re
import msgpack
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import Any, Union, Optional
from torch import Tensor
from numpy import ndarray


EmbeddingList = Union[list[Tensor], ndarray, Tensor]
Embedding = Union[ndarray, Tensor]

def get_lines(filename):
    with open(filename, encoding="utf-8") as f:
        for line in f:
            match = re.match(r"(\d+:\d+) +(.*)", line)
            if match:
                id = match.group(1)
                text = match.group(2)
                yield (id, text)

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

def save_datas(datas:list[Data], path: Path):
    with open(path, "wb") as fp:
        embeddings = []
        ids = []
        for data_index, data  in enumerate(datas):
            ids.extend([f'{data_index}-{id}' for id in data.ids])
            embeddings.extend([list(map(float, e)) for e in data.embeddings])
        packed: Any = msgpack.packb({
            "ids": ids,
            "embeddings": embeddings
        })
        print(f'saving {path}')
        fp.write(packed)
