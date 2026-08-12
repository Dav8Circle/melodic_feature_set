Installation
============

Requirements
------------

* Python 3.9 or later
* A working install of package dependencies (see ``pyproject.toml`` /
  ``requirements.txt``)

Some optional capabilities have additional system requirements:

* **IDyOM** features require a Common Lisp environment and IDyOM installed
  (via ``py2lispIDyOM``).
* **Melsim** similarity features require R and the melsim R package; they are
  not part of ``get_all_features``.

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

Verify the install
------------------

.. code-block:: python

   import melody_features as mf

   print(len(mf.list_available_features()))
