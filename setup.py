from setuptools import setup, find_packages


setup(
    name='zeit.today',
    version='2.1.1',
    author='gocept, Zeit Online',
    author_email='zon-backend@zeit.de',
    url='http://www.zeit.de/',
    description="",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    license='BSD',
    namespace_packages=['zeit'],
    install_requires=[
        'gocept.lxml',
        'gocept.runner',
        'lxml',
        'requests',
        'setuptools',
        'zc.queue',
        'vivi.core',
        'zope.annotation',
        'zope.app.appsetup',
        'zope.app.locking',
        'zope.app.testing',
        'zope.component',
        'zope.interface',
        'zope.schema',
        'zope.testing',
    ],
    entry_points="""
        [console_scripts]
        run-lifetime-hits-importer=zeit.today.yesterday:main
        clickcounter-to-dav=zeit.today.clickimport:import_to_dav
        """
)
