import subprocess

def install(name, version):
    subprocess.call(['pip', 'install', name, '=', version])

install('pyVim', '0.0.20')