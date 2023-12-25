#!/usr/bin/env python3
import os, re

book_titles = [
    'The First Book of Moses: Called Genesis',
    'The Second Book of Moses: Called Exodus',
    'The Third Book of Moses: Called Leviticus',
    'The Fourth Book of Moses: Called Numbers',
    'The Fifth Book of Moses: Called Deuteronomy',
    'The Book of Joshua',
    'The Book of Judges',
    'The Book of Ruth',
    'The First Book of Samuel',
    'The Second Book of Samuel',
    'The First Book of the Kings',
    'The Second Book of the Kings',
    'The First Book of the Chronicles',
    'The Second Book of the Chronicles',
    'Ezra',
    'The Book of Nehemiah',
    'The Book of Esther',
    'The Book of Job',
    'The Book of Psalms',
    'The Proverbs',
    'Ecclesiastes',
    'The Song of Solomon',
    'The Book of the Prophet Isaiah',
    'The Book of the Prophet Jeremiah',
    'The Lamentations of Jeremiah',
    'The Book of the Prophet Ezekiel',
    'The Book of Daniel',
    'Hosea',
    'Joel',
    'Amos',
    'Obadiah',
    'Jonah',
    'Micah',
    'Nahum',
    'Habakkuk',
    'Zephaniah',
    'Haggai',
    'Zechariah',
    'Malachi',
    'The New Testament of the King James Bible',
    'The Gospel According to Saint Matthew',
    'The Gospel According to Saint Mark',
    'The Gospel According to Saint Luke',
    'The Gospel According to Saint John',
    'The Acts of the Apostles',
    'The Epistle of Paul the Apostle to the Romans',
    'The First Epistle of Paul the Apostle to the Corinthians',
    'The Second Epistle of Paul the Apostle to the Corinthians',
    'The Epistle of Paul the Apostle to the Galatians',
    'The Epistle of Paul the Apostle to the Ephesians',
    'The Epistle of Paul the Apostle to the Philippians',
    'The Epistle of Paul the Apostle to the Colossians',
    'The First Epistle of Paul the Apostle to the Thessalonians',
    'The Second Epistle of Paul the Apostle to the Thessalonians',
    'The First Epistle of Paul the Apostle to Timothy',
    'The Second Epistle of Paul the Apostle to Timothy',
    'The Epistle of Paul the Apostle to Titus',
    'The Epistle of Paul the Apostle to Philemon',
    'The Epistle of Paul the Apostle to the Hebrews',
    'The General Epistle of James',
    'The First Epistle General of Peter',
    'The Second General Epistle of Peter',
    'The First Epistle General of John',
    'The Second Epistle General of John',
    'The Third Epistle General of John',
    'The General Epistle of Jude',
    'The Revelation of Saint John the Divine'
]

def save_book(title, i, book):
    if not os.path.exists('out'):
        os.makedirs('out')

    ct = title.replace(" ", "-").replace(":", "").lower()
    print(f'save {ct}')
    fixed_book = fix_book_lines(book)
    with open(f'out/{i:02}-{ct}.txt', 'w', encoding='utf-8') as f:
        f.writelines(fixed_book)


def line_matches_title(line, title):
    return line.strip() == title

verse_regex = re.compile(r'\d+:\d+')
def split_verses(book):
   for line in book:
       for chunk in re.split(r'(\d+:\d+)', line):
           if chunk:
               yield chunk

def fix_book_lines(book):
    fixed_book = [book[0]]
    for chunk in split_verses(book[1:]):
        stripped_chunk = chunk.rstrip()
        # print(f'CHUNK "{stripped_chunk}"')
        if verse_regex.match(stripped_chunk):
            fixed_book[-1] = fixed_book[-1] + '\n'
            fixed_book.append(stripped_chunk)
        elif stripped_chunk:
            fixed_book[-1] = fixed_book[-1] + ' ' + stripped_chunk.strip()
    return fixed_book

def split_bible(filename):
    remaining_titles = book_titles
    book = []
    book_index = 0
    title = ''
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            # if line.strip():
            #     print(line.strip())
            not_last_book = bool(remaining_titles)
            if not_last_book and line.strip() == remaining_titles[0]:
                # print(f'new title after: "{title}"')
                if book:
                    save_book(title, book_index, book)
                if remaining_titles:
                    title = remaining_titles[0]
                    # print(f'new title "{title}"')
                    book = []
                    book_index += 1
                remaining_titles = remaining_titles[1:]
            if title and line.strip():
                book.append(line)
        save_book(title, book_index, book)

if __name__ == "__main__":
    split_bible('bible.txt')
