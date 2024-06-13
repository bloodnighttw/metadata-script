import requests
import rich

from model.fabric import VersionInfo, IntermediaryInfo

console = rich.get_console()


def fetch_fabric(upstream):
    version_list = requests.get("https://meta.fabricmc.net/v2/versions/game").json()
    version_valid = [VersionInfo.model_validate(i) for i in version_list]
    fetch_intermediary_version(upstream)


def fetch_intermediary_version(upstream):
    version_list = requests.get("https://meta.fabricmc.net/v2/versions/intermediary").json()
    version_valid = [IntermediaryInfo.model_validate(i) for i in version_list]
    console.log(version_valid)


if __name__ == '__main__':
    fetch_fabric("upstream")
    fetch_intermediary_version("upstream")