from pydantic import BaseModel


class VersionInfo(BaseModel):
    version: str
    stable: bool


class IntermediaryInfo(BaseModel):
    maven: str
    version: str
    stable: bool
