import subprocess
from os import path
def run(*args):
    subprocess.call(["sudo", path.dirname(__file__)+"/frcup.py"].extend(args), shell=True)