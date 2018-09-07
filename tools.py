import os
from subprocess import Popen

def execute(command, shell=True):
    p=Popen(command.split(), stderr=PIPE, stdout=PIPE)
    output, error = p.communicate()
    return output, error


