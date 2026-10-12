"""
Adds support for working with newline-delimited JSON (ndjson) files. This format is useful for
streaming json content that would otherwise not be possible using raw JSON files.
"""

import json
import re
from typing import IO, Any

_LINE_BREAK_RE = re.compile(r"\r\n|\r|\n")


def split_lines(s: str) -> list[str]:
    """Split NDJSON text into lines on LF, CRLF and CR only.

    Unlike `str.splitlines()`, this does not split on U+0085, U+2028 or U+2029, which JSON allows
    unescaped inside a string value. A trailing line break does not produce a final empty line,
    matching `str.splitlines()`.
    """
    lines = _LINE_BREAK_RE.split(s)
    if lines[-1] == "":
        lines.pop()
    return lines


def dumps(obj: list[dict[str, Any]], **kwargs) -> str:
    """
    Converts the list of dictionaries into string representation

    Args:
        obj (list[dict[str, Any]]): List of dictionaries to convert
        **kwargs: Additional keyword arguments to pass to json.dumps

    Returns:
        str: string representation of the list of dictionaries
    """
    return "\n".join(json.dumps(each, **kwargs) for each in obj)


def dump(obj: list[dict[str, Any]], fp: IO, **kwargs) -> None:
    """
    Writes the list of dictionaries to a newline-delimited file

    Args:
        obj (list[dict[str, Any]]): List of dictionaries to convert
        fp (IO): File pointer to write the string representation to
        **kwargs: Additional keyword arguments to pass to json.dumps

    Returns:
        None
    """
    # Indent breaks ndjson formatting
    kwargs["indent"] = None
    text = dumps(obj, **kwargs)
    fp.write(text)


def loads(s: str, **kwargs) -> list[dict[str, Any]]:
    """
    Converts the raw string into a list of dictionaries

    Args:
        s (str): Raw string to convert
        **kwargs: Additional keyword arguments to pass to json.loads

    Returns:
        list[dict[str, Any]]: List of dictionaries parsed from the input string
    """
    return [json.loads(line, **kwargs) for line in split_lines(s)]


def load(fp: IO, **kwargs) -> list[dict[str, Any]]:
    """
    Converts the contents of the file into a list of dictionaries

    Args:
        fp (IO): File pointer to read the string representation from
        **kwargs: Additional keyword arguments to pass to json.loads

    Returns:
        list[dict[str, Any]]: List of dictionaries parsed from the file
    """
    return loads(fp.read(), **kwargs)
