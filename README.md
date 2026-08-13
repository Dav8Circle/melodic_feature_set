# *melody-features*

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=1023590972)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16894207.svg)](https://doi.org/10.5281/zenodo.16894207)
[![Tests](https://github.com/dmwhyatt/melody-features/actions/workflows/test.yml/badge.svg)](https://github.com/dmwhyatt/melody-features/actions)
[![Coverage](https://codecov.io/gh/dmwhyatt/melody-features/graph/badge.svg)](https://codecov.io/gh/dmwhyatt/melody-features)

## Overview

This is a Python package designed to facilitate the use of many different melody analysis tools. 

The main goal of this package is to consolidate a wide range of features from the computational melody analysis literature
into a single place, in a single language.

This package is strictly for monophonic melodies - it will not compute any features for polyphonic music!

## Included Contributions

Included in the package are contributions from:

- **FANTASTIC** (Müllensiefen, 2009)
- **SIMILE** (Müllensiefen & Frieler, 2006)
- **melsim** (Silas & Frieler, n.d.)
- **jSymbolic2** (McKay & Fujinaga, 2006)
- **IDyOM** (Pearce, 2005)
- **MIDI Toolbox** (Eerola & Toiviainen, 2004)
- **MUST** (Clemente et al., 2020)
- **Partitura** (Cancino-Chacón, 2022)



## Melody Features Summary

This package provides over **200 features** from various computational melody analysis frameworks. For installation, usage, API reference, and a comprehensive interactive feature table with search and sorting, see the documentation:

**[Documentation](https://dmwhyatt.github.io/melody-features/)** (feature catalogue: [Feature catalogue](https://dmwhyatt.github.io/melody-features/feature_catalogue.html))

The interactive catalogue allows you to:

- **Search** features by name, implementation, or description
- **Filter** by domain, category, implementation, or type
- **Sort** by any column (Name, Implementation, Type, etc.)
- **Browse** all features with detailed descriptions and references



## Installation

```bash

# using pip
pip install melody-features

# or clone the repository
git clone https://github.com/dmwhyatt/melody-features.git
cd melody-features

# Install in development mode
pip install -e .
```



## Quick Start

The feature set can be easily accessed using the top-level function `get_all_features`. These docs use the short import `import melody_features as mf`:

```python
import melody_features as mf

# Extract features from a directory of MIDI files, a single MIDI file
# or a list of paths to MIDI files
results = mf.get_all_features(input="path/to/your/midi/files")

# Print the result of all feature calculations
print(results.iloc[:1,].to_json(indent=4, orient="records"))

```

By default, this function will produce a Pandas DataFrame containing the tabulated features, using the a collection of 903 Western traditional music melodies as the reference corpus, from Pearce (2018).

This function can be customised in a number of ways, please see `notebooks/example.ipynb` for a detailed breakdown.

### Long format

By default `get_all_features` returns one row per melody, with one column per feature (`{family}.{feature_name}`, e.g. `absolute_pitch.pitch_range`). Pass `long_format=True` to instead get a tidy long-format DataFrame with one row per melody/feature combination.

```python
import melody_features as mf

long_results = mf.get_all_features(input="path/to/your/midi/files", long_format=True)
# columns: melody_num, melody_id, feature_name, family, source, domain, type, value, description, notes, references

# e.g. keep only descriptor-type features from jSymbolic
descriptors = long_results[
    (long_results["type"] == "Descriptor") & (long_results["source"].str.contains("jSymbolic"))
]

# group by source or family, e.g. to see which sources contribute most features
long_results.groupby("family")["feature_name"].nunique()
```

By default, feature metadata (source, family, domain, type, description) is joined onto the long DataFrame automatically. Pass `join_metadata=False` to skip this and get a minimal `melody_num, melody_id, feature_name, value` table instead.

You can also reshape an existing wide-format DataFrame (for example one you've already saved to CSV) with `to_long_format`, and fetch the metadata table on its own with `get_feature_metadata()`:

```python
import melody_features as mf

wide_results = mf.get_all_features(input="path/to/your/midi/files")
long_results = mf.to_long_format(wide_results)

metadata = mf.get_feature_metadata()  # feature_name, family, source, domain, type, description, notes, references
```



## Loading melodies and computing individual features

Besides the batch pipeline, you can load a `Melody` and call feature functions from the package root. Use `list_available_features()` to browse the full catalogue.

```python
import melody_features as mf
from melody_features.io.midi import load_midi

midi_path = mf.get_corpus_files("essen", max_files=1)[0]
melody = load_midi(str(midi_path))
print(mf.pitch_range(melody.pitches))
```

Some features (FANTASTIC corpus statistics, IDyOM) need extra configuration or reference corpora; it is easiest to use `get_all_features` with `Config` when you need those.

## Melsim

Melsim is an R package for computing similarity between two or more melodies (Silas & Frieler; [melsim on GitHub](https://github.com/sebsilas/melsim)). *melody-features* includes a Python wrapper; see the [Melsim docs page](docs/melsim.rst) (or the built HTML site) for setup, measures, transformations, and examples.

Melsim is **not** run as part of `get_all_features` — you choose which files, methods, and transformations to compare.

### Available Corpora

The package ships with two example corpora:

- A MIDI conversion of the Essen Folksong Collection (Eck, 2024; Schaffrath, 1995), redistributed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — see [License](#license) for more information.
- 903 Western traditional melodies used by Pearce for IDyOM pretraining (Pearce, 2018)

By default, the 903-melody corpus is used as the reference corpus by `get_all_features`.

## Development

### Building documentation

```bash
pip install -r docs/requirements.txt
cd docs && make html
# open docs/_build/html/index.html
```

### Running Tests

```bash
# Simply run pytest
pytest

# or with Python, run all tests
python tests/run_tests.py

# Run specific test suites
python -m pytest tests/test_module_setup.py -v
python -m pytest tests/test_corpus_import.py -v
python -m pytest tests/test_idyom_setup.py -v
```



## Contributing

Fork, implement, and open a PR (one feature per PR unless they belong together).

New features must be **decorated** (source, type, domain) and imported in `features.py`, or `get_all_features()` will not collect them. Docstrings feed the Sphinx API and feature catalogue — keep them NumPy-style and cite literature where relevant.

Details: [docs/contributing.rst](docs/contributing.rst). Add tests (see [tests/test_jsymbolic_validation.py](tests/test_jsymbolic_validation.py) for upstream validation) and prefer native Python return types.



## License

This project uses multiple licenses. Full attribution is in [NOTICE](NOTICE).


| Component                                                                                         | License                                                         | Details                                                                                                                                                                                        |
| ------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Package source code (default)                                                                     | [MIT](LICENSE-MIT)                                              | Copyright (c) 2025 David Mark Whyatt                                                                                                                                                           |
| Code adapted from Partitura                                                                       | [Apache-2.0](LICENSE-APACHE)                                    | `tonal_tension.py`, `pitch_spelling.py`                                                                                                                                                        |
| Bundled Essen Folksong Collection MIDI (`src/melody_features/corpora/essen_folksong_collection/`) | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) | From [Eck's MIDI conversion](https://www.kaggle.com/datasets/sebastianeck/essen-folksong-database-conversion-and-tokenization) of the Essen Folksong Collection (Schaffrath, 1995; Huron, ed.) |


The Essen corpus remains under CC BY-SA 4.0 when redistributed or adapted: retain attribution and share alike. It is not covered by the MIT license that applies to the rest of the package.
