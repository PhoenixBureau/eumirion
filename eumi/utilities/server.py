from collections import defaultdict
from eumi.joy.stack import strstack
from eumi.page_actions import scan_text, linkerate, l


def extract_server_data(server):
  data = {}
  for (kind, unit), page_data in server.router.iteritems():
    key = linkerate(kind, unit)
    page_data = page_data.data
    page = data[key] = {
      'text': page_data['text'],
      'title': page_data['title'],
      }
    if 'joy' in page_data:
      page['joy'] = strstack(page_data['joy'])
  return data


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
