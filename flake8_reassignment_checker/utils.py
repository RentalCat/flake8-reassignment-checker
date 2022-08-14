from __future__ import annotations

import typing as t

from itertools import groupby

T = t.TypeVar("T")


def groupby_sort(iterable: t.Iterable[T], **kwargs: t.Any) -> t.Iterator[tuple[t.Any, t.Iterator[T]]]:
    return groupby(sorted(iterable, **kwargs), key=kwargs.get("key", None))
