#!/usr/bin/python
import re
from version import Version

class Resolver:
    def __init__(self, tags):
        self.tags = tags

    def get_tags_for_branch(self, filter_regexp, branch):
        filtered_tags = filter(lambda x: None != re.match(filter_regexp, x), self.tags)
        filtered_tags.sort(cmp=Version.compare)

        short_versions = []
        for version in self.tags:
            short_version = Version(version).to_short_version_string(include_branch=False)
            if short_version not in short_versions:
                short_versions.append(short_version)

        highest_version = Version.highest(filtered_tags, stable_only=True)
        unstable_highest_version = Version.highest(filtered_tags, stable_only=False, unstable_only=True)
        highest_short_version = {}
        unstable_highest_short_version = {}

        for short_version in short_versions:
            highest_short_version[short_version] = Version.highest(
                self.tags, short_version + ".0alpha0", short_version, stable_only=True
            )
            unstable_highest_short_version[short_version] = Version.highest(
                self.tags, short_version + ".0alpha0", short_version, stable_only=False, unstable_only=True
            )

        possible_tags = {}
        for tag in self.tags:
            possible_tags[tag] = self.__get_possible_tags(
                tag,
                highest_version,
                unstable_highest_version,
                highest_short_version,
                unstable_highest_short_version,
                filtered_tags,
                branch
            )

        return possible_tags

    def __get_possible_tags(
        self,
        tag,
        highest_version,
        unstable_highest_version,
        highest_short_version,
        unstable_highest_short_version,
        filtered_tags,
        branch
    ):
        version_tag = Version(tag)
        version_parts = version_tag.get_parts()
        short_version = version_tag.to_short_version_string(include_branch=False)
        long_version = version_parts["major"] + "." + version_parts["minor"] + "." + version_parts["patch"]

        possible_tags = []

        if tag == unstable_highest_version and not version_tag.is_stable():
            possible_tags.append(short_version + "unstable-" + branch)

        if tag == highest_version:
            possible_tags.append("latest-" + branch)

        if tag == highest_short_version[short_version]:
            possible_tags.append(short_version + "-" + branch)

        if tag == highest_version or tag == unstable_highest_version:
            possible_tags.append(short_version + "edge-" + branch)
            possible_tags.append("edge-" + branch)

        possible_tags.append(long_version + "-" + branch)

        return possible_tags
