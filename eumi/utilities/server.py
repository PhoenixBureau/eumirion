from collections import defaultdict
from os.path import exists, join, realpath
from os import makedirs
from joy.stack import strstack
from .loader import load
from ..page_actions import scan_text, linkerate, l


def dir_to_data(base_dir):
  return dict(
    f(path, page_data)
    for path, page_data in load(base_dir)
    )


def f(path, page_data):
  key = linkerate(*path)
  page = {
      'text': page_data['text'],
      'title': page_data['title'],
      }
  if 'joy' in page_data:
    page['joy'] = strstack(page_data['joy'])
  return key, page


def extract_server_data(server):
  data = {}
  for (kind, unit), page_handler in server.router.iteritems():
    key, page = f((kind, unit), page_handler.data)
    data[key] = page
  return data


def out_to_files(data, base_dir='.'):
  base_dir = realpath(base_dir)
  for path, page_data in data.iteritems():
    loc = join(base_dir, path.lstrip('/'))
    if not exists(loc):
      makedirs(loc)
    for field in ('title', 'text', 'joy'):
      if field in page_data:
        fn = join(loc, field)
        print 'writing', fn
        with open(fn, 'w') as f:
          f.write(page_data[field])


def dependency_graph(data):
  deps = {}
  for key, page_data in data.iteritems():
    page_deps = defaultdict(set)
    text = page_data['text']
    for action, kind, unit in scan_text(text):
      if action == 'text' and unit is None:
        continue
      page_deps[action].add(l(kind, unit))
    deps[key] = dict(page_deps)
  return deps
