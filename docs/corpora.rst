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
(Pearce, 2018). This is the **default** reference corpus for
:func:`~melody_features.get_all_features`.

.. code-block:: python

   import melody_features as mf

   print(mf.list_available_corpora())
   path = mf.get_corpus_path("pearce_default_idyom")

Custom corpora
--------------

Point :class:`~melody_features.Config` ``corpus`` (and optionally
``FantasticConfig.corpus`` / ``IDyOMConfig.corpus``) at any directory of
monophonic MIDI files. FANTASTIC
corpus statistics follow the n-gram document-frequency model described in
Müllensiefen (2009). IDyOM can optionally pretrain on the same or a separate
corpus path.
