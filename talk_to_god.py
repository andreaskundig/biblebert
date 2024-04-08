import sys

from book import Book
from make_embeddings import get_model

if __name__ == '__main__':
    book_index = int(sys.argv[1])
    book = Book(book_index)
    book.init_embeddings()
    model = get_model()

    said = input(f"What do yo want from {book.title} ?\n")
    while True:
        embedding = model.encode([said])[0]
        verse_id = book.data.find_similar_verse_ids(embedding, k=1)[0]
        next_verse_id = book.data.next_verse_id(verse_id)
        verse = book.verses[next_verse_id]
        said = input(verse+'\n')
    

