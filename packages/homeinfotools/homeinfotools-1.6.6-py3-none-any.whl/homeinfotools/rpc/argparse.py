"""Argument parsing."""

from argparse import ArgumentParser, Namespace
from multiprocessing import cpu_count
from pathlib import Path


__all__ = ['get_args']


def get_args() -> Namespace:
    """Returns parsed CLI arguments."""

    parser = ArgumentParser(description='Batch upgrade systems.')
    parser.add_argument(
        'system', type=int, nargs='+', help='systems to upgrade'
    )
    parser.add_argument(
        '-S', '--sysupgrade', action='store_true', help='upgrade the systems'
    )
    parser.add_argument(
        '-X', '--execute', metavar='command',
        help='execute the commands on the systems'
    )
    parser.add_argument(
        '-R', '--reboot', action='store_true', help='reboot the systems'
    )
    parser.add_argument(
        '-c', '--cleanup', action='store_true',
        help='cleanup unneeded packages after upgrade'
    )
    parser.add_argument(
        '-d', '--debug', action='store_true', help='enable debug logging'
    )
    parser.add_argument(
        '-i', '--install', default=(), nargs='+', metavar='pkg',
        help='install the given packages'
    )
    parser.add_argument(
        '-j', '--json', type=Path, metavar='file',
        help='log jobs as JSON when done'
    )
    parser.add_argument(
        '-k', '--keyring', action='store_true',
        help='upgrade the keyring before sysupgrade'
    )
    parser.add_argument(
        '-n', '--no-stdin', action='store_true',
        help='make ssh to not read STDIN'
    )
    parser.add_argument(
        '-o', '--overwrite', default=(), nargs='+', metavar='glob',
        help='globs of files to overwrite'
    )
    parser.add_argument(
        '-p', '--processes', type=int, metavar='n', default=cpu_count(),
        help='amount of parallel processes'
    )
    parser.add_argument(
        '-q', '--chunk-size', type=int, metavar='n',
        help='chunk size for multiprocessing'
    )
    parser.add_argument(
        '-s', '--shuffle', action='store_true', help='shuffle systems'
    )
    parser.add_argument(
        '-t', '--timeout', type=int, metavar='seconds', default=20*60,
        help='seconds to wait for subprocesses to time out'
    )
    parser.add_argument(
        '-u', '--user', metavar='name', help='set the ssh user name'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='enable verbose logging'
    )
    parser.add_argument(
        '-y', '--yes', action='store_true',
        help='assume yes on program queries'
    )
    return parser.parse_args()
