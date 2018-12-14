from cStringIO import StringIO
import argparse
import gocept.runner
import logging
import os.path
import requests
import zeit.connector.interfaces
import zeit.connector.resource
import zope.app.appsetup.product
import zope.component


log = logging.getLogger(__name__)


@gocept.runner.once(principal=gocept.runner.from_config(
    'zeit.today', 'principal'))
def import_to_dav():
    parser = argparse.ArgumentParser(
        description='Download from URL, upload to DAV')
    parser.add_argument('--source', help='Source URL')
    parser.add_argument('--target', help='Target uniqueId')
    args = parser.parse_args()

    if not (args.source and args.target):
        raise Exception('Both --source and --target are required')

    log.info('Importing %s to %s', args.source, args.target)

    config = zope.app.appsetup.product.getProductConfiguration(
        'zeit.today')
    content = requests.get(args.source, stream=True, auth=(
        config['clickcounter-username'], config['clickcounter-password'])).text

    connector = zope.component.getUtility(zeit.connector.interfaces.IConnector)
    resource = zeit.connector.resource.Resource(
        args.target, os.path.basename(args.target), 'rawxml',
        data=StringIO(content),
        contentType='application/xml')
    connector.add(resource, verify_etag=False)
