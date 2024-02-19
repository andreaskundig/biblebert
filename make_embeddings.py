#!/usr/bin/env python3
import re
import json
import datetime
from pathlib import Path
from sentence_transformers import SentenceTransformer
from book import get_lines, BOOKS
import msgpack

def get_model():
    return  SentenceTransformer("sentence-transformers/gtr-t5-large")

def save_embeddings_to_json(book_index, model):
    book_title = BOOKS[book_index]
    print(f'processing {book_title}')
    ids = []
    lines = []
    book_path = Path('split/out') / Path(book_title)
    for (id, line) in get_lines(book_path):
       ids.append(id)
       lines.append(line)

    embeddings = model.encode(lines)
    with open(f"embeddings/embeddings-{book_index}.json", "w") as fp:
        json.dump(
            {
                "ids": ids,
                "embeddings": [list(map(float, e)) for e in embeddings]
            },
            fp,
        )

def save_embeddings(book_index, model):
    book_title = BOOKS[book_index]
    print(f'processing {book_title}')
    ids = []
    lines = []
    book_path = Path('split/out') / Path(book_title)
    for (id, line) in get_lines(book_path):
       ids.append(id)
       lines.append(line)

    embeddings = model.encode(lines)
    with open(f"embeddings/embeddings-{book_index}.json", "w") as fp:
        # TODO create Data object and save it
        pass

if __name__ == '__main__':
    print(datetime.datetime.now().isoformat())
    model = get_model()
    print('got model')
    print(datetime.datetime.now().isoformat())
    for book_index in [0, 40]:
        save_embeddings_to_json(book_index, model)
        print(datetime.datetime.now().isoformat())
