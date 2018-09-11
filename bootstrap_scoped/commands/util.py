# imports - module imports
from bootstrap_scoped.cli.parser import get_args
from bootstrap_scoped import cli

def cli_format(string, type_):
    args = get_args(as_dict = False)

    if not args.no_color:
        string = cli.format(string, type_)

    return string