#!/usr/bin/python
import urllib, json, re, os, argparse, hashlib, time
from updater import *

parent_repo = "php"
current_repo = "mdobak/php-common-stack"

supported_tags = [
    # FPM
    {
        "template": "Dockerfile.template-debian",
        "filter_regexp": r'^(5\.4|5\.5|5\.6|7\.[0-9]+)\.([0-9]+)((alpha|beta|RC)([0-9]*))?-fpm$',
        "branch": "fpm",
        "output": "Dockerfile.fpm",
        "variables": {'supervisor_path': "fpm"},
        "test_script": "python tests/fpm.py"
    },

    # Apache
    {
        "template": "Dockerfile.template-debian",
        "filter_regexp": r'^(5\.4|5\.5|5\.6|7\.[0-9]+)\.([0-9]+)((alpha|beta|RC)([0-9]*))?-apache$',
        "branch": "apache",
        "output": "Dockerfile.apache",
        "variables": {'supervisor_path': "apache"},
        "test_script": "python tests/apache.py"
    },

    # CLI
    {
        "template": "Dockerfile.template-debian",
        "filter_regexp": r'^(5\.4|5\.5|5\.6|7\.[0-9]+)\.([0-9]+)((alpha|beta|RC)([0-9]*))?-cli$',
        "branch": "cli",
        "output": "Dockerfile.cli",
        "variables": {'supervisor_path': "cli"},
        "test_script": "python tests/cli.py"
    },

    # FPM Jessie
    {
        "template": "Dockerfile.template-debian",
        "filter_regexp": r'^(5\.4|5\.5|5\.6|7\.[0-9]+)\.([0-9]+)((alpha|beta|RC)([0-9]*))?-fpm-jessie$',
        "branch": "fpm-jessie",
        "output": "Dockerfile.fpm-jessie",
        "variables": {'supervisor_path': "fpm"},
        "test_script": "python tests/fpm.py"
    },

    # Apache Jessie
    {
        "template": "Dockerfile.template-debian",
        "filter_regexp": r'^(5\.4|5\.5|5\.6|7\.[0-9]+)\.([0-9]+)((alpha|beta|RC)([0-9]*))?-apache-jessie$',
        "branch": "apache-jessie",
        "output": "Dockerfile.apache-jessie",
        "variables": {'supervisor_path': "apache"},
        "test_script": "python tests/apache.py"
    },

    # CLI Jessie
    {
        "template": "Dockerfile.template-debian",
        "filter_regexp": r'^(5\.4|5\.5|5\.6|7\.[0-9]+)\.([0-9]+)((alpha|beta|RC)([0-9]*))?-cli-jessie$',
        "branch": "cli-jessie",
        "output": "Dockerfile.cli-jessie",
        "variables": {'supervisor_path': "cli"},
        "test_script": "python tests/cli.py"
    },

    # FPM Stretch
    {
        "template": "Dockerfile.template-debian",
        "filter_regexp": r'^(5\.4|5\.5|5\.6|7\.[0-9]+)\.([0-9]+)((alpha|beta|RC)([0-9]*))?-fpm-stretch$',
        "branch": "fpm-stretch",
        "output": "Dockerfile.fpm-stretch",
        "variables":
        {'supervisor_path': "fpm"},
        "test_script": "tests/fpm.py"
    },

    # Apache Stretch
    {
        "template": "Dockerfile.template-debian",
        "filter_regexp": r'^(5\.4|5\.5|5\.6|7\.[0-9]+)\.([0-9]+)((alpha|beta|RC)([0-9]*))?-apache-stretch$',
        "branch": "apache-stretch",
        "output": "Dockerfile.apache-stretch",
        "variables": {'supervisor_path': "apache"},
        "test_script": "tests/apache.py"
    },

    # CLI Stretch
    {
        "template": "Dockerfile.template-debian",
        "filter_regexp": r'^(5\.4|5\.5|5\.6|7\.[0-9]+)\.([0-9]+)((alpha|beta|RC)([0-9]*))?-cli-stretch$',
        "branch": "cli-stretch",
        "output": "Dockerfile.cli-stretch",
        "variables": {'supervisor_path': "cli"},
        "test_script": "tests/cli.py"
    },
    
    # FPM Buster
    {
        "template": "Dockerfile.template-debian",
        "filter_regexp": r'^(5\.4|5\.5|5\.6|7\.[0-9]+)\.([0-9]+)((alpha|beta|RC)([0-9]*))?-fpm-buster$',
        "branch": "fpm-buster",
        "output": "Dockerfile.fpm-buster",
        "variables":
            {'supervisor_path': "fpm"},
        "test_script": "tests/fpm.py"
    },

    # Apache Buster
    {
        "template": "Dockerfile.template-debian",
        "filter_regexp": r'^(5\.4|5\.5|5\.6|7\.[0-9]+)\.([0-9]+)((alpha|beta|RC)([0-9]*))?-apache-buster$',
        "branch": "apache-buster",
        "output": "Dockerfile.apache-buster",
        "variables": {'supervisor_path': "apache"},
        "test_script": "tests/apache.py"
    },

    # CLI Buster
    {
        "template": "Dockerfile.template-debian",
        "filter_regexp": r'^(5\.4|5\.5|5\.6|7\.[0-9]+)\.([0-9]+)((alpha|beta|RC)([0-9]*))?-cli-buster$',
        "branch": "cli-buster",
        "output": "Dockerfile.cli-buster",
        "variables": {'supervisor_path': "cli"},
        "test_script": "tests/cli.py"
    },

    # FPM Alpine
    {
        "template": "Dockerfile.template-alpine",
        "filter_regexp": r'^(5\.4|5\.5|5\.6|7\.[0-9]+)\.([0-9]+)((alpha|beta|RC)([0-9]*))?-fpm-alpine$',
        "branch": "fpm-alpine",
        "output": "Dockerfile.fpm-alpine",
        "variables": {'supervisor_path': "fpm-alpine"},
        "test_script": "python tests/fpm.py"
    },

    # CLI Alpine
    {
        "template": "Dockerfile.template-alpine",
        "filter_regexp": r'^(5\.4|5\.5|5\.6|7\.[0-9]+)\.([0-9]+)((alpha|beta|RC)([0-9]*))?-cli-alpine$',
        "branch": "cli-alpine",
        "output": "Dockerfile.cli-alpine",
        "variables": {'supervisor_path': "cli-alpine"},
        "test_script": "python tests/cli.py"
    },

    # FPM Alpine 3.6
    {
        "template": "Dockerfile.template-alpine",
        "filter_regexp": r'^(5\.4|5\.5|5\.6|7\.[0-9]+)\.([0-9]+)((alpha|beta|RC)([0-9]*))?-fpm-alpine3.6$',
        "branch": "fpm-alpine3.6",
        "output": "Dockerfile.fpm-alpine",
        "variables": {'supervisor_path': "fpm-alpine"},
        "test_script": "python tests/fpm.py"
    },

    # CLI Alpine 3.6
    {
        "template": "Dockerfile.template-alpine",
        "filter_regexp": r'^(5\.4|5\.5|5\.6|7\.[0-9]+)\.([0-9]+)((alpha|beta|RC)([0-9]*))?-cli-alpine3.6$',
        "branch": "cli-alpine3.6",
        "output": "Dockerfile.cli-alpine",
        "variables": {'supervisor_path': "cli-alpine"},
        "test_script": "python tests/cli.py"
    },

    # FPM Alpine 3.7
    {
        "template": "Dockerfile.template-alpine",
        "filter_regexp": r'^(5\.4|5\.5|5\.6|7\.[0-9]+)\.([0-9]+)((alpha|beta|RC)([0-9]*))?-fpm-alpine3.7$',
        "branch": "fpm-alpine3.7",
        "output": "Dockerfile.fpm-alpine",
        "variables": {'supervisor_path': "fpm-alpine"},
        "test_script": "python tests/fpm.py"
    },

    # CLI Alpine 3.7
    {
        "template": "Dockerfile.template-alpine",
        "filter_regexp": r'^(5\.4|5\.5|5\.6|7\.[0-9]+)\.([0-9]+)((alpha|beta|RC)([0-9]*))?-cli-alpine3.7$',
        "branch": "cli-alpine3.7",
        "output": "Dockerfile.cli-alpine",
        "variables": {'supervisor_path': "cli-alpine"},
        "test_script": "python tests/cli.py"
    },

    # FPM Alpine 3.8
    {
        "template": "Dockerfile.template-alpine",
        "filter_regexp": r'^(5\.4|5\.5|5\.6|7\.[0-9]+)\.([0-9]+)((alpha|beta|RC)([0-9]*))?-fpm-alpine3.8$',
        "branch": "fpm-alpine3.8",
        "output": "Dockerfile.fpm-alpine",
        "variables": {'supervisor_path': "fpm-alpine"},
        "test_script": "python tests/fpm.py"
    },

    # CLI Alpine 3.8
    {
        "template": "Dockerfile.template-alpine",
        "filter_regexp": r'^(5\.4|5\.5|5\.6|7\.[0-9]+)\.([0-9]+)((alpha|beta|RC)([0-9]*))?-cli-alpine3.8$',
        "branch": "cli-alpine3.8",
        "output": "Dockerfile.cli-alpine",
        "variables": {'supervisor_path': "cli-alpine"},
        "test_script": "python tests/cli.py"
    },

    # FPM Alpine 3.9
    {
        "template": "Dockerfile.template-alpine",
        "filter_regexp": r'^(5\.4|5\.5|5\.6|7\.[0-9]+)\.([0-9]+)((alpha|beta|RC)([0-9]*))?-fpm-alpine3.9$',
        "branch": "fpm-alpine3.9",
        "output": "Dockerfile.fpm-alpine",
        "variables": {'supervisor_path': "fpm-alpine"},
        "test_script": "python tests/fpm.py"
    },

    # CLI Alpine 3.9
    {
        "template": "Dockerfile.template-alpine",
        "filter_regexp": r'^(5\.4|5\.5|5\.6|7\.[0-9]+)\.([0-9]+)((alpha|beta|RC)([0-9]*))?-cli-alpine3.9$',
        "branch": "cli-alpine3.9",
        "output": "Dockerfile.cli-alpine",
        "variables": {'supervisor_path': "cli-alpine"},
        "test_script": "python tests/cli.py"
    },

    # FPM Alpine 3.10
    {
        "template": "Dockerfile.template-alpine",
        "filter_regexp": r'^(5\.4|5\.5|5\.6|7\.[0-9]+)\.([0-9]+)((alpha|beta|RC)([0-9]*))?-fpm-alpine3.10$',
        "branch": "fpm-alpine3.10",
        "output": "Dockerfile.fpm-alpine",
        "variables": {'supervisor_path': "fpm-alpine"},
        "test_script": "python tests/fpm.py"
    },

    # CLI Alpine 3.10
    {
        "template": "Dockerfile.template-alpine",
        "filter_regexp": r'^(5\.4|5\.5|5\.6|7\.[0-9]+)\.([0-9]+)((alpha|beta|RC)([0-9]*))?-cli-alpine3.10$',
        "branch": "cli-alpine3.10",
        "output": "Dockerfile.cli-alpine",
        "variables": {'supervisor_path': "cli-alpine"},
        "test_script": "python tests/cli.py"
    },
]

blacklisted_tags = [
    # Missing OpenSSL:
    "5.4.32-apache",
    "5.5.16-apache",
    "5.6.0-apache",
    "5.4.32-cli",
    "5.4.34-cli",
    "5.5.16-cli",
    "5.6.0-cli",

    # Missing apache2-foreground:
    "5.4.33-apache",
    "5.4.34-apache",
    "5.4.35-apache",
    "5.5.17-apache",
    "5.5.18-apache",
    "5.5.19-apache",
    "5.6.1-apache",
    "5.6.2-apache",
    "5.6.3-apache"
]

def update_dockerfiles(supported_tags):
    new_tags = []

    for supported_tag in supported_tags:
        new_tag = docker_image_builder.build_dockerfile(
            supported_tag["template"],
            supported_tag["output"],
            supported_tag["filter_regexp"],
            supported_tag["branch"],
            supported_tag["variables"]
        )

        if None != new_tag:
            new_tags.append(new_tag)

    return new_tags

def update_images(supported_tags, time_limit):
    end_at = time.time() + time_limit

    for supported_tag in supported_tags:
        while True:
            pushed_images_count = docker_image_builder.build_images(
                supported_tag["template"],
                supported_tag["output"],
                supported_tag["filter_regexp"],
                supported_tag["branch"],
                supported_tag["variables"],
                supported_tag["test_script"],
                1
            )

            if time_limit != 0 and time.time() >= end_at:
                return

            if 0 == pushed_images_count:
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Docker images manager")
    parser.add_argument("-a", "--action", required=True, choices=["update-dockerfiles", "self-update", "update-images", "list-tags"])
    parser.add_argument("-t", "--time-limit", required=False, default=0)
    parser.add_argument("-f", "--force", required=False, action="store_true")

    args = parser.parse_args()

    parent_repo_tags = docker.Repository(parent_repo).get_tags()
    current_repo_tags = [] if args.force else docker.Repository(current_repo).get_tags()
    docker_image_builder = docker.ImageBuilder(parent_repo_tags, current_repo_tags)

    for tag in blacklisted_tags:
        parent_repo_tags.remove(tag)

    if "update-dockerfiles" == args.action:
        update_dockerfiles(supported_tags)

    elif "self-update" == args.action:
        git.SelfUpdater.reset()

        new_tags = update_dockerfiles(supported_tags)
        if len(new_tags) > 0:
            readme_updater = readme.Updater(supported_tags, current_repo_tags)
            readme_updater.update()
            git.SelfUpdater.update("Updated to versions: " + ", ".join(new_tags))

    elif "update-images" == args.action:
        update_images(supported_tags, int(args.time_limit))
        update_dockerfiles(supported_tags)

    elif "list-tags" == args.action:
        tag_resolver = docker.TagResolver(parent_repo_tags)
        for supported_tag in supported_tags:
            possible_tags = tag_resolver.get_tags_for_branch(supported_tag["filter_regexp"], supported_tag["branch"])
            for tag, possible_tags in possible_tags.items():
                print(tag + ": " + ",".join(possible_tags))
