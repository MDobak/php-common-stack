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

limit = 0
while commands.getstatusoutput("docker inspect --format '{{json .State.Health.Status }}' test")[1] != '"healthy"':
    limit += 1
    time.sleep(1)
    if limit >= 60:
        fail("Healtcheck failed")

# Check if supervisor is running
result = commands.getstatusoutput("docker exec test php -r 'echo \"Hello World!\";'")
if result[1] != "Hello World!":
    fail("PHP CLI do not work")

success()
