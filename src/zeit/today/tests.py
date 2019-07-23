import pkg_resources
import zeit.cms.testing


product_config = """\
<product-config zeit.today>
    today-xml-url file://{base}/today.xml
</product-config>
""".format(base=pkg_resources.resource_filename(__name__, '.'))

CONFIG_LAYER = zeit.cms.testing.ProductConfigLayer(product_config, bases=(
    zeit.cms.testing.CONFIG_LAYER,))
ZCML_LAYER = zeit.cms.testing.ZCMLLayer(bases=(CONFIG_LAYER,))
ZOPE_LAYER = zeit.cms.testing.ZopeLayer(bases=(ZCML_LAYER,))


def test_suite():
    return zeit.cms.testing.FunctionalDocFileSuite(
        'README.txt',
        'yesterday.txt',
        layer=ZOPE_LAYER)
