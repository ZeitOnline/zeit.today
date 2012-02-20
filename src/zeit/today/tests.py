# Copyright (c) 2007-2012 gocept gmbh & co. kg
# See also LICENSE.txt

import os
import unittest
import zeit.cms.testing


TodayLayer = zeit.cms.testing.ZCMLLayer(
    os.path.join(os.path.dirname(__file__), 'ftesting.zcml'),
    __name__, 'TodayLayer', allow_teardown=True)

today_xml_url = 'file://%s' % os.path.join(
    os.path.dirname(__file__), 'today.xml')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(zeit.cms.testing.FunctionalDocFileSuite(
        'README.txt',
        'yesterday.txt',
        layer=TodayLayer,
        product_config={'zeit.today': {'today-xml-url': today_xml_url}}
    ))
    return suite
