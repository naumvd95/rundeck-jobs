import argparse
import os

import pytest


def check(args):
    testdir = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'tests'))

    xml_path = os.path.abspath(os.path.join('./', args.xml_path))

    pytest.main([testdir, '-m', args.type,
                 '--junit-xml', xml_path])


def list_types(args):
    print('The following verification types are available:\n\nhealthcheck\n')


def main():
    parser = argparse.ArgumentParser(prog="devops-portal-tests")
    subparsers = parser.add_subparsers()
    parser_check = subparsers.add_parser(
        "check",
        help="execute tests with passed verification type"
    )
    parser_check.add_argument("--type",
                              help="specified verification type")
    parser_check.add_argument("--xml_path",
                              default='result.xml',
                              help="path to test result xml file")
    parser_check.set_defaults(func=check)

    parser_list = subparsers.add_parser(
        "list",
        help="list of available verification types"
    )
    parser_list.set_defaults(func=list_types)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
