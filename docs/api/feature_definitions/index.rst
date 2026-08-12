Feature definitions
===================

Atomic feature callables, grouped by family. Pages use short family names
(e.g. ``absolute_pitch``); the underlying module is
``melody_features.feature_definitions.<family>``. Each function is also
importable via ``import melody_features as mf`` (for example ``mf.pitch_range``).

These pages are the formal API reference for every feature. The interactive
:doc:`/feature_catalogue` summarises the same catalogue for browsing.

.. toctree::
   :maxdepth: 1

   absolute_pitch
   pitch_class
   pitch_interval
   contour
   timing
   inter_onset_interval
   tonality
   metre
   expectation
   complexity
   lexical_diversity
   corpus
