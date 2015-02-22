from os.path import exists, join
from os import listdir
from string import hexdigits
from ..joy.parser import text_to_expression


TEXT_SIZE_LIMIT_BYTES = 299 * 1024


def valid(component):
  return len(component) == 8 and all(
    character in hexdigits
    for character in component
    )


def load(base_dir):
  for k in listdir(base_dir):
    if valid(k):
      kind = join(base_dir, k)
      for u in listdir(kind):
        if valid(u):
          path = join(kind, u)
          key = int(k, 16), int(u, 16)
          yield key, load_page(path)


def load_page(path):
  data = {}

  with open(join(path, 'text'), 'r') as text:
    data['text'] = text.read(TEXT_SIZE_LIMIT_BYTES)

  with open(join(path, 'title'), 'r') as title:
    data['title'] = title.read(1024)

  joy = join(path, 'joy')
  if exists(joy):
    with open(joy, 'r') as joy:
      joy_source = joy.read(1024)
    data['joy'] = text_to_expression(joy_source)

  return data
