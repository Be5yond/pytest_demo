import json
import pathlib
from tablib import Databook
HOMEPATH = pathlib.Path(__file__).parent.parent


def gen_data(book_name, sheet_name):
    book_name +='.xls'
    sheet_name = sheet_name.partition('_')[-1]
    book_path = HOMEPATH/'datas'/book_name
    dbook = Databook().load('xls', open(str(book_path), 'rb').read())
    for sheet in dbook.sheets():
        if sheet.title == sheet_name:
            ret = json.loads(sheet.json)
            return map(parse, ret)
    return []


def parse(data):
    temp = {}
    for k, v in data.items():
        if not v:
            continue
        elif isinstance(v, float):
            temp[k] = int(v)
        else:
            temp[k] = v
    return temp


if __name__ == '__main__':
    pass

