#!/usr/bin/env python3
import json
import datetime
from pathlib import Path
from sentence_transformers import SentenceTransformer
from book import get_lines, BOOKS
from data import data_from_book, save_data

def get_model():
    return  SentenceTransformer("sentence-transformers/gtr-t5-large")

def get_book_lines(book_index):
    book_title = BOOKS[book_index]
    print(f'processing {book_title}')
    book_path = Path('split/out') / Path(book_title)
    return get_lines(book_path)


def save_embeddings(book_index, model):
    book_title = BOOKS[book_index]
    print(f'processing {book_title}')
    book_path = Path('split/out') / Path(book_title)
    data = data_from_book(book_path, model)
    save_path = Path(f"embeddings/embeddings-{book_index}.mpk")
    save_data(data, save_path)


def save_embeddings_to_json(book_index, model):
    book_title = BOOKS[book_index]
    print(f'processing {book_title}')
    book_path = Path('split/out') / Path(book_title)

    ids = []
    lines = []
    for (id, line) in get_book_lines(book_path):
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

if __name__ == '__main__':
    print(datetime.datetime.now().isoformat())
    model = get_model()
    print('got model')
    print(datetime.datetime.now().isoformat())
    for book_index in [0, 40]:
        # save_embeddings_to_json(book_index, model)
        save_embeddings(book_index, model)
        print(datetime.datetime.now().isoformat())
