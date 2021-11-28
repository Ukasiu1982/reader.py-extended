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
        with open(dst, 'w') as file:
            cls.saver(obj, file)


class FileJsonHandler(BaseFileHandler):
    _type = 'json'
    loader = json.load
    saver = json.dump


class FilePickleHandler(BaseFileHandler):
    _type = 'pickle'
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


# def wczytaj_plik(src):
#     try:
#         with open(src, 'r') as f:
#             if check_file_type(src) == "json":
#                 fh = FileJsonHandler()
#                 data = fh.open(src)
#             #data = json.load(f)
#         return True, data
#     except FileNotFoundError:
#         print("Plik nie zostal znaleziony")
#         return False, None


def stworz_katalog(dst):
    if not os.path.isdir(os.path.split(dst)[0]) and os.path.split(dst)[0]:
        os.makedirs(os.path.split(dst)[0])

src = sys.argv[1]
dst = sys.argv[2]
changes = sys.argv[3:]

# czy_wczytany, zawartosc_pliku = wczytaj_plik(src)
# if czy_wczytany:
#     print(zawartosc_pliku)
# else:
#     print(f"Plik nie zostal wczytany poprawnie: {zawartosc_pliku}")

if check_file_type(src) == "json":
    loader = FileJsonHandler()
if check_file_type(src) == "pkl":
    loader = FilePickleHandler()
if check_file_type(src) == "csv":
    loader = FileCSVHandler()
if check_file_type(dst) == "json":
    writer = FileJsonHandler()
if check_file_type(dst) == "pkl":
    writer = FilePickleHandler()
if check_file_type(dst) == "csv":
    writer = FileCSVHandler()

stworz_katalog(dst)

saved_file = loader.open(src)
bf = DataManipulator(changes, saved_file)
writer.save(dst, bf.data)
