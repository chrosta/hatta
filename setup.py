#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools


setuptools.setup(
    name='Hatta',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    version='2.0',
    license='GNU General Public License (GPL)',
    author='Radomir Dopieralski',
    author_email='hatta@sheep.art.pl',
    keywords='wiki wsgi web mercurial repository',
    packages=setuptools.find_packages('.', exclude=('tests',)),
    install_requires=[
        'werkzeug >=1.0',
        'mercurial >=5.4',
        'dulwich>=0.20.23',
        'jinja2',
        'whoosh',
    ],
    tests_require=['pytest', 'lxml', 'pygments'],
    data_files=[
        ('share/locale/ar/LC_MESSAGES', ['locale/ar/LC_MESSAGES/hatta.mo']),
        ('share/locale/cs/LC_MESSAGES', ['locale/cs/LC_MESSAGES/hatta.mo']),
        ('share/locale/da/LC_MESSAGES', ['locale/da/LC_MESSAGES/hatta.mo']),
        ('share/locale/de/LC_MESSAGES', ['locale/de/LC_MESSAGES/hatta.mo']),
        ('share/locale/el/LC_MESSAGES', ['locale/el/LC_MESSAGES/hatta.mo']),
        ('share/locale/es/LC_MESSAGES', ['locale/es/LC_MESSAGES/hatta.mo']),
        ('share/locale/et/LC_MESSAGES', ['locale/et/LC_MESSAGES/hatta.mo']),
        ('share/locale/fi/LC_MESSAGES', ['locale/fi/LC_MESSAGES/hatta.mo']),
        ('share/locale/fr/LC_MESSAGES', ['locale/fr/LC_MESSAGES/hatta.mo']),
        ('share/locale/hu/LC_MESSAGES', ['locale/hu/LC_MESSAGES/hatta.mo']),
        ('share/locale/ja/LC_MESSAGES', ['locale/ja/LC_MESSAGES/hatta.mo']),
        ('share/locale/lt/LC_MESSAGES', ['locale/lt/LC_MESSAGES/hatta.mo']),
        ('share/locale/pl/LC_MESSAGES', ['locale/pl/LC_MESSAGES/hatta.mo']),
        ('share/locale/ru/LC_MESSAGES', ['locale/ru/LC_MESSAGES/hatta.mo']),
        ('share/locale/sv/LC_MESSAGES', ['locale/sv/LC_MESSAGES/hatta.mo']),
        ('share/locale/vi/LC_MESSAGES', ['locale/vi/LC_MESSAGES/hatta.mo']),
        ('share/doc/hatta/examples', [
            'examples/hatta.fcgi',
            'examples/hatta.gzip.fcgi',
            'examples/hatta.wsgi',
            'examples/extend_parser.py'
        ]),
    ],
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'Topic :: Communications',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
    ],
)
