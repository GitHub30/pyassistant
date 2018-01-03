import subprocess


def install(command,init):
    try:
        proc = subprocess.Popen(command.split(' '),stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        res = proc.communicate()
    except FileNotFoundError:
        print('package %s is not found'%command)
        print('install %s'%init)
        subprocess.call(init.split(' '))

    try:
        proc = subprocess.Popen(command.split(' '), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        res = proc.communicate()
    except FileNotFoundError:
        print('command %s could not installed by this command %s'%(command,init))
