"""
Configfile support for discovering local clones of Catalogs.
"""
import pathlib
import collections
import configparser

import appdirs

__all__ = ['Config']
CLONES = 'clones'


class Config(configparser.ConfigParser):
    """
    A config file for the cli.
    """
    def __init__(self):
        self._files = None
        super().__init__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.to_file()

    def read(self, filenames, encoding=None):
        if self._files:
            raise ValueError('Config cannot read more than one file!')
        self._files = filenames
        super().read(filenames, encoding=encoding)

    @staticmethod
    def dir():
        res = pathlib.Path(appdirs.user_config_dir('cldf'))
        if not res.exists():
            res.mkdir(parents=True, exist_ok=True)
        return res

    # Note: `fname` must not be defined at import, because we need to patch `appdirs` for tests!
    @staticmethod
    def fname():
        return Config.dir() / 'catalog.ini'

    @property
    def clones(self):
        if CLONES not in self.sections():
            self[CLONES] = collections.OrderedDict()
        return self[CLONES]

    @classmethod
    def from_file(cls, fname=None):
        cfg = cls()
        cfg.read(str(fname or cls.fname()))
        return cfg

    def to_file(self, fname=None):
        with (fname or self.fname()).open('w', encoding='utf8') as fp:
            self.write(fp)

    def add_clone(self, key, path):
        self.clones[key] = str(pathlib.Path(path).resolve())

    def get_clone(self, key):
        try:
            return pathlib.Path(self.clones[key])
        except KeyError:
            raise KeyError('Config {0} has no entry for {1}'.format(self._files, key))
