"""
Upload downloads for a specific version of the data to CDSTAR
"""
import os
import re
import pathlib

from clldutils.jsonlib import load, update

try:
    from cdstarcat.catalog import Catalog
except ImportError:  # pragma: no cover
    Catalog = None


def register(parser):
    parser.add_argument("--version", help='data version', default="1.0")
    parser.add_argument("--description", default=None)


def run(args):
    if not Catalog:  # pragma: no cover
        args.log.error('pip install cdstarcat')
        return

    title_pattern = re.compile('%s (?P<version>[0-9.]+) - downloads' % re.escape(args.app_name))
    title = '{0} {1} - downloads'.format(args.app_name, args.version)
    pkg_dir = args.project.joinpath(args.app_name)
    with Catalog(
            pathlib.Path(os.environ['CDSTAR_CATALOG']),
            cdstar_url=os.environ['CDSTAR_URL'],
            cdstar_user=os.environ['CDSTAR_USER'],
            cdstar_pwd=os.environ['CDSTAR_PWD']) as cat:
        obj = cat.api.get_object()
        obj.metadata = {"creator": "pycdstar", "title": title}
        if args.description:
            obj.metadata["description"] = args.description

        for fname in pkg_dir.joinpath('static', 'download').iterdir():
            if fname.is_file() and not fname.name.startswith('.'):
                print(fname.name)
                obj.add_bitstream(
                    fname=fname.as_posix(), name=fname.name.replace('-', '_'))
        cat.add(obj)

    fname = pkg_dir.joinpath('static', 'downloads.json')
    with update(fname, default={}, indent=4) as downloads:
        for oid, spec in load(pathlib.Path(os.environ['CDSTAR_CATALOG'])).items():
            if 'metadata' in spec and 'title' in spec['metadata']:
                match = title_pattern.match(spec['metadata']['title'])
                if match:
                    if match.group('version') not in downloads:
                        spec['oid'] = oid
                        downloads[match.group('version')] = spec
    args.log.info('{0} written'.format(fname))
    args.log.info('{0}'.format(os.environ['CDSTAR_CATALOG']))
