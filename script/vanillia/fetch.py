import concurrent.futures
import json
import os

import requests
import rich
from rich.progress import Progress

from model.vanillia import VersionManifestV2, VersionInfo

console = rich.get_console()

VERSION_MANIFEST_V2_URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
PATH = "vanilla"


def download(url, progress, task, version_id, upstream):
    progress.update(task, description=f"[cyan]Start Downloading File {version_id}")
    data = requests.get(url).json()
    progress.update(task, advance=1)
    console.log(f"Download Done from {url} !")
    with open(f"{upstream}/{PATH}/{version_id}.json", "w") as f:
        json.dump(data, f)
    try:
        return VersionInfo.model_validate(data)
    except Exception as e:
        console.log(f"[red]Error on Version:{version_id}")
        console.log(e)
        raise e


def fetch_vanilla(upstream):
    if not os.path.exists(f"{upstream}/{PATH}/"):
        os.makedirs(f"{upstream}/{PATH}/")
    with console.status("[bold green]fetching vanilla data.") as status:
        data = fetch_version_manifest_v2(upstream)

    with Progress() as progress, concurrent.futures.ThreadPoolExecutor() as executor:
        progress_task = progress.add_task("[cyan]Fetching File", total=len(data.versions))
        tasks = []
        for i in data.versions:
            task = executor.submit(download, i.url, progress, progress_task, i.id, upstream)
            tasks.append(task)
        progress.update(progress_task, description="completed!")
        for i in concurrent.futures.as_completed(tasks):
            data = i.result()
            # console.log(data)


def fetch_version_manifest_v2(upstream):
    data = requests.get(VERSION_MANIFEST_V2_URL).json()
    with open(f"{upstream}/version_manifest_v2.json", "w") as f:
        json.dump(data, f)
    return VersionManifestV2.model_validate(data)
