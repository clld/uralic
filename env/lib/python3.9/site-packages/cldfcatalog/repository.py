"""
This module provides a thin wrapper around `git.Repo`, exposing only a small portion of its
functionality, following the [Facade pattern](https://en.wikipedia.org/wiki/Facade_pattern).
"""
import re
import pathlib

import git
import git.exc
from pycldf.dataset import GitRepository

__all__ = ['Repository', 'get_test_repo']


class Repository:
    """
    A (clone of a) git repository.
    """
    def __init__(self, path):
        try:
            self.repo = git.Repo(str(path))
        except (git.exc.NoSuchPathError, git.exc.InvalidGitRepositoryError):
            raise ValueError('invalid git repository: {0}'.format(path))
        self._url = None

    @classmethod
    def clone(cls, url, target):
        target = pathlib.Path(target)
        assert (not target.exists()) and target.parent.exists() and target.parent.is_dir()
        git.Git(str(target.parent)).clone(url, target.name)
        return cls(target)

    def update(self):
        """
        Run `git fetch` for each remote.

        :return: `list` of `FetchInfo` objects, one per remote.
        """
        return [remote.fetch()[0] for remote in self.repo.remotes]  # pragma: no cover

    @property
    def dir(self):
        """
        :return: The path of the repository clone as `pathlib.Path`.
        """
        return pathlib.Path(self.repo.working_dir)

    @property
    def active_branch(self):
        """
        :return: Name of the active branch or `None`, if in "detached HEAD" state.
        """
        try:
            return self.repo.active_branch.name
        except TypeError:
            return None

    @property
    def url(self):
        """
        :return: The URL of the remote called `origin` - if it is set, else `None`.

        Note: Since computing the remote may require a `git` call, and we assume the origin will
        not change, we cache the result.
        """
        if self._url is None:
            try:
                url = self.repo.remotes.origin.url
                if url.endswith('.git'):
                    url = url[:-4]
                self._url = url
            except AttributeError:  # pragma: no cover
                pass
        return self._url

    @property
    def github_repo(self):
        """
        :return: GitHub repository name in the form "ORG/REPO", or `None`, if no matching \
        `self.url` is found.
        """
        match = re.search(r'github\.com/(?P<org>[^/]+)/(?P<repo>[^.]+)', self.url or '')
        if match:
            return match.group('org') + '/' + match.group('repo')

    @property
    def tags(self):
        """
        :return: `list` of tags available for the repository. A tag can be used as `spec` argument \
        for `Repository.checkout`
        """
        return self.repo.git.tag().split()

    def describe(self):
        return self.repo.git.describe('--always', '--tags')

    def hash(self):
        return self.describe().split('-g')[-1]

    def is_dirty(self):
        return self.repo.is_dirty()

    def checkout(self, spec):
        return self.repo.git.checkout(spec)

    def json_ld(self, **dc):
        """
        A repository description in JSON-LD - suitable for inclusion in CLDF metadata.
        """
        return GitRepository(
            self.url or self.dir.name,
            clone=self.dir,
            title=self.__class__.__name__,
            version=self.describe(),
            **{k.replace('dc:', ''): v for k, v in dc.items()},
        ).json_ld()


def get_test_repo(directory, remote_url=None, tags=None, branches=None):
    """
    Since mocking a git repo is somewhat difficult, we provide this function to create a "real"
    git repository for testing.

    :param directory: Parent directory in which a repo called `repo` will be initialized.
    :param remote_url: URL to set for a remote called `origin`.
    :param tags: `list` of tags that should be available in the repo.
    :param branches: `list` of branches that shoud be available in the repo.
    :return: initialized `git.Repo` instance.

    This function may be used for pytest fixtures, e.g.
    ```python
    @pytest.fixture
    def tmprepo(tmpdir):
        return get_test_repo(str(tmpdir))
    ```
    """
    wd = pathlib.Path(directory) / 'repo'
    repo = git.Repo.init(str(wd))

    fname = wd / 'README.md'
    fname.write_text('test', encoding='utf-8')
    repo.index.add([str(fname)])
    repo.index.commit("initial commit")
    repo.git.checkout('master')

    for tag in (tags or []):
        repo.create_tag(tag)

    for branch in (branches or []):
        repo.git.branch(branch)

    if remote_url:
        repo.create_remote('origin', url=remote_url)

    return repo
