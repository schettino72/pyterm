#! /usr/bin/env python

from distutils.core import setup


long_description = """
`pyterm` is tool designed to easy the use of colors,
formatting and positioning of text in a terminal without
the use of `curses`.

website/docs: `http://pythonhosted.org/pyterm <http://pythonhosted.org/pyterm>`_

source/issues: `https://bitbucket.org/schettino72/pyterm <https://bitbucket.org/schettino72/pyterm>`_
"""


setup(name = 'pyterm',
      description = 'pyterm - terminal output style/positioning control',
      version = '0.1.0',
      license = 'MIT',
      author = 'Eduardo Naufel Schettino',
      author_email = 'schettino72@gmail.com',
      url = 'http://pythonhosted.org/pyterm',

      classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Terminals',
        'Topic :: Utilities',
        ],

      keywords = ['terminal', 'tty', 'color', 'console'],
      py_modules = ['pyterm'],
      long_description = long_description,
    )
