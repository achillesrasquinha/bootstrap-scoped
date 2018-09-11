# imports - compatibility imports
from bootstrap_scoped._compat import StringIO

# imports - test imports
import pytest

# imports - module imports
from bootstrap_scoped.commands   import command
from bootstrap_scoped.util._test import mock_input

def test_command():
    with mock_input(StringIO("Y")):
        command(check = True)

    with mock_input(StringIO("Y")):
        command()