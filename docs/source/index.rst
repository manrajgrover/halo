.. halo documentation master file, created by
   sphinx-quickstart on Mon Apr 15 04:18:11 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: ../../art/halo.png
   :height: 50px
   :align: center

halo
====

.. image:: https://travis-ci.org/manrajgrover/halo.svg?branch=master
   :target: https://travis-ci.org/manrajgrover/halo
   :alt: Travis CI Build Status
.. image:: https://ci.appveyor.com/api/projects/status/wa6t414gltr403ff?svg=true
   :target: https://ci.appveyor.com/project/manrajgrover/halo
   :alt: AppVeyor Build status
.. image:: https://coveralls.io/repos/github/manrajgrover/halo/badge.svg?branch=master
   :target: https://coveralls.io/github/manrajgrover/halo?branch=master
   :alt: Coveralls Status
.. image:: https://img.shields.io/pypi/v/halo.svg
   :target: https://github.com/manrajgrover/halo
   :alt: PyPI
.. image:: https://img.shields.io/badge/awesome-yes-green.svg
   :alt: awesome

Beautiful spinners for terminal, IPython and Jupyter

.. image:: ../../art/doge_spin.svg

Install
-------

.. code-block:: bash

   pip install halo


Usage
-----

.. code-block:: python

   from halo import Halo

   spinner = Halo(text='Loading', spinner='dots')
   spinner.start()

   # Run time consuming work here
   # You can also change properties for spinner as and when you want

   spinner.stop()

Alternatively, you can use halo with Python's ``with`` statement:

.. code-block:: python

   from halo import Halo

   with Halo(text='Loading', spinner='dots'):
	   # Run time consuming work here


Finally, you can use halo as a decorator:

.. code-block:: python

   from halo import Halo

   @Halo(text='Loading', spinner='dots')
   def long_running_function():
	   # Run time consuming work here
	   pass

   long_running_function()

Like it?
--------

🌟 this repo to show support. Let me know you liked it on `Twitter`_.
Also, share the `project`_.

.. _Twitter: https://twitter.com/manrajsgrover
.. _project: https://twitter.com/intent/tweet?url=https%3A%2F%2Fgithub.com%2Fmanrajgrover%2Fhalo&via=manrajsgrover&text=Checkout%20%23halo%20-%20a%20beautiful%20%23terminal%20%23spinners%20library%20for%20%23python&hashtags=github%2C%20pypi

Related
-------

* `py-spinners`_ - Spinners in Python
* `py-log-symbols`_ - Log Symbols in Python
* `ora`_ - Elegant terminal spinners in JavaScript (inspiration behind this project)

.. _py-spinners: https://github.com/manrajgrover/py-spinners
.. _py-log-symbols: https://github.com/manrajgrover/py-log-symbols
.. _ora: https://github.com/sindresorhus/ora

License
-------

`MIT`_ © Manraj Singh

.. _MIT: https://github.com/manrajgrover/halo/blob/master/LICENSE

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   modules

.. toctree::
   :maxdepth: 2
   :caption: About

   about/faqs
   about/DEVELOPMENT
   Contributing <about/CONTRIBUTING>
