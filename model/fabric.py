from typing import List, Optional

from pydantic import BaseModel, Field, root_validator


class VersionInfo(BaseModel):
    version: str
    stable: bool


class LoaderInfo(BaseModel):
    separator: str
    build: int
    maven: str
    version: str
    stable: bool


class LibraryV1(BaseModel):
    name: str
    url: Optional[str]


class LibraryV2(BaseModel):
    name: str
    url: str
    md5: str
    sha1: str
    sha256: str
    sha512: str
    size: int


class LaunchMetaV1(BaseModel):
    version: int = 1
    libraries: dict[str, List[LibraryV1 | dict]]
    mainClass: str | dict[str, str]


class LaunchMetaV2(LaunchMetaV1):
    version: int = 2
    min_java_version: int


class LoaderDetails(BaseModel):
    loader: LoaderInfo
    launcherMeta: LaunchMetaV1 | LaunchMetaV2
