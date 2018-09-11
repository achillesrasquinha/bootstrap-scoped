# imports - standard imports
import os
import os.path as osp
import errno
from   subprocess      import Popen, PIPE, list2cmdline, CalledProcessError
from   distutils.spawn import find_executable
from   contextlib      import contextmanager
import shutil
import tempfile
import zipfile

# imports - module imports
from   bootstrap_scoped.util.string import strip, safe_decode

def read(fname):
    with open(fname) as f:
        data = f.read()
    return data

def write(fname, data = None, force = False):
    if not osp.exists(fname) or force:
        with open(fname, "w") as f:
            if data:
                f.write(data)

def remove(path, recursive = False, raise_err = True):
    path = osp.abspath(str(path))

    if osp.isdir(path):
        if recursive:
            shutil.rmtree(path)
        else:
            if raise_err:
                raise OSError("{path} is a directory.".format(
                    path = path
                ))
    else:
        try:
            os.remove(path)
        except OSError:
            if raise_err:
                raise

def which(exec_, raise_err = False):
    executable = find_executable(exec_)
    if not executable and raise_err:
        raise ValueError("{executable} executable not found.".format(
            executable = exec_
        ))
    
    return executable

def popen(*args, **kwargs):
    output      = kwargs.get("output", False)
    directory   = kwargs.get("cwd")
    environment = kwargs.get("env")
    shell       = kwargs.get("shell", True)
    raise_err   = kwargs.get("raise_err", True)

    environ     = os.environ.copy()
    if environment:
        environ.update(environment)

    for k, v in environ.items():
        environ[k] = str(v)

    command     = list2cmdline(args)
    
    proc        = Popen(command,
        stdin   = PIPE if output else None,
        stdout  = PIPE if output else None,
        stderr  = PIPE if output else None,
        env     = environ,
        cwd     = directory,
        shell   = shell
    )

    code        = proc.wait()

    if code and raise_err:
        raise CalledProcessError(code, command)

    if output:
        output, error = proc.communicate()

        if output:
            output = safe_decode(output)
            output = strip(output)

        if error:
            error  = safe_decode(error)
            error  = strip(error)

        return code, output, error
    else:
        return code

def makedirs(dirs, exist_ok = False):
    dirs = str(dirs)
    
    try:
        os.makedirs(dirs)
    except OSError as e:
        if not exist_ok or e.errno != errno.EEXIST:
            raise

@contextmanager
def tmpdir():
    dirpath = tempfile.mkdtemp()
    yield dirpath
    remove(dirpath, recursive = True)

def zipdir(source, target):
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as f:
        for root, _, files in os.walk(source):
            for file in files:
                path = osp.join(root, file)
                f.write(path, osp.relpath(path, start = osp.join(source, "..")))