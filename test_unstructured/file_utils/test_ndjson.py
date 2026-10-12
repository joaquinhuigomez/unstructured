"""Unit-test suite for the `unstructured.file_utils.ndjson` module."""

from __future__ import annotations

import pytest

from unstructured.file_utils import ndjson


@pytest.mark.parametrize("char", ["\u0085", " ", " "])
def test_loads_does_not_split_a_record_on_a_unicode_line_break_inside_a_string(char: str):
    s = '{"body": "first' + char + 'second"}\n{"body": "ok"}\n'

    assert ndjson.loads(s) == [{"body": f"first{char}second"}, {"body": "ok"}]


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("", []),
        ("a\nb", ["a", "b"]),
        ("a\nb\n", ["a", "b"]),
        ("a\r\nb\r\n", ["a", "b"]),
        ("a\rb", ["a", "b"]),
        ("a\n\nb\n\n", ["a", "", "b", ""]),
        ("a b\x85c d", ["a b\x85c d"]),
    ],
)
def test_split_lines_splits_on_CR_and_LF_line_breaks_only(s: str, expected: list[str]):
    assert ndjson.split_lines(s) == expected
