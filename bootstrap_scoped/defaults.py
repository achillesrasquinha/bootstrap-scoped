# imports - standard imports
import os
import os.path as osp

# imports - module imports
from bootstrap_scoped.__attr__ import __name__

BOOTSTRAP_GITHUB_URL = "https://github.com/twbs/bootstrap"
BOOTSTRAP_SCOPE_NAME = ".bootstrap-scope"
BOOTSTRAP_SPACE_SIZE = 2

DIRECTORY_CACHE      = osp.join(osp.expanduser("~"), ".{}".format(__name__))

TEMPLATE_SCOPE       = \
"""
{scope} {{
{includes}
}}
"""