from argparse import ArgumentParser


def make_argparser():
  parser = ArgumentParser(
    prog='eumi',
    description='Run the eumi server.',
    )

  parser.add_argument(
    '--host',
    type=str,
    help='The host (IP) to bind.',
    default='',
    )

  parser.add_argument(
    '--port',
    type=int,
    help='The port number on which to listen.',
    default=8000,
    )

  parser.add_argument(
    '-p', '--pickle',
    type=str,
    help='The pickle file from which to load and save data.',
    default='server.pyckle',
    )

  return parser
