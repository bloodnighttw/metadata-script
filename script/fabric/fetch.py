import concurrent.futures
import json
import os.path

import requests
import rich
from rich.progress import Progress

from model.fabric import VersionInfo, LoaderInfo, LoaderDetails

console = rich.get_console()


def fetch_fabric(upstream):
    if not os.path.exists(f"{upstream}/fabric"):
        os.makedirs(f"{upstream}/fabric")
    if not os.path.exists(f"{upstream}/fabric/loader"):
        console.log(f"[green]Create {upstream}/fabric/loader")
        os.makedirs(f"{upstream}/fabric/loader")

    console.log("[green]start fetching fabric data!")
    fetch_fabric_game_version(upstream)
    versions = fetch_loader_version(upstream)

    with Progress() as progress, concurrent.futures.ThreadPoolExecutor() as executor:
        progress_task = progress.add_task("[cyan]Fetching File", total=len(versions))
        tasks = []
        for i in versions:
            task = executor.submit(fetch_loader_details, upstream, i.version, progress, progress_task)
            tasks.append(task)
        executor.shutdown(wait=True)
        progress.update(progress_task, description="completed!")


def fetch_fabric_game_version(upstream):
    version_list = requests.get("https://meta.fabricmc.net/v2/versions/game").json()
    version_valid = [VersionInfo.model_validate(i) for i in version_list]
    with open(f"{upstream}/fabric/game.json", "w") as f:
        json.dump(version_list, f)
    return version_valid


def fetch_loader_version(upstream):
    version_list = requests.get("https://meta.fabricmc.net/v2/versions/loader").json()
    version_valid = [LoaderInfo.model_validate(i) for i in version_list]
    with open(f"{upstream}/fabric/loader.json", "w") as f:
        json.dump(version_list, f)
    return version_valid


def fetch_loader_details(upstream, loader_version, progress, task):
    progress.update(task, description=f"[cyan]Start Downloading File {loader_version}")
    details = requests.get(f"https://meta.fabricmc.net/v1/versions/loader/1.14/{loader_version}").json()
    console.log(f"Fetch Done from https://meta.fabricmc.net/v1/versions/loader/1.14/{loader_version}")
    progress.update(task, advance=1)

    try:
        LoaderDetails.model_validate(details)
    except Exception as e:
        console.log(f"[red]error on {loader_version}")
        console.log(e)

    with open(f"{upstream}/fabric/loader/{loader_version}.json", "w") as f:
        json.dump(details, f)


if __name__ == '__main__':
    fetch_loader_details("upstream", "0.6.4+build.169")
