import pytest

from covreports.resources import Report, ReportFile, _encode_chunk
from covreports.utils.sessions import Session
from covreports.utils.tuples import ReportTotals, ReportLine, NetworkFile
from tests.helper import v2_to_v3


@pytest.mark.integration
def test_report_repr():
    assert repr(Report()) == '<Report files=0>'


@pytest.mark.integration
@pytest.mark.parametrize('r, network', [
    (Report(files={
        'py.py': [0, ReportTotals(1)]
    }),
     [('py.py', NetworkFile(totals=ReportTotals(1), session_totals=None, diff_totals=None))]),
    (Report(files={
        'py.py': [0, ReportTotals(1, 1, 1, 1, 1, 1)]
    }, chunks='null\n[1]\n[1]\n[1]\n<<<<< end_of_chunk >>>>>\nnull\n[1]\n[1]\n[1]').filter(paths=['py.py']),
     [('py.py', NetworkFile(totals=ReportTotals(1, 1, 1, 1, 1, 1), session_totals=None, diff_totals=None))])
])
def test_network(r, network):
    assert list(r.network) == network


@pytest.mark.integration
@pytest.mark.parametrize('r', [
    (Report(files={
        'py.py': [0, ReportTotals(1)]
    })),
    (Report(files={
        'py.py': [0, ReportTotals(1)]
    }).filter(paths=['py.py']))
])
def test_files(r):
    assert r.files == ['py.py']


@pytest.mark.integration
def test_resolve_paths():
    r = Report(files={
        'py.py': [0, ReportTotals(1)]
    }, chunks='null\n[1]\n[1]\n[1]\n<<<<< end_of_chunk >>>>>\nnull\n[1]\n[1]\n[1]')
    assert r.files == ['py.py']
    r.resolve_paths([('py.py', 'file.py')])
    assert r.files == ['file.py']


@pytest.mark.integration
@pytest.mark.parametrize('r, _file, joined, boolean, lines, hits', [
    (Report(), ReportFile('a', totals=ReportTotals(1, 50, 10), lines=[ReportLine(1)]), False, True, 50, 0),
    (Report(), None, True, False, 0, 0),
    (Report(), ReportFile('name.py'), True, False, 0, 0),
])
def test_append(r, _file, joined, boolean, lines, hits):
    assert r.append(_file, joined) is boolean
    assert r.totals.lines == lines
    assert r.totals.hits == hits


@pytest.mark.integration
def test_append_error():
    r = Report()
    with pytest.raises(Exception) as e_info:
        r.append('str')
    assert e_info.value.message == "expecting ReportFile got <type 'str'>"


@pytest.mark.integration
@pytest.mark.parametrize('r, file_repr, lines', [
    (Report(files={
        'file.py': [0, ReportTotals(1)]
    }), '<ReportFile name=file.py lines=0>', []),
    (Report(files={
        'file.py': [0, ReportTotals(1)]
    }).filter(paths=['py.py']), 'None', None),
    (Report(files={
        'file.py': [0, ReportTotals(1)]
    }, chunks='null\n[1]\n[1]\n[1]\n<<<<< end_of_chunk >>>>>\nnull\n[1]\n[1]\n[1]'), '<ReportFile name=file.py lines=3>', [(1, ReportLine(1)), (2, ReportLine(1)), (3, ReportLine(1))]),
    (Report(files={
        'file.py': [0, ReportTotals(1)]
    }, chunks=[ReportFile(name='file.py')]), '<ReportFile name=file.py lines=0>', []),
    (Report(files={
        'file.py': [1, ReportTotals(1)]
    }, chunks=[ReportFile(name='other-file.py')]), '<ReportFile name=file.py lines=0>', []),
])
def test_get(r, file_repr, lines):
    assert repr(r.get('file.py')) == file_repr
    if lines:
        assert list(r.get('file.py').lines) == lines


@pytest.mark.integration
def test_rename():
    r = Report(files={
        'file.py': [0, ReportTotals(1)]
    }, chunks='null\n[1]\n[1]\n[1]\n<<<<< end_of_chunk >>>>>\nnull\n[1]\n[1]\n[1]')
    assert r.get('name.py') is None
    assert repr(r.get('file.py')) == '<ReportFile name=file.py lines=3>'
    assert r.rename('file.py', 'name.py') is True
    assert r.get('file.py') is None
    assert repr(r.get('name.py')) == '<ReportFile name=name.py lines=3>'


@pytest.mark.integration
def test_get_item():
    r = Report(files={
        'file.py': [0, ReportTotals(1)]
    })
    assert repr(r['file.py']) == '<ReportFile name=file.py lines=0>'


@pytest.mark.integration
def test_get_item_exception():
    r = Report(files={
        'file.py': [0, ReportTotals(1)]
    })
    with pytest.raises(Exception) as e_info:
        r['name.py']
    assert e_info.value.message == 'File at path name.py not found in report'


@pytest.mark.integration
def test_del_item():
    r = Report(files={
        'file.py': [0, ReportTotals(1)]
    }, chunks='null\n[1]\n[1]\n[1]\n<<<<< end_of_chunk >>>>>\nnull\n[1]\n[1]\n[1]')
    assert repr(r.get('file.py')) == '<ReportFile name=file.py lines=3>'
    del r['file.py']
    assert r.get('file.py') is None


@pytest.mark.integration
@pytest.mark.parametrize('r, manifest', [
    (Report(files={
        'file1.py': [0, ReportTotals(1)],
        'file2.py': [1, ReportTotals(1)]
    }), ['file1.py', 'file2.py']),
    (Report(files={
        'file1.py': [0, ReportTotals(1)],
        'file2.py': [1, ReportTotals(1)]
    }).filter(paths=['file2.py']), ['file2.py']),
])
def test_manifest(r, manifest):
    assert r.manifest == manifest


@pytest.mark.integration
def test_get_folder_totals():
    r = Report(files={
        'path/file1.py': [0, ReportTotals(1)],
        'path/file2.py': [0, ReportTotals(1)],
        'wrong/path/file2.py': [0, ReportTotals(1)],
    }, chunks=[ReportFile(name='path/file1.py', totals=[1, 2, 1]), ReportFile(name='path/file2.py', totals=[1, 2, 1])])
    assert r.get_folder_totals('/path/') == ReportTotals(files=2, lines=4, hits=2, misses=0, partials=0, coverage='50.00000')


@pytest.mark.integration
def test_flags():
    r = Report(files={
        'py.py': [0, ReportTotals(1)]
    }, sessions={1: {
        'id': 'id',
        'f': ['a', 1, 'test'],
    }})
    assert r.flags.keys() == ['a', 1, 'test']


@pytest.mark.integration
def test_iter():
    r = Report(files={
        'file1.py': [0, ReportTotals(1)],
        'file2.py': [1, ReportTotals(1)]
    })
    files = []
    for _file in r:
        files.append(_file)
    assert repr(files) == '[<ReportFile name=file1.py lines=0>, <ReportFile name=file2.py lines=0>]'


@pytest.mark.integration
def test_contains():
    r = Report(files={
        'file1.py': [0, ReportTotals(1)],
    })
    assert ('file1.py' in r) is True
    assert ('file2.py' in r) is False


@pytest.mark.integration
@pytest.mark.parametrize('r, new_report, manifest', [
    (Report(files={
        'file.py': [0, ReportTotals(1)],
    }), None, ['file.py']),
    (Report(files={
        'file.py': [0, ReportTotals(1)],
    }), Report(), ['file.py']),
    (Report(files={
        'file.py': [0, ReportTotals(1)],
    }, chunks='null\n[1]\n[1]\n[1]\n<<<<< end_of_chunk >>>>>'), Report(files={
        'other-file.py': [1, ReportTotals(2)]
    }, chunks='null\n[1]\n[1]\n[1]\n<<<<< end_of_chunk >>>>>\nnull\n[1]\n[1]\n[1]'), ['other-file.py', 'file.py']),
])
def test_merge(r, new_report, manifest):
    assert r.manifest == ['file.py']
    r.merge(new_report)
    assert r.manifest == manifest


@pytest.mark.integration
def test_assume_flags():
    prev_r = Report(files={
        'file.py': [0, ReportTotals(1)]
    }, chunks=[ReportFile(name='file.py', totals=[1, 2, 1], lines=[ReportLine(1), ReportLine(2)])], sessions={1: {
        'id': 'id',
        'f': ['int'],
    }})

    r = Report(files={
        'py.py': [0, ReportTotals(1)]
    }, chunks=[ReportFile(name='py.py', totals=[1, 2, 1])])

    assert repr(r) == '<Report files=1>'
    assert r.sessions.keys() == []
    r.assume_flags('int', prev_r)
    assert repr(r) == '<Report files=2>'
    assert r.sessions.keys() == [0]  # TODO filter should work but does not because of the issue with filter


@pytest.mark.integration
@pytest.mark.parametrize('r, boolean', [
    (Report(), True),
    (Report(files={
        'file.py': [0, ReportTotals(1)]
    }).filter(paths=['this-file.py']), True),
    (Report(files={
        'file.py': [0, ReportTotals(1)]
    }), False),
])
def test_is_empty(r, boolean):
    assert r.is_empty() is boolean


@pytest.mark.integration
@pytest.mark.parametrize('r, boolean', [
    (Report(), False),
    (Report(files={
        'file.py': [0, ReportTotals(1)]
    }), True),
])
def test_non_zero(r, boolean):
    assert bool(r) is boolean


@pytest.mark.integration
def test_to_archive():
    assert Report(files={
        'file.py': [0, ReportTotals()]
    }, chunks='null\n[1]\n[1]\n[1]\n<<<<< end_of_chunk >>>>>\nnull\n[1]\n[1]\n[1]').to_archive() ==\
           'null\n[1]\n[1]\n[1]\n<<<<< end_of_chunk >>>>>\nnull\n[1]\n[1]\n[1]'


@pytest.mark.integration
def test_to_database():
    assert Report(files={
        'file.py': [0, ReportTotals()]
    }, chunks='null\n[1]\n[1]\n[1]\n<<<<< end_of_chunk >>>>>\nnull\n[1]\n[1]\n[1]').to_database() ==\
           ({'M': 0, 'c': '100', 'b': 0, 'd': 0, 'f': 1, 'h': 0, 'm': 0, 'C': 0, 'n': 0, 'p': 0, 's': 0, 'diff': None, 'N': 0}, '{"files": {"file.py": [0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]}, "sessions": {}}')


@pytest.mark.integration
@pytest.mark.parametrize('diff, future, future_diff, res', [
    ({}, None, None, False),  # empty
    (None, None, None, False),  # empty
    ({'files': {}}, None, None, False),  # empty
    ({'files': {'b': {'type': 'new'}}}, None, None, False),  # new file not tracked
    ({'files': {'b': {'type': 'new'}}}, {'files': {'b': {'l': {'1': {'c': 1}}}}}, None, True),  # new file is tracked
    ({'files': {'b': {'type': 'modified'}}}, None, None, False),  # file not tracked in base or head
    ({'files': {'a': {'type': 'deleted'}}}, None, None, True),  # tracked file deleted
    ({'files': {'b': {'type': 'deleted'}}}, None, None, False),  # not-tracked file deleted
    ({'files': {'z': {'type': 'modified'}}}, None, None, True),  # modified file missing in base
    ({'files': {'a': {'type': 'modified'}}}, None, None, True),  # modified file missing in head
    ({'files': {'a': {'type': 'modified', 'segments': [{'header': [0, 1, 1, 2], 'lines': ['- a', '+ a']}]}}},
     {'files': {'a': {'l': {'1': {'c': 1}}}}}, None, True),  # tracked line deleted
    ({'files': {'a': {'type': 'modified', 'segments': [{'header': [0, 1, 1, 2], 'lines': ['- a', '+ a']}]}}},
     {'files': {'a': {'l': {'1': {'c': 1}}}}},
     {'files': {'a': {'type': 'modified'}}},
     True),  # tracked line deleted
    ({'files': {'a': {'type': 'modified', 'segments': [{'header': [10, 1, 10, 2], 'lines': ['- a', '+ a']}]}}},
     {'files': {'a': {'l': {'1': {'c': 1}}}}}, None, False)  # lines not tracked`
])
def test_does_diff_adjust_tracked_lines(diff, future, future_diff, res):
    report = Report(**v2_to_v3({'files': {'a': {'l': {'1': {'c': 1}, '2': {'c': 1}}}}}))
    if future:
        future = Report(**v2_to_v3(future))
    else:
        future = Report(**v2_to_v3({'files': {'z': {}}}))

    assert report.does_diff_adjust_tracked_lines(diff, future, future_diff) == res


@pytest.mark.integration
def test_apply_diff():
    report = Report(**v2_to_v3({'files': {'a': {'l': {'1': {'c': 1}, '2': {'c': 0}}}}}))
    diff = {
        'files': {
            'a': {'type': 'new', 'segments': [{'header': list('1313'), 'lines': list('---+++')}]},
            'b': {'type': 'deleted'},
            'c': {'type': 'modified'}
        }
    }
    assert report.apply_diff(None) is None
    assert report.apply_diff({}) is None
    res = report.apply_diff(diff)
    assert res == diff['totals']
    assert diff['totals'].coverage == '50.00000'


@pytest.mark.integration
def test_apply_diff_no_append():
    report = Report(**v2_to_v3({'files': {'a': {'l': {'1': {'c': 1}, '2': {'c': 0}}}}}))
    diff = {
        'files': {
            'a': {'type': 'new', 'segments': [{'header': list('1313'), 'lines': list('---+++')}]},
            'b': {'type': 'deleted'},
            'c': {'type': 'modified'}
        }
    }
    res = report.apply_diff(diff, _save=False)
    assert 'totals' not in diff
    assert 'totals' not in diff['files']['a']
    assert 'totals' not in diff['files']['c']
    assert res.coverage == '50.00000'


@pytest.mark.integration
def test_report_has_flag():
    report = Report(sessions={1: dict(flags=['a'])})
    assert report.has_flag('a')
    assert not report.has_flag('b')


@pytest.mark.integration
def test_add_session():
    s = Session(5)
    r = Report(files={
        'file.py': [0, ReportTotals(0)]
    }, totals=ReportTotals(0))
    assert r.totals.sessions == 0
    assert r.sessions == {}
    assert r.add_session(s) == (0, s)
    assert r.totals.sessions == 1
    assert r.sessions == {0: s}


@pytest.mark.integration
@pytest.mark.parametrize('r, params, flare', [
    (Report(files={
        'py.py': [0, ReportTotals(1)]
    }, chunks='null\n[1]\n[1]\n[1]\n<<<<< end_of_chunk >>>>>\nnull\n[1]\n[1]\n[1]'),
     {'color': lambda cov: 'purple' if cov is None else '#e1e1e1' if cov == 0 else 'green' if cov > 0 else 'red'},
     [{'name': '', 'coverage': 100, 'color': 'green', '_class': None, 'lines': 0, 'children': [{'color': '#e1e1e1', '_class': None, 'lines': 0, 'name': 'py.py', 'coverage': 0}]}]),
    (Report(files={
        'py.py': [0, ReportTotals(1)]
    }),
     {'changes': {}},
     [{'name': '', 'coverage': 100, 'color': 'green', '_class': None, 'lines': 0, 'children': [{'color': '#e1e1e1', '_class': None, 'lines': 0, 'name': 'py.py', 'coverage': 0}]}]),
])
def test_flare(r, params, flare):
    assert r.flare(**params) == flare


# TODO see filter method on Report(), method does nothing because self.reset() is called after _filter_cache is set
# @pytest.mark.integration
# def test_filter():


@pytest.mark.integration
def test_filter_exception():
    with pytest.raises(Exception) as e_info:
        Report().filter(paths='str')
    assert e_info.value.message == "expecting list for argument paths got <type 'str'>"


@pytest.mark.integration
@pytest.mark.parametrize('chunk, res', [
    (None, 'null'),
    (ReportFile(name='name.ply'), '{}\n'),
    ([ReportLine(2), ReportLine(1)], '[[2,null,null,null,null],[1,null,null,null,null]]')
])
def test_encode_chunk(chunk, res):
    assert _encode_chunk(chunk) == res