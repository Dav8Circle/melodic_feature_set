Quick start
===========

These docs use the conventional short import:

.. code-block:: python

   import melody_features as mf

Batch feature extraction
------------------------

The main entry point is :func:`melody_features.get_all_features`.

**Returns:** :class:`pandas.DataFrame`

**Accepts as** ``input``:

* a directory of MIDI files (``str`` / ``Path``)
* a single MIDI path
* a ``list`` of MIDI paths
* a ``list`` of :class:`~melody_features.core.representations.Melody` objects

.. code-block:: python

   import melody_features as mf
   import pandas as pd

   results = mf.get_all_features(input="path/to/your/midi/files", skip_idyom=True)
   assert isinstance(results, pd.DataFrame)
   print(results.iloc[:1,].to_json(indent=4, orient="records"))

By default this is **wide** format: one row per melody, one column per feature
(namespaced as ``{family}.{feature_name}``, e.g. ``absolute_pitch.pitch_range``).
Pass ``long_format=True`` for one row per melody/feature. Minimal sample
tables for both shapes are in :doc:`usage`.

A notebook walkthrough is available in ``notebooks/example.ipynb``.
For signatures, return types, and configuration detail, see :doc:`usage`.

Long format
-----------

Pass ``long_format=True`` for one row per melody/feature combination.

**Returns:** :class:`pandas.DataFrame` with columns including
``melody_num``, ``melody_id``, ``feature_name``, ``value``, and (by default)
joined metadata (``family``, ``source``, ``domain``, ``type``, …).

.. code-block:: python

   import melody_features as mf

   long_results = mf.get_all_features(
       input="path/to/your/midi/files",
       skip_idyom=True,
       long_format=True,       # tidy long table
       join_metadata=True,     # default; set False for minimal columns
   )

   descriptors = long_results[
       (long_results["type"] == "Descriptor")
       & (long_results["source"].str.contains("jSymbolic", na=False))
   ]

You can also reshape an existing wide DataFrame:

.. code-block:: python

   import melody_features as mf

   wide_results = mf.get_all_features("path/to/your/midi/files", skip_idyom=True)
   long_results = mf.to_long_format(wide_results)   # -> DataFrame
   metadata = mf.get_feature_metadata()             # -> DataFrame

Individual features
-------------------

:func:`~melody_features.io.midi.load_midi` loads **one** file and returns a
single :class:`~melody_features.core.representations.Melody` **or** ``None`` (never a list).

Feature functions take note lists rather than a ``Melody`` argument, but
``Melody`` exposes those lists as attributes (``melody.pitches``,
``melody.starts``, …), so you load once and pass attributes through:

.. code-block:: python

   import melody_features as mf
   from melody_features.io.midi import load_midi

   midi_path = mf.get_corpus_files("essen", max_files=1)[0]  # list[Path] -> Path
   melody = load_midi(midi_path)                             # Optional[Melody]
   if melody is None:
       raise RuntimeError(f"could not load {midi_path}")

   span = mf.pitch_range(melody.pitches)                     # list[int] -> int
   print(span)

Use :func:`melody_features.list_available_features` (returns ``list[str]``, or
``list[dict]`` when ``detailed=True``) to browse the catalogue. Features that
need corpus statistics or IDyOM are easiest via ``mf.get_all_features`` and a
:class:`~melody_features.Config` (including multiple named IDyOM runs — see
:doc:`usage`).

Next steps
----------

* :doc:`usage` — loading helpers, Melody attributes, Config, output shapes
* :doc:`feature_catalogue` — searchable table of all features
* :doc:`api/index` — API reference
