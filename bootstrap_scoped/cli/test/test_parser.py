# imports - standard imports
from bootstrap_scoped.cli.parser import get_args

def test_args():
    def _get_arg(args, arg):
        if hasattr(args, arg):
            return getattr(args, arg)
        else:
            return args[arg]
    
    def _assert_args(args):
        assert _get_arg(args, "yes")      == False
        assert _get_arg(args, "check")    == False
        assert _get_arg(args, "latest")   == False
        assert _get_arg(args, "no_color") == False
        assert _get_arg(args, "verbose")  == False
            
    args = get_args()
    _assert_args(args)

    args = get_args(as_dict = False)
    _assert_args(args)

    args = get_args(known = False)
    _assert_args(args)