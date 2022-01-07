import importlib
import pkgutil
import click


@click.group()
def cli():
    pass


# TODO: caching or something so we don't need to do this on every invocation
discovered = {
    name: importlib.import_module(name)
    for (finder, name, ispkg)
    in pkgutil.iter_modules()
    if name.startswith("deck_")
}


for (name, plugin) in discovered.items():
    cli_groups = [
        getattr(plugin, attr)
        for attr in dir(plugin)
        if isinstance(getattr(plugin, attr), click.core.Group)
    ]
    if len(cli_groups) == 1:
        cli.add_command(cli_groups[0])


if __name__ == "__main__":
    cli()
