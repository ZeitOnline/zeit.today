import pkg_resources
import zeit.cms.testing


product_config = """\
<product-config zeit.today>
    today-xml-url file://{base}/today.xml
</product-config>
""".format(base=pkg_resources.resource_filename(__name__, '.'))

TodayLayer = zeit.cms.testing.ZCMLLayer('ftesting.zcml', product_config=(
    product_config +
    zeit.cms.testing.cms_product_config))


def test_suite():
    return zeit.cms.testing.FunctionalDocFileSuite(
        'README.txt',
        'yesterday.txt',
        layer=TodayLayer
    )
