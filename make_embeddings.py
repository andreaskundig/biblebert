#!/usr/bin/env python3
import re
import json
import datetime
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/gtr-t5-large")

def get_model():
    return  SentenceTransformer("sentence-transformers/gtr-t5-large")

def get_lines(filename):
    with open(filename) as f:
        for line in f:
            match = re.match(r'(\d+:\d+ +)(.*)', line)
            if match:
                id = match.group(1)
                text = match.group(2)
                yield (id, text)

def save_embeddings_to_json(book_path, model):
    ids = []
    lines = []
    for (id, line) in get_lines(book_path):
       ids.append(id)
       lines.append(line)

    embeddings = model.encode(lines)
    with open("embeddings.json", "w") as fp:
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
    book_path = 'split/out/11-the-first-book-of-the-kings.txt'
    save_embeddings_to_json(book_path, model)
    print(datetime.datetime.now().isoformat())
