# generated by datamodel-codegen:
#   filename:  media_directories.json

from __future__ import annotations

from pydantic import BaseModel


class Directory(BaseModel):
    key: str
    path: str


class MediaDirectories(BaseModel):
    directories: list[Directory]
