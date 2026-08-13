Contributing
============

Fork the repository, implement your change, and open a pull request.
Related features may share one PR; otherwise prefer one feature per PR.

Adding a new feature
--------------------

Features live in ``src/melody_features/feature_definitions/``.
:func:`~melody_features.get_all_features` discovers decorated callables
imported into :mod:`melody_features.features` — it does not use a hard-coded
list. Without correct decoration and export, a feature will not appear in
``get_all_features``, ``list_available_features``, or the catalogue.

1. Implement in the right ``feature_definitions/<family>.py`` module.
2. Decorate with source(s), **type**, and **domain** (below).
3. Add to that module’s ``__all__`` and import it in ``features.py``.
4. Write a NumPy-style docstring and type hints (docs are built from these).
5. Add tests; validate against the upstream implementation when possible
   (see ``tests/test_jsymbolic_validation.py``).
6. Return native Python types (``int``, ``float``, ``list``, ``dict``, …).

Feature decorators
------------------

Defined in :mod:`melody_features.feature_decorators`. Stack one or more
sources, one type, and one domain:

.. code-block:: python

   from melody_features.feature_decorators import absolute, fantastic, jsymbolic, pitch

   @fantastic
   @jsymbolic
   @absolute
   @pitch
   def pitch_range(pitches: list[int]) -> int:
       ...

* **Source:** ``@fantastic``, ``@jsymbolic``, ``@midi_toolbox``, ``@idyom``,
  ``@simile``, ``@partitura``, ``@must``, ``@melsim``, ``@novel``
* **Type:** ``@absolute``, ``@pitch_class``, ``@interval``, ``@contour``,
  ``@tonality``, ``@timing``, ``@metre``, ``@expectation``, ``@complexity``,
  ``@lexical_diversity``, ``@corpus``
* **Domain:** ``@pitch``, ``@rhythm``, or ``@both``

Only public, canonical bindings are collected (aliases like
``ambitus = pitch_range`` are fine; do not re-decorate a second copy).

Docstrings
----------

Sphinx API pages and the interactive catalogue are generated from feature
docstrings and decorator metadata. Use NumPy style:

.. code-block:: python

   def example_feature(pitches: list[int]) -> float:
       """Short description (becomes the catalogue blurb).

       Parameters
       ----------
       pitches : list[int]
           MIDI pitch values

       Returns
       -------
       float
           Meaning of the value

       Notes
       -----
       Optional caveats.

       Citation
       --------
       Author, A. (Year). Title.
       """

The opening paragraph is the catalogue description; annotate the return type
so metadata can label **Descriptor** vs **Sequence**. Cite literature when
the feature comes from a published method; use ``@novel`` for originals.

Tests and docs builds
---------------------

Every pull request should include tests for the change (new coverage or
updates to existing tests). CI runs the suite on each PR; please run it
locally first:

.. code-block:: bash

   pytest
   # smoke-check discovery after adding a feature:
   python -c "import melody_features as mf; assert 'your_feature' in mf.list_available_features()"

If you touch docs or docstrings that feed the API / catalogue, build the
Sphinx site locally as well:

.. code-block:: bash

   pip install -r docs/requirements.txt
   cd docs && make html   # open _build/html/index.html
