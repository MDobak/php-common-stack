#!/usr/bin/python
import sys, os, time, commands

image = sys.argv[1]

def clean():
    os.system("docker rm -f test &> /dev/null");

def success():
    clean()
    sys.exit(0)

def fail(message):
    print message
    clean()
    sys.exit(1)

clean()
os.system("docker run -d -p 80:80 --name test " + image + "");

# Check if php is working
result = commands.getstatusoutput("docker exec test php -r 'echo \"Hello World!\";'")
if result[1] != "Hello World!":
    fail("PHP CLI do not work")

# Check if Apache is working
os.system("docker exec test bash -c 'echo \"<?php echo \\\"Hello World!\\\"; \" > /var/www/html/index.php'");
result = commands.getstatusoutput("curl -sS 127.0.0.1:80")
if result[1].strip() != "Hello World!":
    fail("Apache do not work")

success()
