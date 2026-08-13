Installation
============

Requirements
------------

* Python 3.9 or later
* A working install of package dependencies (see ``pyproject.toml`` /
  ``requirements.txt``)

Some optional capabilities have additional system requirements:

* IDyOM features require SBCL (Steel Bank Common Lisp), Quicklisp, and the
  IDyOM Lisp package (used via ``py2lispIDyOM``). See :ref:`install-idyom`.
* Melsim similarity features require R and the melsim R package; they are
  not part of ``get_all_features``. See :doc:`melsim`.

Install from PyPI
-----------------

.. code-block:: bash

   pip install melody-features

Install from source
-------------------

.. code-block:: bash

   git clone https://github.com/dmwhyatt/melody-features.git
   cd melody-features
   pip install -e .

Development install
-------------------

For running tests and building documentation:

.. code-block:: bash

   pip install -e .
   pip install -r requirements.txt
   pip install -r docs/requirements.txt

Verify the Python package
-------------------------

.. code-block:: python

   import melody_features as mf

   print(len(mf.list_available_features()))

You can run :func:`~melody_features.get_all_features` without IDyOM by passing
``skip_idyom=True``.

.. _install-idyom:

Installing IDyOM
----------------

By default ``get_all_features`` runs IDyOM. Install it once on the machine
(Linux/macOS), then verify from Python.

What the installer sets up
~~~~~~~~~~~~~~~~~~~~~~~~~~

The bundled script ``src/melody_features/install_idyom.sh`` installs:

* SBCL and SQLite tooling
* Quicklisp under ``~/quicklisp``
* IDyOM sources under ``~/quicklisp/local-projects/idyom``
* Data dirs under ``~/idyom/`` (including ``db/database.sqlite``)
* An IDyOM block in ``~/.sbclrc`` (marker ``;; IDyOM Configuration (v3)``)

Run the installer
~~~~~~~~~~~~~~~~~

From a clone of this repository:

.. code-block:: bash

   chmod +x src/melody_features/install_idyom.sh
   ./src/melody_features/install_idyom.sh

Or from Python (runs the same script):

.. code-block:: python

   from melody_features.idyom.interface import install_idyom

   install_idyom()

Verify
~~~~~~

.. code-block:: python

   from melody_features.idyom.interface import is_idyom_installed

   print(is_idyom_installed())  # True when SBCL, DB, sources, and .sbclrc look OK

``is_idyom_installed`` checks for ``sbcl`` on ``PATH``,
``~/idyom/db/database.sqlite``, ``~/quicklisp/local-projects/idyom``, and the
``;; IDyOM Configuration (v3)`` marker in ``~/.sbclrc``.

If installation is incomplete, ``get_all_features`` (without ``skip_idyom``)
and :func:`~melody_features.idyom.interface.run_idyom` may prompt to install
or fail in non-interactive environments — prefer installing ahead of time.

More on defaults, viewpoints, and calling IDyOM outside the feature pipeline:
:doc:`idyom`.
