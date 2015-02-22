from argparse import ArgumentParser


def make_argparser():
  parser = ArgumentParser(
    prog='eumi',
    description='Run the eumi server.',
    )

  parser.add_argument(
    '--host',
    type=str,
    help='The host (IP) to bind. Default: localhost.',
    default='',
    )

  parser.add_argument(
    '--port',
    type=int,
    help='The port number on which to listen. Default: 8000.',
    default=8000,
    )

  parser.add_argument(
    '-b', '--base-dir',
    help='The directory to load/store page data. Default: ./server',
    default='./server',
    )

  return parser
