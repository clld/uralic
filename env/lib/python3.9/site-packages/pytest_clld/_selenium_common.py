import time

SLEEP_TICK = 0.3


def sleep(n=1, tick=SLEEP_TICK):
    time.sleep(tick * n)


class PageObject(object):  # pragma: no cover
    """Virtual base class for objects we wish to interact with in selenium tests."""

    sleep = staticmethod(sleep)

    def __init__(self, browser, eid, url=None):
        """Initialize.

        :param browser: The selenium webdriver instance.
        :param eid: Element id of a dom object.
        :param url: If specified, we first navigate to this url.
        """
        self.browser = browser
        if url:
            self.browser.get(url)
        self.eid = eid

    @property
    def e(self):
        try:
            return self.browser.find_element_by_id(self.eid)
        except Exception:
            return self.browser.find_element_by_class_name(self.eid)
