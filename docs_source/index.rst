.. py-etherpad documentation master file, created by
   sphinx-quickstart on Sun Sep  6 21:41:39 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

etherpadlite!
=======================================

`etherpadlite` is a wrapper for Etherpad to make accessing the HTTP API of Etherpad easy. Although wrappers already
exist, it's designed to make access more Pythonic, easy to understand, and have the API well documented so that
developers can view the documentation via an IDE easily.

For example::
   >>> client = EtherpadClient('localhost:9000', 'SECRET_KEY')
   >>> client.create_author('Ganesh Datta', 'internal_id')


Contents:

.. toctree::
   :maxdepth: 2

   client/EtherpadClient


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

