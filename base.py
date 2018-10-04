import os
import argparse
from datetime import datetime
import sys

from git import Repo
import docker
from docker.errors import NotFound


class BaseImageBuilder(object):
    """Class to manage building base images
    """
    @staticmethod
    def get_root_dir() -> str:
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
        repo = Repo(self.get_root_dir())
        return repo.head.commit.hexsha

    def _generate_image_tag_suffix(self) -> str:
        """Method to generate a suffix for an image tag

        Returns:
            str
        """
        return "{}-{}".format(self._get_current_commit_hash()[:10], str(datetime.utcnow().date()))

    def build(self, image_name: str, namespace: str, repository: str, no_cache=False) -> str:
        """

        Args:
            image_name(str): Name of the image (and directory containing the Dockerfile)
            namespace(str): Namespace to publish to on dockerhub
            repository(str): Name of the repository to publish to on dockerhub
            no_cache(bool): If True, don't use the docker build cache

        Returns:

        """
        client = docker.from_env()

        named_tag = f"{namespace}/{repository}:{self._generate_image_tag_suffix()}"
        build_dir = os.path.join(self.get_root_dir(), image_name)

        [print(ln[list(ln.keys())[0]], end='') for ln in client.api.build(path=build_dir,
                                                                          tag=named_tag,
                                                                          nocache=no_cache,
                                                                          pull=True, rm=True,
                                                                          decode=True)]

        # Verify the desired image built successfully
        try:
            client.images.get(named_tag)
        except NotFound:
            raise ValueError("Image Build Failed!")

        return named_tag

    def publish(self, tagged_image_name: str) -> bool:
        """Private method to push images to the logged in server (e.g hub.docker.com)

        Args:
            tagged_image_name(str): full image name + tag to publish

        Returns:
            None
        """
        client = docker.from_env()

        # Split out the image and the tag
        image, tag = tagged_image_name.split(":")

        last_msg = ""
        successful = True
        for ln in client.api.push(image, tag=tag, stream=True, decode=True):
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
    parser.add_argument("--repository", "-r",
                        help="Push to a non-default repository. Use this option if you are an open source user "
                             "and can't push to Gigantum Official repositories. Format: `namespace/repository`")
    parser.add_argument("--no-cache",
                        default=False,
                        action='store_true',
                        help="Boolean indicating if docker cache should be ignored")
    parser.add_argument("base_image",
                        help="Name of the base image to build (same as the directory name)")

    args = parser.parse_args()
    builder = BaseImageBuilder()

    # Validate image is available to build
    if not os.path.exists(os.path.join(builder.get_root_dir(), args.base_image)):
        raise ValueError(f"Base not found: {args.base_image}")

    # Set target repo info
    if args.repository:
        repository_str = args.repository
    else:
        repository_str = f"gigantum/{args.base_image}"
    namespace, repository = repository_str.split("/")

    # Build
    print("\n\nStep 1: Building Image\n\n")
    image_str = builder.build(args.base_image, namespace, repository, args.no_cache)

    if args.build_only:
        print("Skipping publish operation.")
    else:
        print("\n\nStep 2: Publishing Image\n\n")
        # Publish
        successful = builder.publish(image_str)

        _, tag = image_str.split(":")
        if successful:
            print(f"** Successfully pushed image to {image_str} **\n")
            print(f"To use this new base:")
            print(f" - Create a new base specification yaml file (remember to increment the revision in the file!)")
            print(f" - Update the base information:")
            print(f"    - namespace: {namespace}")
            print(f"    - repository: {repository}")
            print(f"    - tag: {tag}")
            print(f" - Commit changes to this repo and push to GitHub (make sure your Client config file points to"
                  f" both the repository and branch if not default)")

            print(f"\n\nIf pushing official bases, remember they `go live` as soon as your PR is accepted to master.")


if __name__ == '__main__':
    main()
