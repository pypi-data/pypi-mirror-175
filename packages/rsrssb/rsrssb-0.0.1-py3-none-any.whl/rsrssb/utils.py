import json
import re
import os
from .parser import args


def tsv2json(input_file) -> list:
    arr = []
    with open(input_file, 'r+') as file:

        a = file.readline()

        # The first line consist of headings of the record.
        # Store it in an array and move to next line in input_file.
        headers = [t.strip() for t in a.split('\t')]
        for line in file:
            d = {}
            for t, f in zip(headers, line.split('\t')):

                # Convert each row into dictionary with keys as titles
                d[t] = f.strip()

            # use strip to remove '\n'.
            arr.append(d)

        # append all the individual dictionaires into list
        # and return as a hydrated json object
        return json.loads(json.dumps(arr))


def filesEndingWith(extension) -> list:
    return [file for file in os.listdir() if file.__contains__(extension)]


def filterFiles():
    sortValue = args.sort
    fullLibrary = tsv2json(args.audible_cli_data)
    goodFiles = []

    # RSRSSB expects files to be named as follows: '$title: $series, Book $series_sequence'
    # for now, only author sort is implemented.
    for book in fullLibrary:
        if authorsInList(book['authors'], sortValue):
            if book['subtitle'] == '':
                book['filePath'] = book['title'] + '.mp3'
            else:
                book['filePath'] = book['title'] + \
                    ': ' + book['subtitle'] + f'.mp3'
            goodFiles += [book["filePath"]]
    return goodFiles


# changes ```any_filename.123``` to ```any_filename```
def stripFileExtension(fileName):
    return re.sub(r'\....$', '', fileName)


def authorsInList(authors, author):
    if type(authors) == type('some string'):
        if authors == author:
            return True

    for a in authors:
        if a == author:
            return True

    return False


def bookInSeries(book, series):
    return book.series_title == series
