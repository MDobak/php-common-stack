#!/usr/bin/python
import os
import sys

import subprocess

image = sys.argv[1]


def clean():
    os.system("docker rm -f test &> /dev/null")


def success():
    clean()
    sys.exit(0)


def fail(message):
    print(message)
    clean()
    sys.exit(1)


clean()
os.system("docker run -d -p 80:80 --name test " + image + "")

# Check if php is working
result = subprocess.getstatusoutput("docker exec test php -r 'echo \"Hello World!\";'")
if result[1] != "Hello World!":
    fail("PHP CLI do not work")

success()
