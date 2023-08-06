
This package helps in daemonize your Python3 projects.

Installation
------------

You can install directly after cloning:

use the Python package:

.. code-block:: bash

  $ pip install --user mattdaemon_py3

Features
--------

- superuser (root) enforcement. Your script either requires it or it doesn't. You choose!

  -  If these checks fail, the script will exit with a status of **1**.

- Uses the double-fork magic of UNIX to daemonize.

Dependencies
------------

- `Python`_ 3

Notes
-----

- This is designed for CLI scripts, because it decouples from the parent environment and all.
- Includes annoying messages when you use root to run a script.
- ``daemon.start()`` and ``daemon.stop()`` don't print messages. You'll have to decide what to print, if anything.
- MIT Licensed code, so you're free to do whatever you want with this. Sell it, steal it, improve it, anything at all!

Running / Usage
---------------

- Add the script to your dependencies, it's on pypi! (``pip install mattdaemon``)
- Documentation is available on `readthedocs`_, so check there for usage.

Usage
-----


License
~~~~~~~
MIT License
~~~~~~~~~~~


.. code:: rst

    |MIT license|

    .. image:: https://img.shields.io/badge/License-MIT-blue.svg

Authors
~~~~~~~
Maurya Allimuthu ( catchmaurya@gmail.com )
Santosh Bhaskar ( justsbk28@gmail.com )

Contact
~~~~~~~
Please submit an issue if you encounter a bug and please email any questions or requests to @authors
