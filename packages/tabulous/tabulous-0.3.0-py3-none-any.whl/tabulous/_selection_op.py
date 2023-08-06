from __future__ import annotations

from typing import Hashable, Iterator, TYPE_CHECKING, Union
from functools import singledispatch
import re

if TYPE_CHECKING:
    import pandas as pd
    from typing_extensions import Self

_Slice = Union[int, slice]


class SelectionOperator:
    """An object that defines a selection on a dataframe."""

    args: tuple
    PATTERN: str

    def fmt(self, df_expr: str = "df") -> str:
        """Format selection literal for display."""
        raise NotImplementedError()

    def fmt_scalar(self, df_expr: str = "df") -> str:
        """Format 1x1 selection literal as a scalar reference."""
        raise NotImplementedError()

    def __format__(self, spec: str) -> str:
        return self.fmt(df_expr=spec)

    def __repr__(self) -> str:
        cname = type(self).__name__
        return f"{cname}({self.fmt()})"

    def operate(self, df: pd.DataFrame) -> pd.DataFrame:
        """Slice dataframe according to selection literal."""
        raise NotImplementedError()

    def as_iloc(self, df: pd.DataFrame) -> tuple[_Slice, _Slice]:
        """Return selection literal as iloc indices."""
        raise NotImplementedError()

    def as_iloc_slices(self, df: pd.DataFrame) -> tuple[slice, slice]:
        """Return selection literal as iloc indices, forcing slices."""
        rsl, csl = self.as_iloc(df)
        if isinstance(rsl, int):
            rsl = slice(rsl, rsl + 1)
        elif rsl == slice(None):
            rsl = slice(0, df.index.size)
        if isinstance(csl, int):
            csl = slice(csl, csl + 1)
        elif csl == slice(None):
            csl = slice(0, df.columns.size)
        return rsl, csl

    def area(self, df: pd.DataFrame) -> int:
        """Return the number of cells selected."""
        rsl, csl = self.as_iloc_slices(df)
        return (rsl.stop - rsl.start) * (csl.stop - csl.start)

    @classmethod
    def from_iloc(cls, r: _Slice, c: _Slice, df: pd.DataFrame) -> Self:
        """Construct selection literal from iloc indices."""
        raise NotImplementedError()

    def __eq__(self, other: Self) -> bool:
        if isinstance(other, type(self)):
            return self.args == other.args
        return False


class ColumnSelOp(SelectionOperator):
    """An object that represents selection such as ``df["foo"][2:5]``."""

    args: tuple[Hashable, slice]
    PATTERN = r"df\[.+?\]\[.+?\]"

    def __init__(self, col: Hashable, rows: slice):
        self.args = (col, rows)

    def fmt(self, df_expr: str = "df") -> str:
        col, rows = self.args
        return f"{df_expr}[{_fmt_slice(col)}][{_fmt_slice(rows)}]"

    def fmt_scalar(self, df_expr: str = "df") -> str:
        col, rows = self.args
        start, stop = rows.start, rows.stop
        if stop - start != 1:
            raise ValueError("Cannot format as a scalar value.")
        return f"{df_expr}[{_fmt_slice(col)}][{_fmt_slice(start)}]"

    def operate(self, df: pd.DataFrame) -> pd.DataFrame:
        col, rows = self.args
        return df[col][rows]

    def as_iloc(self, df: pd.DataFrame) -> tuple[_Slice, _Slice]:
        colname, rsel = self.args
        col = df.columns.get_loc(colname)
        return rsel, col

    @classmethod
    def from_iloc(cls, r: _Slice, c: _Slice, df: pd.DataFrame) -> Self:
        if isinstance(c, slice):
            if c.start == c.stop - 1:
                c = c.start
            else:
                raise ValueError("Cannot convert slice to row selection.")
        colname = df.columns[c]
        return cls(colname, r)


class LocSelOp(SelectionOperator):
    """An object that represents selection such as ``df.loc["foo":"bar", 2:5]``."""

    PATTERN = r"df\.loc\[.+?\]"

    def __init__(self, rsel: Hashable | slice, csel: Hashable | slice):
        self.args = (rsel, csel)

    def fmt(self, df_expr: str = "df") -> str:
        rsel, csel = self.args
        return f"{df_expr}.loc[{_fmt_slice(rsel)}, {_fmt_slice(csel)}]"

    def fmt_scalar(self, df_expr: str = "df") -> str:
        rsel, csel = self.args
        if isinstance(rsel, slice):
            if rsel.start != rsel.stop:
                raise ValueError("Cannot format as a scalar value.")
            rsel = rsel.start
        if isinstance(csel, slice):
            if csel.start != csel.stop:
                raise ValueError("Cannot format as a scalar value.")
            csel = csel.start
        return f"{df_expr}.loc[{_fmt_slice(rsel)}, {_fmt_slice(csel)}]"

    def operate(self, df: pd.DataFrame) -> pd.DataFrame:
        rsel, csel = self.args
        return df.loc[rsel, csel]

    def as_iloc(self, df: pd.DataFrame) -> tuple[_Slice, _Slice]:
        rsel, csel = self.args
        index, columns = df.axes
        if isinstance(rsel, slice):
            if rsel.start is None:
                rstart = None
            else:
                rstart = index.get_loc(rsel.start)
            if rsel.stop is None:
                rstop = None
            else:
                rstop = index.get_loc(rsel.stop) + 1
            irsel = slice(rstart, rstop)
        else:
            irsel = index.get_loc(rsel)
        if isinstance(csel, slice):
            if csel.start is None:
                cstart = None
            else:
                cstart = columns.get_loc(csel.start)
            if csel.stop is None:
                cstop = None
            else:
                cstop = columns.get_loc(csel.stop) + 1
            icsel = slice(cstart, cstop)
        else:
            icsel = columns.get_loc(csel)
        return irsel, icsel

    @classmethod
    def from_iloc(cls, r: _Slice, c: _Slice, df: pd.DataFrame) -> Self:
        index, columns = df.axes
        if isinstance(r, slice):
            rsel = slice(index[r.start], index[r.stop - 1])
        else:
            rsel = index[r]
        if isinstance(c, slice):
            csel = slice(columns[c.start], columns[c.stop - 1])
        else:
            csel = columns[c]
        return cls(rsel, csel)


class ILocSelOp(SelectionOperator):
    """An object that represents selection such as ``df.iloc[4:7, 2:5]``."""

    args: tuple[_Slice, _Slice]
    PATTERN = r"df\.iloc\[.+?\]"

    def __init__(self, rsel: _Slice, csel: _Slice):
        self.args = (rsel, csel)

    def fmt(self, df_expr: str = "df") -> str:
        rsel, csel = self.args
        return f"{df_expr}.iloc[{_fmt_slice(rsel)}, {_fmt_slice(csel)}]"

    def fmt_scalar(self, df_expr: str = "df") -> str:
        rsel, csel = self.args
        if isinstance(rsel, slice):
            if rsel.start != rsel.stop - 1:
                raise ValueError("Cannot format as a scalar value.")
            rsel = rsel.start
        if isinstance(csel, slice):
            if csel.start != csel.stop - 1:
                raise ValueError("Cannot format as a scalar value.")
            csel = csel.start
        return f"{df_expr}.iloc[{_fmt_slice(rsel)}, {_fmt_slice(csel)}]"

    def operate(self, df: pd.DataFrame) -> pd.DataFrame:
        rsel, csel = self.args
        return df.iloc[rsel, csel]

    def as_iloc(self, df: pd.DataFrame) -> tuple[_Slice, _Slice]:
        return self.args

    @classmethod
    def from_iloc(cls, r: _Slice, c: _Slice, df: pd.DataFrame) -> Self:
        return cls(r, c)


class ValueSelOp(SelectionOperator):
    """An object that represents selection such as ``df.iloc[4:7, 2:5]``."""

    PATTERN = r"df\.values\[.+?\]"

    def __init__(self, rsel: _Slice, csel: _Slice):
        self.args = (rsel, csel)

    def fmt(self, df_expr: str = "df") -> str:
        rsel, csel = self.args
        return f"{df_expr}.values[{_fmt_slice(rsel)}, {_fmt_slice(csel)}]"

    def fmt_scalar(self, df_expr: str = "df") -> str:
        rsel, csel = self.args
        if isinstance(rsel, slice):
            if rsel.start != rsel.stop - 1:
                raise ValueError("Cannot format as a scalar value.")
            rsel = rsel.start
        if isinstance(csel, slice):
            if csel.start != csel.stop - 1:
                raise ValueError("Cannot format as a scalar value.")
            csel = csel.start
        return f"{df_expr}.values[{_fmt_slice(rsel)}, {_fmt_slice(csel)}]"

    def operate(self, df: pd.DataFrame) -> pd.DataFrame:
        rsel, csel = self.args
        return df.values[rsel, csel]

    def as_iloc(self, df: pd.DataFrame) -> tuple[_Slice, _Slice]:
        return self.args

    @classmethod
    def from_iloc(cls, r: _Slice, c: _Slice, df: pd.DataFrame) -> Self:
        return cls(r, c)


def iter_extract(text: str, *, df_expr: str = "df") -> Iterator[SelectionOperator]:
    """Iteratively extract selection literal from text."""
    ndf = len(df_expr)
    for expr in find_all_dataframe_expr(text):
        if expr.startswith(f"{df_expr}["):
            # df['val'][...]
            colname, rsl_str = expr[ndf + 1 : -1].split("][")
            rsl = _parse_slice(rsl_str)
            sel = ColumnSelOp(_eval(colname), rsl)

        elif expr.startswith(f"{df_expr}.loc["):
            # df.loc[..., ...]
            rsl_str, csl_str = expr[ndf + 5 : -1].split(",")
            rsl = _parse_slice(rsl_str)
            csl = _parse_slice(csl_str)
            sel = LocSelOp(rsl, csl)

        elif expr.startswith(f"{df_expr}.iloc["):
            # df.iloc[..., ...]
            rsl_str, csl_str = expr[ndf + 6 : -1].split(",")
            rsl = _parse_slice(rsl_str)
            csl = _parse_slice(csl_str)
            sel = ILocSelOp(rsl, csl)

        elif expr.startswith(f"{df_expr}.values["):
            # df.values[..., ...]
            rsl_str, csl_str = expr[ndf + 8 : -1].split(",")
            rsl = _parse_slice(rsl_str)
            csl = _parse_slice(csl_str)
            sel = ValueSelOp(rsl, csl)

        else:
            raise ValueError(f"Unreachable expression: {expr!r}")

        yield sel


_PATTERN = re.compile(
    "|".join(s.PATTERN for s in (ColumnSelOp, LocSelOp, ILocSelOp, ValueSelOp))
)


def find_all_dataframe_expr(s: str) -> list[str]:
    return _PATTERN.findall(s)


def find_last_dataframe_expr(s: str) -> int:
    """
    Detect last `df[...][...]` expression from given string.

    Returns start index if matched, otherwise -1.
    """
    _match = None
    for _match in _PATTERN.finditer(s):
        pass
    return _match.start() if _match else -1


def _eval(expr: str, default=None):
    """evaluate expression."""
    return eval(expr, {}, {}) if expr else default


def _parse_slice(s: str) -> Hashable | slice:
    s = s.strip()
    if ":" in s:
        start_str, stop_str = s.split(":")
        start = _eval(start_str)
        stop = _eval(stop_str)
        return slice(start, stop)
    else:
        return _eval(s)


@singledispatch
def _fmt_slice(s) -> str:
    return str(s)


@_fmt_slice.register
def _(s: int) -> str:
    return str(s)


@_fmt_slice.register
def _(s: str) -> str:
    return repr(s)


@_fmt_slice.register
def _(s: slice) -> str:
    if s == slice(None):
        return ":"
    start = "" if s.start is None else s.start
    stop = "" if s.stop is None else s.stop
    return f"{start!r}:{stop!r}"
