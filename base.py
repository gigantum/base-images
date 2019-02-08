#!/usr/bin/env python
import os
import argparse
from datetime import datetime
import sys
from typing import List, Tuple
import json
import subprocess
import glob
import yaml

import docker
from docker.errors import NotFound


class BaseImageBuilder(object):
    """Class to manage building base images
    """
    def __init__(self, args):
        self.args = args
        self.client = docker.from_env()

    @staticmethod
    def _get_root_dir() -> str:
        """Method to get the root base-images directory

        Returns:
            str
        """
        return os.path.dirname(os.path.abspath(__file__))

    def _get_current_commit_hash(self) -> str:
        """Method to get the current commit hash of the gtm repository

        Returns:
            str
        """
        # Get the path of the root directory
        result = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=self._get_root_dir(), check=True,
                                stdout=subprocess.PIPE)
        if result.returncode != 0:
            raise IOError(f"Failed to look up current commit hash: {result.stderr}")
        return result.stdout.decode().strip()

    def _generate_image_tag_suffix(self) -> str:
        """Method to generate a suffix for an image tag

        Returns:
            str
        """
        return "{}-{}".format(self._get_current_commit_hash()[:10], str(datetime.utcnow().date()))

    def _get_bases_to_build(self) -> List[str]:
        """Get list of base names directories to build

        Returns:
            str
        """
        ignore_dirs = ['.git', '.github', '_templates']

        if self.args.base_image == 'all':
            print("Building all Base images")
            base_names = [x[0] for x in os.walk(self._get_root_dir()) if x[0] not in ignore_dirs]
        else:
            # Validate specific image specified is available to build
            base_dir = os.path.join(self._get_root_dir(), self.args.base_image)
            if not os.path.exists(base_dir):
                raise ValueError(f"Base not found: {self.args.base_image}")
            base_names = [self.args.base_image]

        return base_names

    def _auto_update_base_config_yaml(self, base_image_name: str, namespace: str, repository: str, tag: str) -> str:
        """Method to automatically update a base config yaml after successful build/publish

        Returns:
            str
        """
        base_image_dir = os.path.join(self._get_root_dir(), base_image_name)

        # Get latest revision file
        base_config_files = glob.glob(os.path.join(base_image_dir, "*.yaml"))
        config_info = list()
        for b in base_config_files:
            with open(b, 'rt') as bf:
                data = yaml.safe_load(bf)

            config_info.append((data['revision'], b))
        config_info = sorted(config_info, key=lambda x: x[0], reverse=True)

        # Load current file
        with open(config_info[0][1], 'rt') as bf:
            base_config_data = yaml.safe_load(bf)

        # Update file contents
        new_revision = config_info[0][0] + 1
        base_config_data['revision'] = new_revision
        base_config_data['image']['namespace'] = namespace
        base_config_data['image']['repository'] = repository
        base_config_data['image']['tag'] = tag

        # write new file
        new_config_file = os.path.join(self._get_root_dir(), base_image_name,
                                       f"{base_image_name}_r{new_revision}.yaml")
        with open(new_config_file, 'wt') as bf:
            yaml.safe_dump(base_config_data, bf, default_flow_style=False)

        return new_config_file

    def _build(self, base_dir: str, namespace: str, repository: str, no_cache=False) -> Tuple[str, str, str]:
        """

        Args:
            base_dir(str): Directory for the base to build, containing a Dockerfile or template info
            namespace(str): Namespace to publish to on dockerhub
            repository(str): Name of the repository to publish to on dockerhub
            no_cache(bool): If True, don't use the docker build cache

        Returns:

        """
        build_args = None
        if os.path.isfile(os.path.join(base_dir, "dockerfile_template.json")):
            with open(os.path.join(base_dir, "dockerfile_template.json"), 'rt') as tf:
                template_data = json.load(tf)
            build_dir = os.path.join(self._get_root_dir(), '_templates', template_data['template'])
            build_args = template_data['args']
        else:
            build_dir = base_dir

        if not os.path.isfile(os.path.join(build_dir, "Dockerfile")):
            raise ValueError(f"Could not find Dockerfile in {build_dir}")

        tag = self._generate_image_tag_suffix()
        named_tag = f"{namespace}/{repository}:{tag}"

        [print(ln[list(ln.keys())[0]], end='') for ln in self.client.api.build(path=build_dir,
                                                                               tag=named_tag,
                                                                               nocache=no_cache,
                                                                               pull=True, rm=True,
                                                                               buildargs=build_args,
                                                                               decode=True)]

        # Verify the desired image built successfully
        try:
            self.client.images.get(named_tag)
        except NotFound:
            raise ValueError(f"Image Build Failed for {base_dir}")

        return namespace, repository, tag

    def _publish(self, namespace: str, repository: str, tag: str) -> bool:
        """Private method to push images to the logged in server (e.g hub.docker.com)

        Args:
            namespace(str): namespace to publish
            repository(str): repo to publish
            tag(str): tag to publish

        Returns:
            None
        """
        # Split out the image and the tag
        image = f"{namespace}/{repository}"

        last_msg = ""
        successful = True
        for ln in self.client.api.push(image, tag=tag, stream=True, decode=True):
            if 'status' in ln:
                if last_msg != ln.get('status'):
                    print(f"\n{ln.get('status')}", end='', flush=True)
                    last_msg = ln.get('status')
                else:
                    print(".", end='', flush=True)

            elif 'error' in ln:
                sys.stderr.write(f"\n{ln.get('error')}\n")
                sys.stderr.flush()
                successful = False
            else:
                print(ln)

        return successful

    @staticmethod
    def _print_results(publish_results: List[dict]):
        for result in publish_results:
            img_str = f"{result['namespace']}/{result['repository']}:{result['tag']}"
            if not result['generated_yaml']:
                print(f"\n\nSuccessfully pushed image to {img_str}. To use this new base:\n")
                print(f" - Create a new base configuration yaml file (remember to increment the revision in the file!)")
                print(f" - Update the base information:")
                print(f"    - namespace: {result['namespace']}")
                print(f"    - repository: {result['repository']}")
                print(f"    - tag: {result['tag']}")

            else:
                print(f"\n\nSuccessfully pushed image to {img_str}.\n")
                print(f" -  Base configuration yaml file automatically generated: {result['generated_yaml']}")

        if publish_results:
            print(f" \n\nCommit changes to this repo and push to GitHub (make sure your Client config file points to"
                  f" both the repository and branch if not default to test changes)")
            print(f"\n\nNote: If pushing official bases, remember they `go live` as soon as your "
                  f"PR is accepted to master!")

    def run(self):
        """

        Returns:

        """
        bases_to_build = self._get_bases_to_build()

        publish_results = list()
        for cnt, base_image_name in enumerate(bases_to_build):
            print(f"\n\n------ Building {base_image_name} ({cnt + 1} of {len(bases_to_build)}) ------\n\n")

            namespace = self.args.namespace
            base_image_dir = os.path.join(self._get_root_dir(), base_image_name)

            namespace, repository, tag = self._build(base_image_dir, namespace, base_image_name, self.args.no_cache)

            if self.args.build_only:
                print("  - Skipping publish operation")
            else:
                print(f"\n\n------ Publishing {cnt + 1} of {len(bases_to_build)} ------\n\n")
                successful = self._publish(namespace, repository, tag)

                base_config_yaml = None
                if successful and self.args.generate_base_config_yaml:
                    base_config_yaml = self._auto_update_base_config_yaml(base_image_name, namespace, repository, tag)

                publish_results.append({"namespace": namespace,
                                        "repository": repository,
                                        "tag": tag,
                                        "generated_yaml": base_config_yaml,
                                        "published": successful})

        self._print_results(publish_results)


def main():
    description_str = "A simple tool to build and publish base images to DockerHub. \n\n"
    description_str = description_str + "  Run `python3 base.py <base-image-name> <options>` to build and " \
                                        "publish an image.\n\n"
    description_str = description_str + "  Run `python3 base.py -h` to view available options\n"

    parser = argparse.ArgumentParser(description=description_str,
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("--build-only", "-b",
                        default=False,
                        action='store_true',
                        help="Only build the image. Do not publish after build is complete.")
    parser.add_argument("--namespace", "-n",
                        default="gigantum",
                        help="Push to a non-default namespace. Use this option if you are an open source user "
                             "and can't push to Gigantum Official repositories.")
    parser.add_argument("--no-cache",
                        default=False,
                        action='store_true',
                        help="Boolean indicating if docker cache should be ignored")
    parser.add_argument("--generate-base-config-yaml", "-g",
                        default=False,
                        action='store_true',
                        help="Boolean indicating if base image configuration files "
                             "should be auto-generated after publish operation succeeds")
    parser.add_argument("base_image",
                        help="Name of the base image to build (same as the directory name) or the string 'all' if you"
                             " want to build all the images at once (this is useful when simply rebuilding bases "
                             "for security updates)")

    args = parser.parse_args()
    builder = BaseImageBuilder(args)
    builder.run()


if __name__ == '__main__':
    main()
