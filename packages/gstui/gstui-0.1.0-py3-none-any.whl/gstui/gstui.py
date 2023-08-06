from click import Choice, command, option

from gstui.gsclient import CachedClient
from gstui.ui_base import FzfUI


@command()
@option(
    "--interface", "-i", default="fzf",
    type=Choice(["fzf"]), help="UI interface to use"
)
@option("--clean", "-c", is_flag=True, help="Clean cache")
@option("--cache-path", "-p", default="~/.cache/gstui", help="Cache directory")
@option("--cache-all", "-a", is_flag=True, help="Cache all tree structure")
def main(interface, clean, cache_path, cache_all):
    storage_client = CachedClient()
    storage_client.cache_path = cache_path
    if clean:
        storage_client.clean_cache()
        return
    if cache_all:
        storage_client.cache_all()
        return
    if interface == "fzf":
        ui = FzfUI()
        ui.mainloop(storage_client)
    storage_client.close()
