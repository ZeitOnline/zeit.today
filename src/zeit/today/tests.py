import pkg_resources
import zeit.cms.testing


TodayLayer = zeit.cms.testing.ZCMLLayer('ftesting.zcml')

today_xml_url = 'file://%s' % pkg_resources.resource_filename(
    __name__, 'today.xml')


def test_suite():
    return zeit.cms.testing.FunctionalDocFileSuite(
        'README.txt',
        'yesterday.txt',
        layer=TodayLayer,
        product_config={'zeit.today': {'today-xml-url': today_xml_url}}
    )
