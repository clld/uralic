import shutil
import logging
import tempfile
import functools

import pytest
import sqlalchemy as sa
from pyramid import paster

from . import _app, _selenium

APPINI = 'development.ini'


def pytest_addoption(parser):
    """The app ini file to be used for testing (should be specified)."""
    parser.addoption('--appini', default=APPINI, help='app conf')


@pytest.fixture
def env(data, pytestconfig):
    env = paster.bootstrap(pytestconfig.getoption('appini'))
    env['request'].translate = lambda s, **kw: s
    return env


@pytest.fixture
def app(env):
    return _app.ExtendedTestApp(env['app'])


@pytest.fixture
def request_factory(env):
    return functools.partial(_app.request, env)


@pytest.fixture
def utility_factory(env):
    return functools.partial(_app.utility, env)


@pytest.fixture
def dbschema(scope='session'):
    from clld.db.meta import Base

    engine = sa.create_engine('sqlite://')
    result = []

    def dump(sql):
        result.append(sql.compile(dialect=engine.dialect).string)

    mock_engine = sa.create_engine(engine.url, strategy='mock', executor=dump)
    Base.metadata.create_all(mock_engine, checkfirst=False)
    return ''.join(result)


@pytest.fixture(scope='session')
def db(url='sqlite://'):
    from clld.db.meta import Base, DBSession

    engine = sa.create_engine(url)
    Base.metadata.create_all(bind=engine)
    DBSession.configure(bind=engine)

    yield engine

    DBSession.close()


@pytest.fixture(scope='session')
def data(db):
    yield db


@pytest.fixture(scope='module')
def selenium(pytestconfig, logger='selenium.webdriver.remote.remote_connection'):
    selenium_logger = logging.getLogger(logger)
    selenium_logger.setLevel(logging.WARNING)

    appini = pytestconfig.getoption('appini')
    app = paster.bootstrap(appini)['app']
    res = _selenium.Selenium(app, '127.0.0.1:8880', tempfile.mkdtemp())
    res.server.start()
    res.sleep()
    assert res.server.srv

    yield res

    res.browser.quit()
    res.server.quit()
    shutil.rmtree(res.downloads)
