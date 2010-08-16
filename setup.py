from setuptools import setup, find_packages

setup(
    name='zeit.today',
    version='1.21.1dev',
    author='gocept',
    author_email='mail@gocept.com',
    url='https://svn.gocept.com/repos/gocept-int/zeit.cms',
    description="""\
""",
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data = True,
    zip_safe=False,
    license='gocept proprietary',
    namespace_packages = ['zeit'],
    install_requires=[
        'gocept.lxml',
        'gocept.runner',
        'lxml',
        'setuptools',
        'zc.queue',
        'zeit.cms>=1.19',
        'zope.annotation',
        'zope.app.appsetup',
        'zope.app.locking',
        'zope.app.testing',
        'zope.component',
        'zope.interface',
        'zope.schema',
        'zope.testing',
    ],
    entry_points = """
        [console_scripts]
        run-lifetime-hits-importer = zeit.today.yesterday:main
        """
)
