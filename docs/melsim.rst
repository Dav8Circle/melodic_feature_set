Melsim
======

`Melsim <https://github.com/sebsilas/melsim>`_ is an R package for pairwise
melodic similarity (Silas & Frieler), building on SIMILE (Müllensiefen &
Frieler, 2004). *melody-features* wraps it so you can call melsim from
Python on MIDI files (or, via a legacy helper, on note arrays).

Important notes
---------------

* Melsim is not part of :func:`~melody_features.get_all_features`. Similarity
  is modular: you choose which melodies, measures, and transformations to
  compare.
* You need a working R install, plus the melsim R package and its
  dependencies (the wrapper can install those for you).
* Measure and transformation names are case-sensitive.

Requirements and setup
----------------------

1. Install R and ensure ``Rscript`` is on your ``PATH``.
2. From Python, install the CRAN/GitHub packages the wrapper expects:

.. code-block:: python

   from melody_features.melsim_wrapper.melsim import install_dependencies

   install_dependencies()

This installs required CRAN packages (``dplyr``, ``proxy``, ``dtw``, …) and
``melsim`` from GitHub (``sebsilas/melsim``). To only check what is missing:

.. code-block:: python

   from melody_features.melsim_wrapper.melsim import check_r_packages_installed

   check_r_packages_installed(install_missing=False)
   # raises ImportError listing missing packages; pass install_missing=True to install

Main entry point: ``get_similarity_from_midi``
----------------------------------------------

Prefer :func:`~melody_features.melsim_wrapper.melsim.get_similarity_from_midi`.
It reads MIDI through melsim’s own reader and returns either a single score
or a dictionary of pairwise scores.

Inputs for ``midi_path1``:

* one MIDI path (then ``midi_path2`` is required)
* a directory of ``.mid`` / ``.midi`` files → all pairwise comparisons
* a list of MIDI paths → all pairwise comparisons

Useful parameters:

* ``method`` — string or list of measure names (default ``"opti3"``)
* ``transformation`` — string or list; domain to compare (e.g. ``"pitch"``,
  ``"parsons"``). Required for most measures other than composite ``opti3``;
  defaults to ``"pitch"`` in multi-file runs when omitted
* ``output_file`` — optional path; multi-file results are also written as JSON
  records
* ``batch_size`` / ``r_timeout`` — batch size for R calls and timeout in seconds

Compare two files
~~~~~~~~~~~~~~~~~

.. code-block:: python

   import melody_features as mf
   from melody_features.melsim_wrapper.melsim import get_similarity_from_midi

   files = mf.get_corpus_files("essen", max_files=2)
   a, b = files[0], files[1]

   # Composite measure (no transformation needed)
   score = get_similarity_from_midi(a, b, method="opti3")
   print(f"opti3: {score:.3f}")

   jaccard = get_similarity_from_midi(
       a, b, method="Jaccard", transformation="pitch"
   )
   edit = get_similarity_from_midi(
       a, b, method="edit_sim", transformation="parsons"
   )
   print(f"Jaccard(pitch)={jaccard:.3f}, edit_sim(parsons)={edit:.3f}")

**Returns:** ``float`` for a single pair and a single method.

Pairwise corpus (or directory)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import melody_features as mf
   from melody_features.melsim_wrapper.melsim import get_similarity_from_midi

   files = mf.get_corpus_files("essen", max_files=10)
   results = get_similarity_from_midi(
       files,
       method=["Jaccard", "edit_sim"],
       transformation=["pitch", "parsons"],
       output_file="essen10_similarity.json",
   )

   # results: dict[(file1, file2, method, transformation)] -> float
   for (f1, f2, method, trans), score in list(results.items())[:3]:
       print(f"{f1} vs {f2} | {method}/{trans}: {score:.3f}")

You can pass a directory path instead of a list; every ``.mid`` / ``.midi``
inside is included. You need at least two files.

JSON output (when ``output_file`` is set) is a list of records with
``file1``, ``file2``, ``method``, ``transformation``, and ``similarity``.

Worked example in the repo
~~~~~~~~~~~~~~~~~~~~~~~~~~

``src/melody_features/melsim_wrapper/example.py`` shows the same patterns
(two-file calls, then a small Essen subset with multiple methods and
transforms). Run it from the repository root after
``install_dependencies()``.

Similarity measures
-------------------

Names are case-sensitive:

.. list-table::
   :header-rows: 1
   :widths: 8 40

   * - #
     - Name
   * - 1
     - ``Jaccard``
   * - 2
     - ``Kulczynski2``
   * - 3
     - ``Russel``
   * - 4
     - ``Faith``
   * - 5
     - ``Tanimoto``
   * - 6
     - ``Dice``
   * - 7
     - ``Mozley``
   * - 8
     - ``Ochiai``
   * - 9
     - ``Simpson``
   * - 10
     - ``cosine``
   * - 11
     - ``angular``
   * - 12
     - ``correlation``
   * - 13
     - ``Tschuprow``
   * - 14
     - ``Cramer``
   * - 15
     - ``Gower``
   * - 16
     - ``Euclidean``
   * - 17
     - ``Manhattan``
   * - 18
     - ``supremum``
   * - 19
     - ``Canberra``
   * - 20
     - ``Chord``
   * - 21
     - ``Geodesic``
   * - 22
     - ``Bray``
   * - 23
     - ``Soergel``
   * - 24
     - ``Podani``
   * - 25
     - ``Whittaker``
   * - 26
     - ``eJaccard``
   * - 27
     - ``eDice``
   * - 28
     - ``Bhjattacharyya``
   * - 29
     - ``divergence``
   * - 30
     - ``Hellinger``
   * - 31
     - ``edit_sim_utf8``
   * - 32
     - ``edit_sim``
   * - 33
     - ``Levenshtein``
   * - 34
     - ``sim_NCD``
   * - 35
     - ``const``
   * - 36
     - ``sim_dtw``
   * - 37
     - ``opti3`` (default composite measure)
   * - 38
     - ``count_distinct``
   * - 39
     - ``tversky``
   * - 40
     - ``simple matching``
   * - 41
     - ``braun_blanquet``
   * - 42
     - ``minkowski``
   * - 43
     - ``ukkon``
   * - 44
     - ``sum_common``
   * - 45
     - ``distr_sim``
   * - 46
     - ``stringdot_utf8``
   * - 47
     - ``pmi``
   * - 48
     - ``sim_emd``

Transformations
---------------

A **transformation** is the representation domain used for the comparison
(called “transformation” in melsim):

.. list-table::
   :header-rows: 1
   :widths: 8 28 64

   * - #
     - Name
     - Typical use
   * - 1
     - ``pitch``
     - Raw MIDI pitch sequence
   * - 2
     - ``int``
     - Pitch intervals
   * - 3
     - ``fuzzy_int``
     - Coarse interval classes
   * - 4
     - ``parsons``
     - Up / down / repeat contour (Parsons code)
   * - 5
     - ``pc``
     - Pitch class
   * - 6
     - ``ioi_class``
     - Inter-onset interval classes
   * - 7
     - ``duration_class``
     - Duration classes
   * - 8
     - ``int_X_ioi_class``
     - Joint interval × IOI class
   * - 9
     - ``implicit_harmonies``
     - Implied harmonic context
   * - 10
     - ``ioi``
     - Inter-onset intervals
   * - 11
     - ``phrase_segmentation``
     - Phrase segmentation

For multi-file runs, if you omit ``transformation``, the wrapper defaults to
``["pitch"]``. For ``opti3``, transformation is unused.

Legacy: arrays instead of MIDI paths
------------------------------------

:func:`~melody_features.melsim_wrapper.melsim.get_similarity` accepts pitch /
onset / offset arrays for two melodies. Prefer
``get_similarity_from_midi`` when you have files; the MIDI path is faster and
stays consistent with melsim’s reader.

.. code-block:: python

   import numpy as np
   from melody_features.melsim_wrapper.melsim import get_similarity
   from melody_features.io.midi import load_midi

   m1 = load_midi("a.mid")
   m2 = load_midi("b.mid")
   score = get_similarity(
       np.array(m1.pitches), np.array(m1.starts), np.array(m1.ends),
       np.array(m2.pitches), np.array(m2.starts), np.array(m2.ends),
       method="Jaccard",
       transformation="pitch",
   )

API reference
-------------

Full signatures and docstrings:

* :doc:`api/melsim`

See also
--------

* Upstream package: https://github.com/sebsilas/melsim
* Repo demo: ``src/melody_features/melsim_wrapper/example.py``
* :doc:`installation` — optional R / melsim system requirements
* :doc:`corpora` — bundled MIDI for trials
