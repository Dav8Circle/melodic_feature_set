Contour representations
=======================

Contour features in ``get_all_features`` come from
:mod:`melody_features.feature_definitions.contour`. Under the hood they use
classes in :mod:`melody_features.contour` that expose the full contour vectors
and summary properties — useful when you want intermediates, not only
scalars.

Classes
-------

* :class:`~melody_features.contour.StepContour` — duration-weighted step
  contour (default length 64, FANTASTIC-style), with
  ``global_variation``, ``global_direction``, ``local_variation``
* :class:`~melody_features.contour.InterpolationContour` — interpolated
  contour statistics and ``class_label``
* :class:`~melody_features.contour.PolynomialContour` — polynomial fit;
  ``coefficients`` via :func:`~melody_features.contour.polynomial_contour_coefficients`
* :class:`~melody_features.contour.HuronContour` — Huron contour /
  :func:`~melody_features.contour.get_huron_contour`

Example: step contour
---------------------

Durations are typically in beats/tatums (feature helpers derive them from
``starts`` / ``ends`` / ``tempo``). Constructing the class directly:

.. code-block:: python

   from melody_features.contour import StepContour
   from melody_features.io.midi import load_midi

   melody = load_midi("example.mid")
   # durations in beats (seconds × tempo/60)
   beat = 60.0 / melody.tempo
   durations = [(e - s) / beat for s, e in zip(melody.starts, melody.ends)]
   sc = StepContour(melody.pitches, durations, method="amads")  # or "fantastic"

   print(len(sc.contour))       # 64 by default
   print(sc.global_variation)
   print(sc.global_direction)
   print(sc.local_variation)

For batch scalar features only, prefer
``melody_features.features.get_contour_features(melody)`` or
``mf.get_all_features``.

API reference: :doc:`api/contour`.
