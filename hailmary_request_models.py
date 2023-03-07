from typing import Optional
from pydantic import BaseModel
from typing import Any


class Request(BaseModel):
    host: str


class LogsRequest(Request):
    log_stream: str


class ContentRequest(Request):
    """A request for content.

    paths can be a list of directories
    and files or a single directory/file.
    Must be a path relative to the hailmary_server's
    cwd.
    If an element in content_path is a directory,
    it will be globbed and the results can
    be filtered with includes_pattern
    or excludes_pattern.
    These are both lists of patterns.

    """

    paths: list[str] | str
    includes_pattern: list[str]
    excludes_pattern: list[str]
