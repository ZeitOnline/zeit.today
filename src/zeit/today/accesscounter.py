# Copyright (c) 2008-2009 gocept gmbh & co. kg
# See also LICENSE.txt

import urllib
import zeit.cms.content.interfaces
import zeit.cms.interfaces
import zope.component
import zope.interface


class AccessCounter(object):

    zope.interface.implements(zeit.cms.content.interfaces.IAccessCounter)
    zope.component.adapts(zeit.cms.interfaces.ICMSContent)

    def __init__(self, context):
        self.context = context

    @property
    def hits(self):
        storage = zope.component.getUtility(
            zeit.today.interfaces.ICountStorage)
        return storage.get_count(self.context.uniqueId)

    @property
    def total_hits(self):
        lifetime = zeit.today.interfaces.ILifeTimeCounter(self.context, None)
        if lifetime is None:
            return None
        if not lifetime.total_hits:
            return None

        # The lifetime total hits do not contain today's hits, but we want to
        # take today's hits into account.
        today = self.hits
        if today is None:
            today = 0

        return lifetime.total_hits + today

    @property
    def detail_url(self):
        if self.context.uniqueId.startswith('http://xml.zeit.de/'):
            url = self.context.uniqueId.replace('http://xml.', 'www.', 1)
        elif self.context.uniqueId.startswith('http://video.zeit.de/'):
            url = self.context.uniqueId.replace('http://video.zeit.de/',
                                                'http://www.zeit.de/video/', 1)
        else:
            url = None
        if url:
            return 'http://ccreport.zeit.de/zeit_clickcounter/cc/clicks?%s' % (
                urllib.urlencode(dict(url=url)))


class UniqueIdAccessCounter(object):

    zope.interface.implements(zeit.cms.content.interfaces.IAccessCounter)
    zope.component.adapts(basestring)

    total_hits = None

    def __init__(self, context):
        self.context = context

    @property
    def hits(self):
        storage = zope.component.getUtility(
            zeit.today.interfaces.ICountStorage)
        return storage.get_count(self.context)
