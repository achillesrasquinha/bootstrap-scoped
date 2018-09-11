# imports - standard imports
import os.path as osp

# imports - module imports
from bootstrap_scoped               import cli, defaults
from bootstrap_scoped.commands.util import cli_format
from bootstrap_scoped.system        import read, write, which, popen, makedirs, tmpdir, zipdir
from bootstrap_scoped.util          import get_if_empty
from bootstrap_scoped.util.string   import strip

def _sanitize(content, size = defaults.BOOTSTRAP_SPACE_SIZE):
    spaces  = " " * size
    content = "\n".join(filter(
        lambda x: bool(strip(x)),
        map(
            lambda x: spaces + strip(x),
            content.splitlines()
        )
    ))

    return content

@cli.command
def command(
    scope             = defaults.BOOTSTRAP_SCOPE_NAME,
    bootstrap_url     = defaults.BOOTSTRAP_GITHUB_URL,
    bootstrap_version = None,
    latest            = False,
    output            = None,
    no_cache          = False,
    no_color          = False,
    verbose           = False
):
    git  = which("git", raise_err = True)
    npm  = which("npm", raise_err = True)

    repo = "bootstrap-repo"

    def _bootstrap_scope_repo(repo):
        if not osp.exists(repo):
            cli.echo(cli_format("Cloning {}...".format(bootstrap_url), cli.YELLOW))
            popen(git, "clone", bootstrap_url, repo,   output = not verbose)
            cli.echo(cli_format("Cloned.", cli.GREEN))

        if not latest:
            _, tag, _ = popen(git, "describe", "--tags", cwd = repo, output = True)

            cli.echo(cli_format("Checking out from {}...".format(tag), cli.YELLOW))
            popen(git, "checkout", tag, cwd = repo, output = not verbose)

        popen(npm, "install", cwd = repo, output = not verbose)

        cli.echo("{}: {}".format(
            cli_format("Using scope name", cli.YELLOW),
            cli_format(scope, cli.GREEN)
        ))

        path     = osp.join(repo, "scss", "bootstrap.scss")
        content  = read(path)
        content  = _sanitize(content)
        
        cli.echo(cli_format("Generating template...", cli.YELLOW))
        template = defaults.TEMPLATE_SCOPE.format(scope = scope, includes = content)
        write(path, template, force = True)

        popen(npm, "run", "dist", cwd = repo, output = not verbose)
        
        _, commit, _ = popen(git, "rev-parse", "--short", "HEAD", cwd = repo, output = True)

        source       = osp.join(repo, "dist")
        target       = get_if_empty(output, "bootstrap-scoped-{}.gzip".format(commit))
        
        cli.echo(cli_format("Writing to {}".format(target), cli.YELLOW))
        zipdir(source, target)

    if not no_cache:
        makedirs(defaults.DIRECTORY_CACHE, exist_ok = True)
        path = osp.join(defaults.DIRECTORY_CACHE, repo)
        _bootstrap_scope_repo(path)
    else:
        with tmpdir() as dirpath:
            path = osp.join(dirpath, repo)
            _bootstrap_scope_repo(path)