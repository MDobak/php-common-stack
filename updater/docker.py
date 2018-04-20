#!/usr/bin/python
import os, re, urllib, json, hashlib
from version import Version
from utils import CLIColor

class TagResolver:
    def __init__(self, tags):
        self.tags = tags

    def get_tags_for_branch(self, filter_regexp, branch):
        filtered_tags = filter(lambda x: None != re.match(filter_regexp, x) and Version(x).is_valid(), self.tags)
        filtered_tags.sort(cmp=Version.compare)

        short_versions = []
        for version in filtered_tags:
            short_version = Version(version).to_short_version_string(include_branch=False)
            if short_version not in short_versions:
                short_versions.append(short_version)

        highest_version = Version.highest(filtered_tags, stable_only=True)
        unstable_highest_version = Version.highest(filtered_tags, stable_only=False, unstable_only=True)
        highest_short_version = {}
        unstable_highest_short_version = {}

        for short_version in short_versions:
            highest_short_version[short_version] = Version.highest(
                filtered_tags, short_version + ".0alpha0", short_version, stable_only=True
            )
            unstable_highest_short_version[short_version] = Version.highest(
                filtered_tags, short_version + ".0alpha0", short_version, stable_only=False, unstable_only=True
            )

        possible_tags = {}
        for tag in filtered_tags:
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
        long_version = version_parts["major"] \
            + "." + version_parts["minor"] \
            + "." + version_parts["patch"] \
            + version_parts["label"] \
            + version_parts["label_version"]

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

class ImageBuilder:
    def __init__(self, parent_repo_tags, current_repo_tags):
        self.parent_repo_tags = parent_repo_tags
        self.current_repo_tags = current_repo_tags

    def build_dockerfile(self, template, output, filter_regexp, branch, variables):
        parent_tags = filter(lambda x: None != re.match(filter_regexp, x), self.parent_repo_tags)
        parent_tags.sort(cmp=Version.compare)

        tag_resolver = TagResolver(parent_tags)
        possible_tags = tag_resolver.get_tags_for_branch(filter_regexp, branch)
        highest_base_tag = Version.highest(possible_tags.keys(), stable_only=False)

        updated = self.__build_dockerfile(template, output, highest_base_tag, variables)

        if updated:
            return highest_base_tag

        return None

    def build_images(self, template, output, filter_regexp, branch, variables, test_script, limit=None):
        if limit is None:
            limit = 0

        parent_tags = filter(lambda x: None != re.match(filter_regexp, x), self.parent_repo_tags)
        parent_tags.sort(cmp=Version.compare)

        tag_resolver = TagResolver(parent_tags)
        possible_tags = tag_resolver.get_tags_for_branch(filter_regexp, branch)
        pushed_images_count = 0

        for base_tag, inherited_tags in possible_tags.items():
            self.__build_dockerfile(template, output, base_tag, variables)
            is_something_pushed = False
            is_something_built = False
            is_at_least_one_tag_missing = False

            for inherited_tag in inherited_tags:
                if inherited_tag not in self.current_repo_tags:
                    is_at_least_one_tag_missing = True
                    break

            for inherited_tag in inherited_tags:
                tag_already_build = inherited_tag in self.current_repo_tags

                if tag_already_build and not is_at_least_one_tag_missing:
                    continue

                print CLIColor.HEADER + "Building tag " + inherited_tag + " based on " + base_tag + CLIColor.ENDC
                    
                is_something_built = True
                self.current_repo_tags.append(inherited_tag)
                build_status_code = os.system("docker build -f " + output + " . -t \"mdobak/php-common-stack:" + inherited_tag + "\"")
                
                if 0 != build_status_code:
                    print CLIColor.FAIL + "Unable to build " + inherited_tag + CLIColor.ENDC
                    continue

                test_status_code = os.system(test_script + " \"mdobak/php-common-stack:" + inherited_tag + "\"")
                if 0 != test_status_code:
                    print CLIColor.FAIL + "Test failed for " + inherited_tag + CLIColor.ENDC
                    continue

                is_something_pushed = True
                pushed_images_count += 1
                os.system("docker push \"mdobak/php-common-stack:" + inherited_tag + "\"")

            if is_something_built:
                os.system("docker system prune -af")
                
            if is_something_pushed and limit > 0 and pushed_images_count >= limit:
                break

        return pushed_images_count

    def __build_dockerfile(self, template, output, base_tag, variables):
        current_file_hash = ""
        if os.path.isfile(output):
            current_file_hash = hashlib.md5(open(output, "rb").read()).hexdigest()

        with open(template, "r") as content_file:
            output_dockerfile_content = "" \
                "# THIS IS AN AUTOGENERATED FILE. DO NOT EDIT THIS FILE DIRECTLY\n" \
                "# Content of this file is based on " + template + "\n\n" \
                + content_file.read().replace('{{version}}', base_tag)

            for key, value in variables.items():
                output_dockerfile_content = output_dockerfile_content.replace('{{' + key + '}}', value)

        with open(output, "w") as output_dockerfile:
            output_dockerfile.write(output_dockerfile_content)

        return current_file_hash != hashlib.md5(open(output, "rb").read()).hexdigest()

class Repository:
    def __init__(self, name):
        repo_response = urllib.urlopen("https://registry.hub.docker.com/v1/repositories/" + name + "/tags")
        self.tags = map(lambda x: x["name"], json.loads(repo_response.read()))

    def get_tags(self):
        return self.tags
