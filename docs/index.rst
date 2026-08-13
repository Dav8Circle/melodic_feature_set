*melody-features*
=================

.. raw:: html

   <img src="_static/melody_features_logo.svg" class="mf-home-logo" width="128" height="128" alt="melody-features" />

*melody-features* consolidates a wide range of computational melody analysis
features into a single Python package for monophonic melodies.

This package provides over 200 features drawn from frameworks including
FANTASTIC, SIMILE, melsim, jSymbolic2, IDyOM, MIDI Toolbox, MUST, and Partitura.

.. note::

   This package is strictly for monophonic melodies. It will not compute
   features for polyphonic music.

Start here
----------

* :doc:`installation` — install from PyPI or from source (including IDyOM)
* :doc:`quickstart` — extract features in a few lines
* :doc:`feature_catalogue` — searchable catalogue of every feature
* :doc:`api/index` — API reference

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: User guide

   installation
   quickstart
   usage
   feature_catalogue
   corpora
   idyom
   melsim
   contour
   contributing
   license

.. toctree::
   :maxdepth: 2
   :caption: API reference

   api/index

Quick example
-------------

.. code-block:: python

   import melody_features as mf

   results = mf.get_all_features(input="path/to/your/midi/files")
   print(results.iloc[:1,].to_json(indent=4, orient="records"))

By default, ``get_all_features`` returns a pandas DataFrame of tabulated features,
using a collection of 903 Western traditional music melodies as the reference
corpus (Pearce, 2018).

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
