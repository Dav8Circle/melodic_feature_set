IDyOM
=====

`IDyOM <https://github.com/mtpearce/idyom>`_ (Pearce, 2005) is used for expectation /
information-content style features. *melody-features* drives it through
``py2lispIDyOM``.

Setup (install and verify) is in :ref:`install-idyom`. Config options and
linked viewpoints for ``get_all_features`` are in :doc:`usage`. This page
covers default runs, standalone IDyOM, and how they relate.

Default runs inside ``get_all_features``
----------------------------------------

When you omit ``config``, the package runs four IDyOM jobs. Dict keys become
labels in the wide-format output:

.. list-table::
   :header-rows: 1
   :widths: 18 12 28 42

   * - Label
     - ``models``
     - Target
     - Sources
   * - ``pitch_stm``
     - ``:stm``
     - ``cpitch``
     - linked ``(cpitch, cpint, cpintfref)``
   * - ``pitch_ltm``
     - ``:ltm``
     - ``cpitch``
     - linked ``(cpitch, cpint, cpintfref)``
   * - ``rhythm_stm``
     - ``:stm``
     - ``onset``
     - ``ioi``, ``ioi-ratio``
   * - ``rhythm_ltm``
     - ``:ltm``
     - ``onset``
     - ``ioi``, ``ioi-ratio``

* STM runs do not use a pretraining corpus.
* LTM runs use ``Config.corpus`` (default: bundled Pearce 2018 set).
* Default ``ppm_order`` is ``None`` (IDyOM / py2lispIDyOM default order).

To change or replace these, pass ``Config(idyom={...})`` with your own named
:class:`~melody_features.IDyOMConfig` entries — see :doc:`usage`.

Skip IDyOM entirely with ``skip_idyom=True``.

Wide-format column names
~~~~~~~~~~~~~~~~~~~~~~~~

Each named IDyOM run contributes columns under the ``idyom`` family. Internally
the pipeline stores keys like
``idyom_<label>_features.<metric>``; after renaming for the DataFrame they
become:

.. code-block:: text

   idyom.<label>_<metric>

With the default labels, mean information content appears as:

.. code-block:: text

   idyom.pitch_stm_mean_information_content
   idyom.pitch_ltm_mean_information_content
   idyom.rhythm_stm_mean_information_content
   idyom.rhythm_ltm_mean_information_content

If you use custom dict keys (for example ``"pitch_stm"`` and ``"rhythm_ltm"``
in :doc:`usage`), you get columns such as
``idyom.pitch_stm_mean_information_content`` and
``idyom.rhythm_ltm_mean_information_content``.

There is a second, related set under the expectation family for the four
default mean-information-content helpers
(``expectation.pitch_stm_mean_information_content``, and so on). Those are
static feature definitions that read cached IDyOM results; the ``idyom.*``
columns above are the dynamic per-config batch outputs. Custom config labels
only appear under ``idyom.<label>_…``.

In long format, each of those names is a ``feature_name`` row. Dynamic
``idyom.*`` names may not have a full static metadata row in
:func:`~melody_features.get_feature_metadata`; the reshape helpers still fill
family/source fallbacks.

Standalone ``run_idyom``
------------------------

For information-content experiments that do not need the full feature DataFrame, call
:func:`~melody_features.idyom.interface.run_idyom` on a directory of MIDI
files:

.. code-block:: python

   from melody_features.idyom.interface import is_idyom_installed, run_idyom

   assert is_idyom_installed(), "Install IDyOM first (see Installation)"

   dat_path = run_idyom(
       input_path="/path/to/midi_dir",
       pretraining_path=None,          # or a corpus directory for LTM
       output_dir="idyom_out",
       description="my experiment",
       target_viewpoints=["cpitch"],
       source_viewpoints=[("cpint", "cpintfref")],
       models=":both",                 # ":stm" | ":ltm" | ":both"
       ppm_order=2,
       detail=3,
   )
   print(dat_path)  # path to the IDyOM .dat output when successful

Notes:

* ``input_path`` should be a directory of ``.mid`` / ``.midi`` (or ``.krn``).
* Omit ``pretraining_path`` for no LTM pretraining; set it to a corpus
  directory when you want long-term models trained on that set.
* Viewpoints follow the same rules as ``IDyOMConfig`` (atomic strings; linked
  viewpoints as tuples). Valid names are in
  ``melody_features.idyom.config.VALID_VIEWPOINTS``.
* ``get_all_features`` uses higher-level runners that also apply
  ``Config.key_estimation`` when writing temporary MIDI for IDyOM; prefer
  that path when you need package feature columns.

Key estimation and IDyOM
------------------------

``Config.key_estimation`` affects temporary MIDI written for IDyOM (and
tonality features). See :ref:`key-estimation` in :doc:`usage`.
