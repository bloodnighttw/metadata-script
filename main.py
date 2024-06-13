import os
import rich

from script.fabric.fetch import fetch_fabric
from script.vanillia.fetch import fetch_vanilla

ASSETS_PATH = "assets/"
UPSTREAM_PATH = "upstream"
LAUNCHER_PATH = "launcher"

console = rich.get_console()


def check():
    console.log("[green]Checking Folder is existing.[/green]")
    if not os.path.exists(ASSETS_PATH):
        os.makedirs(ASSETS_PATH)
        console.log(f"[red]ASSETS_PATH {ASSETS_PATH} not found, create it for you![/red]")
    else:
        console.log(f"[green]ASSETS_PATH {ASSETS_PATH} found![/green]")
    if not os.path.exists(UPSTREAM_PATH):
        os.makedirs(UPSTREAM_PATH)
        console.log(f"[red]UPSTREAM_PATH {UPSTREAM_PATH} not found, create it for you![/red]")
    else:
        console.log(f"[green]UPSTREAM_PATH {UPSTREAM_PATH} found![/green]")
    if not os.path.exists(LAUNCHER_PATH):
        os.makedirs(LAUNCHER_PATH)
        console.log(f"[red]LAUNCHER_PATH {LAUNCHER_PATH} not found, create it for you![/red]")
    else:
        console.log(f"[green]LAUNCHER_PATH {LAUNCHER_PATH} found![/green]")


if __name__ == '__main__':
    check()

    fetch_vanilla(UPSTREAM_PATH)
    fetch_fabric(UPSTREAM_PATH)

