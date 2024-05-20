#!/usr/bin/env python3
import sys
import datetime
from pathlib import Path
from book import get_lines, BOOKS
from data import data_from_book, save_data, save_datas

def get_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("sentence-transformers/gtr-t5-large")

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
    save_data_mpk(data, book_index)

def save_data_mpk(data, book_index):
    save_path = Path(f"embeddings/embeddings-{book_index}.mpk")
    print(f'saving {save_path}')
    save_data(data, save_path)

def save_all_embeddings( model):
    datas = []
    for book_index, book_title in enumerate(BOOKS):
        print(f'processing {book_title}')
        book_path = Path('split/out') / Path(book_title)
        data = data_from_book(book_path, model)
        datas.append(data)
        save_data_mpk(data, book_index)
    save_path = Path(f"embeddings/embeddings-all.mpk")
    save_datas(datas, save_path)

if __name__ == '__main__':
    print(datetime.datetime.now().isoformat())
    model = get_model()
    print('got model')
    print(datetime.datetime.now().isoformat())
    if len(sys.argv) == 1:
        print('save all books')
        save_all_embeddings(model)
    else:
        books = [int(b) for b in sys.argv[1:]]
        for book_index in books:
            save_embeddings(book_index, model)
    print(datetime.datetime.now().isoformat())
