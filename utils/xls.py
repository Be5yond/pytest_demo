import json
import pathlib
from functools import namedtuple
import pandas as pd
HOMEPATH = pathlib.Path(__file__).parent.parent


testdata = namedtuple('testdata', ['title', 'step', 'schema'])

def gen_data(book_name, sheet_name):
    book_name +='.xls'  # 测试类名为文件名
    sheet_name = sheet_name.partition('_')[-1]  # 测试方法名 去掉test前缀为sheet名
    book_path = HOMEPATH/'datas'/book_name
    dbook = pd.ExcelFile(book_path)
    if sheet_name in dbook.sheet_names:
        df_data =  dbook.parse(sheet_name=sheet_name)
        ret = []
        for index, row in df_data.iterrows():
            dct = row.to_dict()
            title = dct.pop('id')
            schema = json.loads(dct.pop('scm'))
            step = parse(dct)
            ret.append(testdata(title, step, schema))
        return ret
    return []




def parse(data):
    temp = {}
    for k, v in data.items():
        if not v:
            continue
        elif isinstance(v, float):
            temp[k] = float(v)
        else:
            temp[k] = v
    return temp


if __name__ == '__main__':
    gen_data('TestUserClass','test_user_login_fail')
    pass

