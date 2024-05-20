import sys

from book import Book
from make_embeddings import get_model

if __name__ == '__main__':
    if len(sys.argv) > 1 :
        book_index = int(sys.argv[1])
        book = Book(book_index)
    else:
        book = Book()
    simils = book.similarities()
    totals = [(sum(s),i) for i,s in enumerate(simils)]
    sorted_totals = sorted(totals)
    least_idx = sorted_totals[0][1]
    most_idx = sorted_totals[-1][1]
    least_similar_verse_id = book.data.verse_index_to_id(least_idx)
    most_similar_verse_id = book.data.verse_index_to_id(most_idx)
    print(book.verses[most_similar_verse_id])
    print('-' * 100)
    print(book.verses[least_similar_verse_id])


 
    

