import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field
from enum import Enum


# Minecraft Version
class Version(BaseModel):
    id: str
    type: str
    url: str
    time: str
    releaseTime: str
    sha1: str
    complianceLevel: int


# Minecraft Version Manifest V2
class VersionManifestV2(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    versions: List[Version]


class OSNAME(str, Enum):
    windows = "windows"
    windows_arm64 = "windows-arm64"
    linux = "linux"
    linux_arm32 = "linux-arm32"
    linux_arm64 = "linux-arm64"
    macos = "osx"
    macos_arm = "osx-arm64"


class OSNAME(BaseModel):
    name: OSNAME


class ActionEnum(str, Enum):
    allow = "allow"
    disallow = "disallow"


class Rule(BaseModel):
    action: ActionEnum
    os: Optional[OSNAME] = Field(default=None)


class Arguments:
    game: List[str | dict]
    jvm: List[str | dict]


class AssetsInfo(BaseModel):
    id: str
    sha1: str
    size: int
    totalSize: int
    url: str


class DownloadInfo(BaseModel):
    sha1: str
    size: int
    url: str


class Artifact(BaseModel):
    path: str
    sha1: str
    size: int
    url: str


class LibrariesDownloads(BaseModel):
    artifact: Optional[Artifact] = Field(default=None)
    classifiers: Optional[dict] = Field(default=None)


class Libraries(BaseModel):
    name: str
    downloads: LibrariesDownloads
    rules: Optional[List[Rule]] = Field(default=None)
    extract: Optional[dict] = Field(default=None)
    natives: Optional[dict] = Field(default=None)


class JavaVersion(BaseModel):
    component: str
    majorVersion: int


class VersionInfo(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    arguments: Optional[dict] = Field(default=None)
    assetIndex: AssetsInfo
    assets: str
    complianceLevel: Optional[int] = Field(default=None)
    downloads: dict[str, DownloadInfo]
    javaVersion: Optional[JavaVersion] = Field(default=None)
    libraries: List[Libraries]
    mainClass: str
    minimumLauncherVersion: int
    releaseTime: datetime.datetime
    time: datetime.datetime
    type: str
