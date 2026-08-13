Feature catalogue
=================

Browse every documented feature with search and filters (domain, category,
implementation, and type). Feature names link to their source definitions on
GitHub when available.

.. feature-catalogue::

Sources
-------

* **FANTASTIC**: Müllensiefen, D. (2009). Feature ANalysis Technology Accessing STatistics (In a Corpus): Technical Report v1.5
* **jSymbolic**: McKay, C., & Fujinaga, I. (2006). jSymbolic: A Feature Extractor for MIDI Files
* **IDyOM**: Pearce, M. T. (2005). The construction and evaluation of statistical models of melodic structure in music perception and composition
* **MIDI Toolbox**: Eerola, T., & Toiviainen, P. (2004). MIDI Toolbox: MATLAB Tools for Music Research
* **MUST**: Clemente, A., Vila-Vidal, M., Pearce, M. T., et al. (2020). A Set of 200 Musical Stimuli Varying in Balance, Contour, Symmetry, and Complexity
* **Melsim**: Silas, S., & Frieler, K. (n.d.). Melsim: Framework for calculating tons of melodic similarities
* **SIMILE**: Müllensiefen, D., & Frieler, K. (2006). The Simile algorithms documentation 0.3
* **Partitura**: Cancino-Chacón, C. (2022). Partitura
* **Novel**: Custom features introduced in this package

Feature types
-------------

* **Descriptor**: Returns a single scalar value (``int``, ``float``, ``bool``)
* **Sequence**: Returns a collection (``list``, ``tuple``, ``dict``, etc.)

Programmatic metadata
---------------------

.. code-block:: python

   import melody_features as mf

   metadata = mf.get_feature_metadata()
   names = mf.list_available_features()

Full function signatures and docstrings for every feature are also in the API
reference under :doc:`api/feature_definitions/index`.
