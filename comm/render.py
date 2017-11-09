
import re
from faker import Faker
from comm.logger import logger


fake = Faker('zh_CN')


def render(p, cache):
    """
    replace json object values
    :param p: json template to be rendered
    :param cache: parameter pool for data replacement
    :return: new json object
    """
    matcher = re.compile('^{{\s*([A-Za-z]+)\s*}}$')
    func_matcher = re.compile('^{%\s*([0-9a-zA-Z()"_.=]+)\s*%}$')
    if isinstance(p, str) and re.match(matcher, p):
        try:
            para = p.strip('{ }')
            return cache.get(para, p)
        except KeyError as e:
            logger.error(e)
            logger.error(cache)

    if isinstance(p, str) and re.match(func_matcher, p):
        try:
            para = p.strip('[{%} ]')
            return eval(para)
        except Exception as e:
            logger.error(e)
    elif isinstance(p, dict):
        for k, v in p.items():
            p[k] = render(v, cache)
    elif isinstance(p, list):
        for i, v in enumerate(p):
            p[i] = render(v, cache)
        # return list(map(render, *((i,cache) for i in p)))
    return p


if __name__=="__main__":
    import time
    start = time.time()
    for _ in range(1):
        b = {
            'key': {
                'str': '{% fake.pystr(max_chars=10) %}',
                'phone': '{% fake.phone_number() %}',
                'company': '{% fake.company() %}',
            },
            'tu':['{{ val }}', {'newkey': '{{ val }}'}]
        }
        c = {'val': 456}
        print(b)
        print(render(b, c))
    print(time.time() - start)

    # print(render('{{ val }}', c))
    print(b['tu'])
    print(render(b['tu'], c))
