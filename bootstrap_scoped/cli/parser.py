# imports - standard imports
import argparse

# imports - module imports
from bootstrap_scoped          import defaults
from bootstrap_scoped.__attr__ import (
    __version__,
    __description__
)
from bootstrap_scoped.util     import get_if_empty

def get_parser():
    parser = argparse.ArgumentParser(
        description = __description__,
        add_help    = False
    )
    parser.add_argument("-s", "--scope",
        type    = str,
        default = defaults.BOOTSTRAP_SCOPE_NAME,
        help    = "Scope Name"
    )
    parser.add_argument("--bootstrap-url",
        type    = str,
        default = defaults.BOOTSTRAP_GITHUB_URL,
        help    = "Remote URL for bootstrap repository"
    )
    parser.add_argument("--bootstrap-version",
        type    = str,
        help    = "Bootstrap Version to checkout from (defaults to latest stable version)"
    )
    parser.add_argument("--latest",
        action  = "store_true",
        help    = "Use latest Bootstrap Version"
    )
    parser.add_argument("-o", "--output",
        type    = str,
        default = None,
        help    = "Output path of generated distribution"
    )
    parser.add_argument("--no-cache",
        action  = "store_true",
        help    = "Avoid fetching from cached Bootstrap"
    )
    parser.add_argument("--no-color",
        action  = "store_true",
        help    = "Avoid colored output"
    )
    parser.add_argument("-V", "--verbose",
        action  = "store_true",
        help    = "Display verbose output"
    )

    parser.add_argument("-v", "--version",
        action  = "version",
        version = __version__
    )
    parser.add_argument("-h", "--help",
        action  = "help",
        default = argparse.SUPPRESS,
        help    = "Show this help message and exit"
    )

    return parser

def get_args(args = None, known = True, as_dict = True):
    parser  = get_parser()
    args    = get_if_empty(args, None)

    if known:
        args, _ = parser.parse_known_args(args)
    else:
        args    = parser.parse_args(args)

    if as_dict:
        args = args.__dict__
        
    return args