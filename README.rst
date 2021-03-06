================
README
================

pyterm - terminal output style/positioning control
===================================================

`pyterm` is tool designed to easy the use of colors,
formatting and positioning of text in a terminal without
the use of `curses` mode (curses.initwin).

By default the python `curses` module is used to get code info from the terminal.
If `curses` is not available ANSI codes are used.
The idea to use curses to get terminfo was taken from
blessings [https://pypi.python.org/pypi/blessings/]


Project Details
===============

 - Project management on bitbucket - https://bitbucket.org/schettino72/pyterm
 - Website & docs - http://pythonhosted.org/pyterm


license
=======

The MIT License
Copyright (c) 2012-2013 Eduardo Naufel Schettino

see LICENSE file


developers / contributors
==========================

see AUTHORS file


install
=======

::

 $ pip install pyterm

or download and::

 $ python setup.py install


developemnt setup
==================

The best way to setup an environment to develop `pyterm` itself is to
create a virtualenv...

  pyterm$ virtualen dev
  (dev)pyterm$ dev/bin/activate

install `pyterm` as "editable", and add development dependencies
from `dev_requirements.txt`:

  (dev)pyterm$ pip install --editable .
  (dev)pyterm$ pip install --requirement dev_requirements.txt


Tools required for development:

- merucrial * VCS
- pyflakes * syntax checker
- py.test * unit-tests
- coverage * code coverage
- ansi2html * generate doc
- doit * admin tasks


tests
=======

To run the tests::

  $ py.test

or use doit::

  $ doit


documentation
=============

To generate the documentation::

 $ doit docs


project files
===============

 * pyterm.py -> pyterm implementaion
 * test_pyterm.py -> unit-test (uses py.test)
 * dodo.py -> development tasks management (uses doit)
 * tutorial.py -> sample code demonstrating basic features
 * sample_bar -> example on how to create a progress bar
 * ddemo.py -> generate docs from tutorial

