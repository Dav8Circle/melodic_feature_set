"""Configuration classes and defaults for the feature extraction pipeline."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional

from ..idyom.config import IDyOMConfig, _DEFAULT_CORPUS, _default_idyom_configs


# Inclusive maximum m-type length (FANTASTIC n.limits default: 1-5).
DEFAULT_MAX_NGRAM_ORDER = 5


@dataclass
class FantasticConfig:
    """Settings for FANTASTIC-style features (tokenization and corpus n-grams).

    These options apply to lexical-diversity / m-type features and to
    corpus-relative FANTASTIC statistics computed by
    :func:`~melody_features.get_all_features`.

    Parameters
    ----------
    max_ngram_order :
        Inclusive maximum n-gram / m-type length (must be ``>= 1``).
        Features use orders ``1`` through this value (FANTASTIC default
        range is 1–5).
    phrase_gap :
        Inter-onset interval threshold in quarter-note units (must be
        ``> 0``). An IOI larger than this starts a new phrase when the
        melody is segmented for tokenization.
    corpus :
        Optional MIDI directory for FANTASTIC corpus statistics. If
        ``None``, the parent :class:`~melody_features.Config` corpus is
        used. Independent of IDyOM pretraining corpora.
    """

    max_ngram_order: int
    phrase_gap: float
    corpus: Optional[os.PathLike] = None

    def __post_init__(self):
        """Validate the configuration after initialization."""
        if not isinstance(self.max_ngram_order, int):
            raise ValueError(
                f"max_ngram_order must be an integer, got {type(self.max_ngram_order)}"
            )
        if self.max_ngram_order < 1:
            raise ValueError(
                f"max_ngram_order must be at least 1, got {self.max_ngram_order}"
            )

        if not isinstance(self.phrase_gap, (int, float)):
            raise ValueError(
                f"phrase_gap must be a number, got {type(self.phrase_gap)}"
            )
        if self.phrase_gap <= 0:
            raise ValueError(f"phrase_gap must be positive, got {self.phrase_gap}")

        if self.corpus is not None:
            if not isinstance(self.corpus, (str, os.PathLike)):
                raise ValueError(
                    f"corpus must be a string or PathLike, got {type(self.corpus)}"
                )
            if not Path(self.corpus).exists():
                raise ValueError(f"corpus path does not exist: {self.corpus}")


@dataclass
class Config:
    """Configuration for :func:`~melody_features.get_all_features`.

    Use ``Config`` to control corpus statistics, FANTASTIC settings, key
    estimation, and IDyOM. The ``idyom`` field is a non-empty dictionary of
    named :class:`~melody_features.IDyOMConfig` objects: **each entry runs
    IDyOM once**, and the dict key labels that run in the output columns.
    That lets you compare several IDyOM setups (models, viewpoints, corpora)
    in a single feature-extraction call.

    Parameters
    ----------
    idyom :
        Mapping of run label → :class:`~melody_features.IDyOMConfig`.
        Must contain at least one entry.
    fantastic :
        :class:`~melody_features.FantasticConfig` for corpus n-gram features.
    corpus :
        Optional default reference corpus path (FANTASTIC / IDyOM LTM).
        Per-entry ``IDyOMConfig.corpus`` and ``FantasticConfig.corpus``
        override this when set.
    key_estimation :
        ``"always_read_from_file"``, ``"infer_if_necessary"`` (default), or
        ``"always_infer"``.
    key_finding_algorithm :
        Currently only ``"krumhansl_schmuckler"``.
    """

    idyom: dict[str, IDyOMConfig]
    fantastic: FantasticConfig
    corpus: Optional[os.PathLike] = None
    key_estimation: Literal["always_read_from_file", "infer_if_necessary", "always_infer"] = "infer_if_necessary"
    key_finding_algorithm: Literal["krumhansl_schmuckler"] = "krumhansl_schmuckler"

    def __post_init__(self):
        """Validate the configuration after initialization."""
        if self.corpus is not None:
            if not isinstance(self.corpus, (str, os.PathLike)):
                raise ValueError(
                    f"corpus must be a string or PathLike, got {type(self.corpus)}"
                )
            if not Path(self.corpus).exists():
                raise ValueError(f"corpus path does not exist: {self.corpus}")

        if not isinstance(self.idyom, dict):
            raise ValueError(f"idyom must be a dictionary, got {type(self.idyom)}")
        if not self.idyom:
            raise ValueError("idyom dictionary cannot be empty")

        for name, config in self.idyom.items():
            if not isinstance(name, str):
                raise ValueError(
                    f"idyom dictionary keys must be strings, got {type(name)}"
                )
            if not isinstance(config, IDyOMConfig):
                raise ValueError(
                    f"idyom dictionary values must be IDyOMConfig objects, got {type(config)}"
                )

        if not isinstance(self.fantastic, FantasticConfig):
            raise ValueError(
                f"fantastic must be a FantasticConfig object, got {type(self.fantastic)}"
            )

        if self.key_estimation not in ["always_read_from_file", "infer_if_necessary", "always_infer"]:
            raise ValueError(f"key_estimation must be one of ['always_read_from_file', 'infer_if_necessary', 'always_infer'], got {self.key_estimation}")

        if self.key_finding_algorithm != "krumhansl_schmuckler":
            raise NotImplementedError(
                f"key_finding_algorithm '{self.key_finding_algorithm}' is not supported. "
                f"Currently only 'krumhansl_schmuckler' is implemented. More algorithms may be added in the future."
            )


def _setup_default_config(config: Optional[Config]) -> Config:
    """Set up default configuration if none is provided."""
    if config is None:
        config = Config(
            corpus=_DEFAULT_CORPUS,
            idyom=_default_idyom_configs(_DEFAULT_CORPUS),
            fantastic=FantasticConfig(
                max_ngram_order=DEFAULT_MAX_NGRAM_ORDER,
                phrase_gap=1.5,
                corpus=None,
            ),
            key_estimation="infer_if_necessary",
        )
    return config


def _validate_config(config: Config) -> None:
    """Validate the configuration object."""
    if not hasattr(config, "idyom") or not config.idyom:
        raise ValueError("Config must have at least one IDyOM configuration")

    if not hasattr(config, "fantastic"):
        raise ValueError("Config must have FANTASTIC configuration")
