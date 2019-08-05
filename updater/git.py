#!/usr/bin/python
import os


class SelfUpdater:
    @staticmethod
    def reset():
        os.system("git checkout master")
        os.system("git reset --hard")

    @staticmethod
    def update(message):
        os.system("git add README.md")
        os.system("git add Dockerfile.*")
        os.system("git commit --message 'Travis build: " + SelfUpdater.__addslashes(message) + "'")
        os.system("git remote add origin-self-update https://" + os.environ[
            'GH_TOKEN'] + "@github.com/MDobak/php-common-stack.git > /dev/null 2>&1")
        os.system("git push --quiet origin-self-update master")

    @staticmethod
    def __addslashes(s):
        d = {'"': '\\"', "'": "\\'", "\0": "\\\0", "\\": "\\\\"}
        return ''.join(d.get(c, c) for c in s)
