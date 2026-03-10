import yaml
from typing import Any
from pydantic import BaseModel


class VocalData(BaseModel):
    musicId: int
    vocals: list[int]


class GameAppVersion(BaseModel):
    systemProfile: str = "production"
    appVersion: str
    multiPlayVersion: str
    assetVersion: str
    appVersionStatus: str


class ApiInformation(BaseModel):
    id: int
    seq: int
    displayOrder: int = 3
    informationType: str
    informationTag: str
    platform: str
    browseType: str
    title: str
    path: str
    startAt: int
    endAt: int | None = None


class VersionData(BaseModel):
    profile: str = "production"
    assetbundleHostHash: str
    domain: str


class DomainsConfig(BaseModel):
    assetbundleApi: str
    assetbundleUrl: str
    assetbundleInfoUrl: str


class LegalConfig(BaseModel):
    privacyPolicy: str
    termsOfUse: str


class Config(BaseModel):
    apiPort: int
    webPort: int
    versionPort: int
    databaseUrl: str | None = None
    assetsPort: int
    domains: DomainsConfig
    versions: list[GameAppVersion]
    latestVersion: int
    dataVersion: str
    versionData: dict[str, VersionData]
    apiDomain: str
    webDomain: str
    maintenanceStatus: str
    suiteMasterSplitPath: list[str]
    assetHash: str
    legal: LegalConfig
    informations: list[ApiInformation]
    deleteLiveDataAfterFinishing: bool
    upstreamAssetUrl: str


def load_config(path: str = "./config.yml") -> Config:
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return Config(**data)


config = load_config()
