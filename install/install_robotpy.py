import subprocess
import os
import shutil

def check_executable(cmd):
    if shutil.which(cmd) == None:
        raise EnvironmentError('"%s" is not installed, or is not in the system $PATH' % cmd)

def gitclone_robotpy_to(path):
    check_executable("git")


print(shutil.which("git") != None)