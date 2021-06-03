from . import _selenium_common


class Map(_selenium_common.PageObject):  # pragma: no cover
    """PageObject to interact with maps."""

    def __init__(self, browser, eid=None, url=None, sleep_ticks=7):
        super(Map, self).__init__(browser, eid or 'map-container', url=url)
        self.sleep(sleep_ticks)

    def test_show_marker(self, index=0):
        self.sleep(2)
        assert not self.e.find_elements_by_class_name('leaflet-popup-content')
        marker = self.e.find_elements_by_class_name('leaflet-marker-icon')
        marker[0].click()
        self.sleep(3)
        assert self.e.find_elements_by_class_name('leaflet-popup-content')

    def test_show_legend(self, name='iconsize'):
        e = self.e.find_element_by_id('legend-%s-container' % name)
        assert not e.is_displayed()
        opener = self.e.find_element_by_id('legend-%s-opener' % name)
        opener.click()
        self.sleep()
        assert e.is_displayed()
        opener.click()  # TODO: better test would be to click somewhere else!
        self.sleep()
        assert not e.is_displayed()
