Corpora
=======

The package ships with two example corpora.

Essen Folksong Collection
-------------------------

A MIDI conversion of the Essen Folksong Collection (Eck, 2024; Schaffrath,
1995), redistributed under `CC BY-SA 4.0
<https://creativecommons.org/licenses/by-sa/4.0/>`_. See :doc:`license` for
attribution requirements.

Access:

.. code-block:: python

   import melody_features as mf

   path = mf.get_corpus_path("essen")
   files = mf.get_corpus_files("essen", max_files=5)

Pearce (2018) reference corpus
------------------------------

903 Western traditional melodies used by Pearce for IDyOM pretraining
(Pearce, 2018). This is the default reference corpus for
:func:`~melody_features.get_all_features`.

.. code-block:: python

   import melody_features as mf

   print(mf.list_available_corpora())
   path = mf.get_corpus_path("pearce_default_idyom")

Custom reference corpora
------------------------

The bundled corpora are optional. For FANTASTIC corpus statistics and IDyOM
long-term-model pretraining you can point *melody-features* at any directory
of monophonic MIDI files.

Set :class:`~melody_features.Config` ``corpus`` to that directory. Optionally
override just one subsystem with ``FantasticConfig.corpus`` or
``IDyOMConfig.corpus`` (short-term IDyOM runs, ``models=":stm"``, do not use a
pretraining corpus).

.. code-block:: python

   import melody_features as mf

   my_reference = "/path/to/my/monophonic_midis"

   config = mf.Config(
       corpus=my_reference,
       fantastic=mf.FantasticConfig(max_ngram_order=5, phrase_gap=1.5),
       idyom={
           "pitch_ltm": mf.IDyOMConfig(
               target_viewpoints=["cpitch"],
               source_viewpoints=[("cpitch", "cpint", "cpintfref")],
               ppm_order=2,
               models=":ltm",
               # corpus=None → uses Config.corpus (my_reference)
           ),
       },
   )

   # Melodies to analyse can be a different directory from the reference corpus
   results = mf.get_all_features("/path/to/melodies_to_analyse", config=config)

FANTASTIC corpus statistics follow the n-gram document-frequency model in
Müllensiefen (2009). That is step 4 of the FANTASTIC pipeline (tokenize →
count → compare to reference frequencies); see :ref:`fantastic-workflow` in
:doc:`usage`. IDyOM can pretrain on the same path or a separate
``IDyOMConfig.corpus``.

Precomputing FANTASTIC corpus statistics
----------------------------------------

``get_all_features`` builds corpus n-gram statistics from ``Config.corpus``
when needed. For large corpora or repeated runs, precompute once and reuse
(same ``phrase_gap`` / ``n_range`` as your ``FantasticConfig``):

.. code-block:: python

   from melody_features.corpus import (
       make_corpus_stats,
       load_corpus_stats,
   )
   from melody_features.features import get_fantastic_features, get_corpus_features
   from melody_features.io.midi import load_midi

   make_corpus_stats(
       midi_dir="/path/to/reference_midis",
       output_file="my_corpus_stats.json",
       n_range=(1, 5),
       phrase_gap=1.5,
   )
   stats = load_corpus_stats("my_corpus_stats.json")

   melody = load_midi("query.mid")
   fantastic = get_fantastic_features(
       melody, corpus_stats=stats, phrase_gap=1.5, max_ngram_order=5
   )
   corpus_only = get_corpus_features(
       melody, corpus_stats=stats, phrase_gap=1.5, max_ngram_order=5
   )

Related helpers: :func:`~melody_features.corpus.compute_corpus_ngrams`,
:func:`~melody_features.corpus.save_corpus_stats`,
:func:`~melody_features.corpus.make_corpus_stats_from_json`.
