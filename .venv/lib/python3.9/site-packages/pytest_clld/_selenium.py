import threading

from selenium import webdriver
from wsgiref.simple_server import WSGIRequestHandler, make_server

from . import _selenium_common, _selenium_map, _selenium_datatable


class Handler(WSGIRequestHandler):
    """Logging HTTP request handler."""

    def log_message(self, *args, **kw):
        return


class ServerThread(threading.Thread):
    """Run WSGI server on a background thread.

    Pass in WSGI app object and serve pages from it for Selenium browser.
    """

    handler_cls = Handler

    def __init__(self, app, host='127.0.0.1:8880'):
        threading.Thread.__init__(self)
        self.app = app
        self.host, self.port = host.split(':')
        self.srv = None

    def run(self):
        """Open WSGI server to listen to HOST_BASE address."""
        self.srv = make_server(self.host, int(self.port), self.app, handler_class=self.handler_cls)
        try:
            self.srv.serve_forever()
        except Exception:
            import traceback
            traceback.print_exc()
            # Failed to start
            self.srv = None

    def quit(self):
        if self.srv:
            self.srv.shutdown()


class Selenium(object):

    sleep = staticmethod(_selenium_common.sleep)

    server_cls = ServerThread

    def __init__(self, app, host, downloads):
        self.host = host
        self.downloads = downloads
        profile = webdriver.firefox.firefox_profile.FirefoxProfile()
        profile.set_preference('browser.download.folderList', 2)
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.download.dir', downloads)
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/x-bibtex')
        self.browser = webdriver.Firefox(firefox_profile=profile)
        self.server = self.server_cls(app, host)

    def url(self, path):
        return 'http://%s%s' % (self.host, path)

    def get_page(self, eid=None, url=None):
        if url is not None:
            url = self.url(url)
        return _selenium_common.PageObject(self.browser, eid=eid, url=url)

    def get_map(self, path, eid=None, sleep_ticks=7):
        return _selenium_map.Map(self.browser, eid=eid, url=self.url(path), sleep_ticks=sleep_ticks)

    def get_datatable(self, path, eid=None):
        return _selenium_datatable.DataTable(self.browser, eid=eid, url=self.url(path))
