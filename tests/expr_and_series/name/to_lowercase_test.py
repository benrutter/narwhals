from __future__ import annotations

from contextlib import nullcontext as does_not_raise
from typing import Any

import polars as pl
import pytest

import narwhals.stable.v1 as nw
from tests.utils import compare_dicts

data = {"foo": [1, 2, 3], "BAR": [4, 5, 6]}


def test_to_lowercase(constructor: Any) -> None:
    df = nw.from_native(constructor(data))
    result = df.select((nw.col("foo", "BAR") * 2).name.to_lowercase())
    expected = {k.lower(): [e * 2 for e in v] for k, v in data.items()}
    compare_dicts(result, expected)


def test_to_lowercase_after_alias(constructor: Any) -> None:
    df = nw.from_native(constructor(data))
    result = df.select((nw.col("BAR")).alias("ALIAS_FOR_BAR").name.to_lowercase())
    expected = {"bar": data["BAR"]}
    compare_dicts(result, expected)


def test_to_lowercase_raise_anonymous(constructor: Any) -> None:
    df_raw = constructor(data)
    df = nw.from_native(df_raw)

    context = (
        does_not_raise()
        if isinstance(df_raw, (pl.LazyFrame, pl.DataFrame))
        else pytest.raises(
            ValueError,
            match="Anonymous expressions are not supported in `.name.to_lowercase`.",
        )
    )

    with context:
        df.select(nw.all().name.to_lowercase())
