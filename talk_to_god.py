import sys

from book import Book
from make_embeddings import get_model

if __name__ == '__main__':
    if len(sys.argv) > 1 :
        book_index = int(sys.argv[1])
        book = Book(book_index)
    else:
        book = Book()
    book.init_embeddings()
    model = get_model()

    said = input(f"What do yo want from {book.title} ?\n")
    while True:
        embedding = model.encode([said])[0]
        verse_id = book.data.find_similar_verse_ids(embedding, k=1)[0]
        # verse = book.verses[next_verse_id]
        verse = book.verses[verse_id]
        additional_verses = 3
        for i in range(0,additional_verses):
            verse_id = book.data.next_verse_id(verse_id)
            verse = f'{verse}\n{book.verses[verse_id]}'
        print('-'*50)    
        print('\n'+verse+'\n'+('-'*50)+'\n')
        said = input('> ')
    

