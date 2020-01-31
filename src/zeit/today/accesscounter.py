import six
import six.moves.urllib.parse
import zeit.cms.content.interfaces
import zeit.cms.interfaces
import zope.component
import zope.interface


@zope.component.adapter(zeit.cms.interfaces.ICMSContent)
@zope.interface.implementer(zeit.cms.content.interfaces.IAccessCounter)
class AccessCounter(object):

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
            url = url.encode('utf8')
            return 'http://ccreport.zeit.de/zeit_clickcounter/cc/clicks?%s' % (
                six.moves.urllib.parse.urlencode(dict(url=url)))


@zope.component.adapter(six.string_types[0])
@zope.interface.implementer(zeit.cms.content.interfaces.IAccessCounter)
class UniqueIdAccessCounter(object):

    total_hits = None

    def __init__(self, context):
        self.context = context

    @property
    def hits(self):
        storage = zope.component.getUtility(
            zeit.today.interfaces.ICountStorage)
        return storage.get_count(self.context)
