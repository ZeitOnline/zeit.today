from zeit.cms.content.interfaces import WRITEABLE_LIVE
import gocept.runner
import logging
import zc.queue
import zeit.cms.content.dav
import zeit.cms.interfaces
import zeit.today.interfaces
import zeit.today.storage
import zope.annotation.interfaces
import zope.app.appsetup.product
import zope.app.locking.interfaces
import zope.cachedescriptors.property
import zope.component
import zope.interface


log = logging.getLogger(__name__)


@zope.interface.implementer(zeit.today.interfaces.ICountStorage)
def yesterday_storage_factory():
    def url_getter():
        config = zope.app.appsetup.product.getProductConfiguration(
            'zeit.today')
        return config['yesterday-xml-url']
    return zeit.today.storage.CountStorage(url_getter)


class LifeTimeCounter(object):

    zope.interface.implements(zeit.today.interfaces.ILifeTimeCounter)
    zope.component.adapts(zeit.cms.interfaces.ICMSContent)

    zeit.cms.content.dav.mapProperties(
        zeit.today.interfaces.ILifeTimeCounter,
        zeit.today.interfaces.LIFETIME_DAV_NAMESPACE,
        ('total_hits', 'first_count', 'last_count'),
        writeable=WRITEABLE_LIVE)

    def __init__(self, context):
        self.context = context


@zope.component.adapter(LifeTimeCounter)
@zope.interface.implementer(zeit.connector.interfaces.IWebDAVProperties)
def webdav_properties(context):
    return zeit.connector.interfaces.IWebDAVProperties(context.context, None)


class UpdateLifetimecounters(object):
    """Aggregates figures from yesterday with the days before."""

    TICKS = 0.025

    def __call__(self):
        self.fill_queue()

        if not self.queue:
            return
        put_back = self.process_one()
        if put_back:
            return 1
        return self.TICKS

    def process_one(self):
        unique_id, count_date, count = self.queue.pull()
        __traceback_info__ = (unique_id,)
        put_back = self._process(unique_id, count_date, count)
        if put_back:
            self.queue.put((unique_id, count_date, count))
        return put_back

    def _process(self, unique_id, count_date, count):
        content = zeit.cms.interfaces.ICMSContent(unique_id, None)
        if content is None:
            log.warning("Could not find %s" % unique_id)
            return False

        try:
            lockable = zope.app.locking.interfaces.ILockable(content)
        except TypeError:
            log.warning("Invalid uniqueId %s" % unique_id)
            return False
        try:
            lockable.lock(timeout=60)
        except zope.app.locking.interfaces.LockingError:
            log.warning("Could not update %s because it is locked." %
                        unique_id)
            return True

        lifetime = zeit.today.interfaces.ILifeTimeCounter(content)

        try:
            if lifetime.first_count is None:
                lifetime.first_count = count_date
                lifetime.total_hits = count
            else:
                lifetime.total_hits += count

            if not lifetime.last_count or lifetime.last_count < count_date:
                lifetime.last_count = count_date
        finally:
            lockable.unlock()
        log.debug("Updated %s (%s hits)" % (unique_id, lifetime.total_hits))
        return False

    def fill_queue(self):
        last_import = getattr(self.queue, 'last_import', None)
        for unique_id in self.storage:
            count_date = self.storage.get_count_date(unique_id)
            if last_import is not None and last_import >= count_date:
                break
            count = self.storage.get_count(unique_id)
            self.queue.put((unique_id, count_date, count))
        else:
            self.queue.last_import = count_date

    @zope.cachedescriptors.property.Lazy
    def storage(self):
        return zope.component.getUtility(zeit.today.interfaces.ICountStorage,
                                         name='yesterday')

    @zope.cachedescriptors.property.Lazy
    def repository(self):
        return zope.component.getUtility(
            zeit.cms.repository.interfaces.IRepository)

    @zope.cachedescriptors.property.Lazy
    def queue(self):
        site = zope.app.component.hooks.getSite()
        annotations = zope.annotation.interfaces.IAnnotations(site)
        try:
            queue = annotations[__name__]
        except KeyError:
            queue = annotations[__name__] = zc.queue.CompositeQueue()
        return queue


def update_lifetime_counters():
    ticks = UpdateLifetimecounters()()
    return ticks


# XXX the principal should go to product config
@gocept.runner.appmain(ticks=3600, principal='zope.hitimporter')
def main():
    return update_lifetime_counters()
