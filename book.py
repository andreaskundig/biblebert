#!/usr/bin/env python3
import re

BOOK11 = book_path = 'split/out/11-the-first-book-of-the-kings.txt'

def get_lines(filename):
    with open(filename, encoding="utf-8") as f:
        for line in f:
            match = re.match(r'(\d+:\d+) +(.*)', line)
            if match:
                id = match.group(1)
                text = match.group(2)
                yield (id, text)

BOOKS = [
    '00-the-first-book-of-moses-called-genesis.txt',
    '01-the-second-book-of-moses-called-exodus.txt',
    '02-the-third-book-of-moses-called-leviticus.txt',
    '03-the-fourth-book-of-moses-called-numbers.txt',
    '04-the-fifth-book-of-moses-called-deuteronomy.txt',
    '05-the-book-of-joshua.txt',
    '06-the-book-of-judges.txt',
    '07-the-book-of-ruth.txt',
    '08-the-first-book-of-samuel.txt',
    '09-the-second-book-of-samuel.txt',
    '10-the-first-book-of-the-kings.txt',
    '11-the-second-book-of-the-kings.txt',
    '12-the-first-book-of-the-chronicles.txt',
    '13-the-second-book-of-the-chronicles.txt',
    '14-ezra.txt',
    '15-the-book-of-nehemiah.txt',
    '16-the-book-of-esther.txt',
    '17-the-book-of-job.txt',
    '18-the-book-of-psalms.txt',
    '19-the-proverbs.txt',
    '20-ecclesiastes.txt',
    '21-the-song-of-solomon.txt',
    '22-the-book-of-the-prophet-isaiah.txt',
    '23-the-book-of-the-prophet-jeremiah.txt',
    '24-the-lamentations-of-jeremiah.txt',
    '25-the-book-of-the-prophet-ezekiel.txt',
    '26-the-book-of-daniel.txt',
    '27-hosea.txt',
    '28-joel.txt',
    '29-amos.txt',
    '30-obadiah.txt',
    '31-jonah.txt',
    '32-micah.txt',
    '33-nahum.txt',
    '34-habakkuk.txt',
    '35-zephaniah.txt',
    '36-haggai.txt',
    '37-zechariah.txt',
    '38-malachi.txt',
    '39-the-new-testament-of-the-king-james-bible.txt',
    '40-the-gospel-according-to-saint-matthew.txt',
    '41-the-gospel-according-to-saint-mark.txt',
    '42-the-gospel-according-to-saint-luke.txt',
    '43-the-gospel-according-to-saint-john.txt',
    '44-the-acts-of-the-apostles.txt',
    '45-the-epistle-of-paul-the-apostle-to-the-romans.txt',
    '46-the-first-epistle-of-paul-the-apostle-to-the-corinthians.txt',
    '47-the-second-epistle-of-paul-the-apostle-to-the-corinthians.txt',
    '48-the-epistle-of-paul-the-apostle-to-the-galatians.txt',
    '49-the-epistle-of-paul-the-apostle-to-the-ephesians.txt',
    '50-the-epistle-of-paul-the-apostle-to-the-philippians.txt',
    '51-the-epistle-of-paul-the-apostle-to-the-colossians.txt',
    '52-the-first-epistle-of-paul-the-apostle-to-the-thessalonians.txt',
    '53-the-second-epistle-of-paul-the-apostle-to-the-thessalonians.txt',
    '54-the-first-epistle-of-paul-the-apostle-to-timothy.txt',
    '55-the-second-epistle-of-paul-the-apostle-to-timothy.txt',
    '56-the-epistle-of-paul-the-apostle-to-titus.txt',
    '57-the-epistle-of-paul-the-apostle-to-philemon.txt',
    '58-the-epistle-of-paul-the-apostle-to-the-hebrews.txt',
    '59-the-general-epistle-of-james.txt',
    '60-the-first-epistle-general-of-peter.txt',
    '61-the-second-general-epistle-of-peter.txt',
    '62-the-first-epistle-general-of-john.txt',
    '63-the-second-epistle-general-of-john.txt',
    '64-the-third-epistle-general-of-john.txt',
    '65-the-general-epistle-of-jude.txt',
    '66-the-revelation-of-saint-john-the-divine.txt',
]
