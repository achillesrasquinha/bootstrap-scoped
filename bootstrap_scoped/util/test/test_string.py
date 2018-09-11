# imports - module imports
from bootstrap_scoped.util.string import strip_ansi, strip, safe_decode
from bootstrap_scoped import cli

def test_strip_ansi():
    assert strip_ansi(cli.format("foobar", cli.GREEN)) == "foobar"
    assert strip_ansi(cli.format("barfoo", cli.BOLD))  == "barfoo"

def test_strip():
    string = "foobar"
    assert strip(string) == string

    string = "\n   foobar\nfoobar   \n   "
    assert strip(string) == "foobar\nfoobar"

    string = "\n\n\n"
    assert strip(string) == ""

def test_safe_decode():
    assert safe_decode(b"foobar") == "foobar"
    assert safe_decode( "foobar") == "foobar"
    
    assert safe_decode(123456789) == 123456789
