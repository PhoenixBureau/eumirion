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
    '-p', '--pickle',
    type=str,
    help=('The pickle file from which to load and save data.'
          ' Default: server.pyckle.'
          ),
    default='server.pyckle',
    )

  parser.add_argument(
    '--crazy-town',
    action='store_true',
    help='Run without saving pickles! Yikes!',
    )

  return parser
