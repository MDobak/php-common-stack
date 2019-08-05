#!/usr/bin/python
import re


class Updater:
    def __init__(self, supported_tags, pushed_tags):
        self.supported_tags = supported_tags
        self.pushed_tags = pushed_tags

    def update(self):
        readme_file_content = open("./README.md", "r").read()
        tags_list = self.__build_tags_list()

        begin_line = "<!--- BEGIN_TAGS_LIST -->"
        end_line = "<!--- END_TAGS_LIST -->"

        readme_file_content = re.sub(
            re.escape(begin_line) + "(.*)" + re.escape(end_line),
            begin_line + "\n\n" + tags_list + "\n" + end_line,
            readme_file_content,
            flags=re.S
        )

        with open("./README.md", "w") as readme_file:
            readme_file.write(readme_file_content)

    def __build_tags_list(self):
        content = ""

        for supported_tag in self.supported_tags:
            tags = []
            for tag in self.pushed_tags:
                if tag.endswith("-" + supported_tag["branch"]):
                    tags.append("`" + tag + "`")

            content += "  * " + supported_tag["branch"] \
                       + " branch [(Dockerfile)](https://github.com/MDobak/php-common-stack/blob/master/" + \
                       supported_tag["output"] + "): " \
                       + ", ".join(tags) + "\n"

        return content
