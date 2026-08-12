melody_features
===============

Primary public entry points. Individual feature callables are documented under
:doc:`feature_definitions/index` (and summarised in the interactive
:doc:`/feature_catalogue`). They are also importable from this package root.

Batch extraction
----------------

.. autofunction:: melody_features.get_all_features

.. autofunction:: melody_features.list_available_features

.. autofunction:: melody_features.get_feature_metadata

.. autofunction:: melody_features.to_long_format

Configuration
-------------

.. autoclass:: melody_features.Config
   :members:
   :undoc-members:

.. autoclass:: melody_features.FantasticConfig
   :members:
   :undoc-members:

.. autoclass:: melody_features.IDyOMConfig
   :members:
   :undoc-members:

Corpora helpers
---------------

.. autofunction:: melody_features.get_corpus_path

.. autofunction:: melody_features.list_available_corpora

.. autofunction:: melody_features.load_melodies_from_directory
