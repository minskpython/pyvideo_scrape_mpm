import argparse


def create_interface():
    parser = argparse.ArgumentParser()
    parser._actions[0].help = 'Show parameters'

    parser.add_argument('-f', '--file',
                        help='Use your own file with urls',
                        action='store',
                        default='urls.list',
                        metavar='file'
                        )

    parser.add_argument('-s', '--silent',
                        help='silent mode',
                        action='store_true'
                        )

    parser.add_argument('-d', '--directory',
                        help='directory name for JSON files',
                        action='store',
                        default='.',
                        metavar='dir'
                        )

    args = parser.parse_args()
    return args
