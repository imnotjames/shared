from decimal import Decimal
from dataclasses import dataclass
from typing import Union, Tuple, Sequence, Any


@dataclass
class ReportTotals(object):
    files: int = 0
    lines: int = 0
    hits: int = 0
    misses: int = 0
    partials: int = 0
    coverage: int = 0
    branches: int = 0
    methods: int = 0
    messages: int = 0
    sessions: int = 0
    complexity: int = 0
    complexity_total: int = 0
    diff: int = 0

    def __iter__(self):
        return iter(self.astuple())

    def astuple(self):
        return (
            self.files,
            self.lines,
            self.hits,
            self.misses,
            self.partials,
            self.coverage,
            self.branches,
            self.methods,
            self.messages,
            self.sessions,
            self.complexity,
            self.complexity_total,
            self.diff,
        )

    @classmethod
    def default_totals(cls):
        args = (0,) * 13
        return cls(*args)


@dataclass
class NetworkFile(object):
    totals: ReportTotals
    session_totals: ReportTotals
    diff_totals: ReportTotals

    def astuple(self):
        return (
            self.totals.astuple(),
            [s.astuple() for s in self.session_totals] if self.session_totals else None,
            self.diff_totals.astuple() if self.diff_totals else None,
        )


@dataclass
class LineSession(object):
    id: int
    coverage: Decimal
    branches: int = None
    partials: Sequence[int] = None
    complexity: int = None

    def astuple(self):
        return (self.id, self.coverage, self.branches, self.partials, self.complexity)


@dataclass
class ReportLine(object):
    coverage: Decimal = None
    type: str = None
    sessions: Sequence[LineSession] = None
    messages: int = None
    complexity: Union[int, Tuple[int, int]] = None

    def astuple(self):
        return (
            self.coverage,
            self.type,
            [s.astuple() for s in self.sessions] if self.sessions else None,
            self.messages,
            self.complexity,
        )

    def __post_init__(self):
        if self.sessions is not None:
            for i, sess in enumerate(self.sessions):
                if not isinstance(sess, LineSession) and sess is not None:
                    self.sessions[i] = LineSession(*sess)


@dataclass
class ReportFileSummary(object):
    file_index: int
    file_totals: ReportTotals = None
    session_totals: Sequence[ReportTotals] = None
    diff_totals: Any = None

    def astuple(self):
        return (
            self.file_index,
            self.file_totals,
            self.session_totals,
            self.diff_totals,
        )


@dataclass
class Change(object):
    path: str = None
    new: bool = False
    deleted: bool = False
    in_diff: bool = None
    old_path: str = None
    totals: ReportTotals = None

    def __post_init__(self):
        if self.totals is not None:
            if not isinstance(self.totals, ReportTotals):
                self.totals = ReportTotals(*self.totals)


EMPTY = ""

TOTALS_MAP = tuple("fnhmpcbdMsCN")