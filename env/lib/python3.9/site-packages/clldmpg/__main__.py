import re
import sys
import argparse
import contextlib

from clldutils.loglib import Logging
from clldutils.clilib import get_parser_and_subparsers, register_subcommands, PathType

import clldmpg.commands


def app_name(project_dir):
    setup = (project_dir / 'setup.py').read_text(encoding='utf-8')
    match = re.search(r'main\s*=\s*(?P<name>[a-z0-9]+):main', setup)
    if match:
        return match.group('name')


class ProjectDirType(PathType):
    def __init__(self):
        PathType.__init__(self, type='dir')

    def __call__(self, string):
        d = super().__call__(string)
        setup = d / 'setup.py'
        if not setup.exists():
            raise argparse.ArgumentTypeError('{0}/setup.py does not exist!'.format(d))
        if not app_name(d):
            raise argparse.ArgumentTypeError('Cannot determine app name for {0}!'.format(d))
        return d


def main(args=None, catch_all=False, parsed_args=None, log=None):
    parser, subparsers = get_parser_and_subparsers('clldmpg')
    parser.add_argument(
        "--project",
        help='clld app project dir',
        default=".",
        type=ProjectDirType())

    register_subcommands(subparsers, clldmpg.commands)

    args = parsed_args or parser.parse_args(args=args)

    if not hasattr(args, "main"):
        parser.print_help()
        return 1

    with contextlib.ExitStack() as stack:
        if not log:  # pragma: no cover
            stack.enter_context(Logging(args.log, level=args.log_level))
        else:  # pragma: no cover
            args.log = log
        args.app_name = app_name(args.project)
        try:
            return args.main(args) or 0
        except KeyboardInterrupt:  # pragma: no cover
            return 0
        except Exception as e:  # pragma: no cover
            if catch_all:
                print(e)
                return 1
            raise


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main() or 0)
