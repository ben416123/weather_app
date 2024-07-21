import os
import re
import inspect


def _get_parser(dirname):
    files = [f.replace('.py', '')
             for f in os.listdir(dirname)
             if not f.startswith('___')]

    return files


def import_parsers(parserfiles):
    m = re.compile('.+parser$', re.I)
    __modules = __import__('weatherapp.parsers',
                           globals(),
                           locals(),
                           parserfiles,
                           0)
    __parsers = [(k, v) for k, v in inspect.getmembers(__modules)
                 if inspect.isclass(v) and m.match(k)]

    __classes = dict()

    for k, v in __parsers:
        __classes.update({k: v for k, v in inspect.getmembers(v)
                          if inspect.isclass(v) and m.match(k)})

    return __classes


def load(dirname):
    parserfiles = _get_parser(dirname)
    return import_parsers(parserfiles)
