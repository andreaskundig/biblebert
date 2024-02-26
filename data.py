from dataclasses import dataclass
from pathlib import Path
import json
import msgpack
from sentence_transformers import SentenceTransformer
from typing import Any, Union
from torch import Tensor
from numpy import ndarray
from book import get_lines

EmbeddingList = Union[list[Tensor], ndarray, Tensor]

@dataclass
class Data:
    ids: list[str]
    embeddings: EmbeddingList

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
