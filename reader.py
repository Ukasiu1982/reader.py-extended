import json
import pickle
import csv
import os
import sys


class BaseFileHandler:
    @classmethod
    def open(cls, src):
        with open(src, 'r') as file:
            retval = cls.loader(file)
        return retval

    @classmethod
    def save(cls, dst, obj):
        with open(dst, f'w{cls.byte}') as file:
            cls.saver(obj, file)


class FileJsonHandler(BaseFileHandler):
    _type = 'json'
    byte = ""
    loader = json.load
    saver = json.dump

class FilePickleHandler(BaseFileHandler):
    _type = 'pickle'
    byte = "b"
    loader = pickle.load
    saver = pickle.dump

class FileCSVHandler:
    _type = "csv"
    def open(self, src):
        with open(src, "r") as file:
            reader = csv.reader(file)
            retval = [line for line in reader]
        return retval

    def save(self, dst, obj):
        with open(dst, "w") as file:
            writer = csv.writer(file)
            for row in obj:
                writer.writerow(row)

class DataManipulator:
    def __init__(self, changes, data):
        self.changes = [z.split(",") for z in changes]
        self.data = data

    def make_changes(self):
        for change in self.changes:
            self.data[int(change[0])][int(change[1])] = change[2]


def check_file_type(src):
    return os.path.splitext(src)[-1][1:]


def stworz_katalog(dst):
    if not os.path.isdir(os.path.split(dst)[0]) and os.path.split(dst)[0]:
        os.makedirs(os.path.split(dst)[0])

src = sys.argv[1]
dst = sys.argv[2]
changes = sys.argv[3:]


if check_file_type(src) == "json":
    loader = FileJsonHandler()
if check_file_type(src) == "pickle":
    loader = FilePickleHandler()
if check_file_type(src) == "csv":
    loader = FileCSVHandler()
if check_file_type(dst) == "json":
    writer = FileJsonHandler()
if check_file_type(dst) == "pickle":
    writer = FilePickleHandler()
if check_file_type(dst) == "csv":
    writer = FileCSVHandler()

stworz_katalog(dst)

saved_file = loader.open(src)
bf = DataManipulator(changes, saved_file)
bf.make_changes()
print(bf.data)
writer.save(dst, bf.data)


# python reader.py '.\hurricanes.csv' '.\out11.csv'  "6,6, 666" "7,6, 787
# python reader.py '.\hurricanes.csv' '.\out11.json'  "6,6, 666" "7,6, 787
# python reader.py '.\hurricanes.csv' '.\out11.pickle'  "6,6, 666" "7,6, 787

