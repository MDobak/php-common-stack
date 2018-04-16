#!/usr/bin/python
import re

class Version:
    def __init__(self, version):
        self.version = version

        parsed_version = re.match(r'^(?P<major>[0-9]+)(\.(?P<minor>[0-9]+)(\.(?P<patch>[0-9]+))?)?((?P<label>[A-Za-z]+)(?P<label_version>[0-9]+)?)?(-(?P<branch>.+))?$', version)
        self.version_parts = parsed_version.groupdict() if None != parsed_version else {}

        for key, value in self.version_parts.items():
            if value is None:
                self.version_parts[key] = ""

    def is_valid(self):
        return {} != self.version_parts

    def to_string(self):
        return self.version

    def to_short_version_string(self, include_branch=True):
        if include_branch and None != self.version_parts["branch"]:
            return self.version_parts["major"] + "." + self.version_parts["minor"] + "-" + self.version_parts["branch"]
        return self.version_parts["major"] + "." + self.version_parts["minor"]

    def to_short_version(self, include_branch=True):
        return Version(self.to_short_version_string(include_branch))

    def get_parts(self):
        return self.version_parts

    def to_tuple(self):
        if None == self.version_parts:
            return None

        version_parts = self.version_parts
        for group, value in version_parts.items():
            if group == "label" and value == "alpha":
                version_parts[group] = "0"
            elif group == "label" and value == "beta":
                version_parts[group] = "1"
            elif group == "label" and value == "RC":
                version_parts[group] = "2"
            elif group == "label" and value == "unstable":
                version_parts[group] = "3"
            elif group == "label" and value == "edge":
                version_parts[group] = "4"
            elif "" == value:
                version_parts[group] = "99999999"

        return (
            int(version_parts["major"]),
            int(version_parts["minor"]),
            int(version_parts["patch"]),
            int(version_parts["label"]),
            int(version_parts['label_version'])
        )

    def is_stable(self):
        return self.version_parts["label"] == "99999999"

    def __lt__(self, other):
        return Version.compare(self, other) < 0

    def __le__(self, other):
        return Version.compare(self, other) <= 0

    def __ne__(self, other):
        return Version.compare(self, other) != 0

    def __ge__(self, other):
        return Version.compare(self, other) >= 0

    def __gt__(self, other):
        return Version.compare(self, other) > 0

    def __eq__(self, other):
        if not isinstance(other, Version):
            return False

        return Version.compare(self, other) == 0

    @staticmethod
    def compare(version1, version2):
        if isinstance(version1, basestring):
            version1 = Version(version1)
        if isinstance(version2, basestring):
            version2 = Version(version2)

        v1 = version1.to_tuple()
        v2 = version2.to_tuple()

        if v1 == v2:
            return 0
        if v1 > v2:
            return 1
        if v1 < v2:
            return -1

    @staticmethod
    def highest(versions, from_version=None, to_version=None, stable_only=None, unstable_only=None):
        if 0 == len(versions):
            return None
        if None == from_version:
            from_version = "0.0.0alpha0"
        if None == to_version:
            to_version = "99999999.99999999.99999999edge99999999"
        if None == stable_only:
            stable_only = False
        if None == unstable_only:
            unstable_only = False

        from_version = Version(from_version)
        to_version = Version(to_version)

        highest = None
        for version_string in versions:
            version = Version(version_string)

            if version < from_version:
                continue

            if version > to_version:
                continue

            if stable_only and not version.is_stable():
                continue

            if unstable_only and version.is_stable():
                continue

            if None == highest:
                highest = version

            if version > highest:
                highest = version

        if highest == None:
            return None

        return highest.to_string()
