import os
import json
import glob
from datetime import datetime
from pkg_resources import resource_filename

from git import Repo
import docker
from docker.errors import NotFound


class BaseImageBuilder(object):
    """Class to manage building base images
    """
    def __init__(self):
        """

        """
        self.tracking_file = os.path.join(self._get_root_dir(), ".image-build-status.json")

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
        repo = Repo(self._get_root_dir())
        return repo.head.commit.hexsha

    def _generate_image_tag_suffix(self) -> str:
        """Method to generate a suffix for an image tag

        Returns:
            str
        """
        return "{}-{}".format(self._get_current_commit_hash()[:10], str(datetime.utcnow().date()))

    def _load_tracking_file(self) -> dict:
        """Method to open or create the tracking file

        Format:
            {
                base-name: [{tag: str, is_published: bool, build_on: datetime),]
            }

        Returns:
            dict
        """
        if os.path.isfile(self.tracking_file):
            with open(self.tracking_file, "rt") as f:
                data = json.load(f)
        else:
            # No tracking file exists
            data = dict()
        return data

    def _save_tracking_file(self, data) -> None:
        """Method to save the tracking file

        Format:
            {
                base-name: {tag: {is_published: bool, build_on: datetime},}
            }

        Returns:
            dict
        """
        with open(self.tracking_file, "wt") as f:
            json.dump(data, f)

    def _record_image_build(self, base_name: str, image_tag: str) -> None:
        """Method to update the status of an image in the tracking file, which is used to control publishing and
        prune commands. Use this method to record when an image finishes building.

        Args:
            base_name(str): Name of the base being built
            image_tag(str): Image tag

        Returns:
            None
        """
        data = self._load_tracking_file()

        if base_name not in data.keys():
            data[base_name] = dict()

        data[base_name] = {"tag": image_tag, "is_published": False, "build_on": datetime.utcnow()}

        self._save_tracking_file(data)

    def _record_image_publish(self, base_name: str, image_tag: str, is_built: bool, is_published: bool) -> None:
        """Method to update the status of an image in the tracking file, which is used to control publishing and
        prune commands

        Format:

            {
                base-name: [{tag: str, is_published: bool, build_on: datetime),]
            }

        Args:
            is_built(bool): Flag indicating if the image has been built
            is_published(bool): Flag indiciating if the image has been published
            image_tag(str): Name of the built image

        Returns:
            None
        """
        if os.path.isfile(self.tracking_file):
            with open(self.tracking_file, "rt") as f:
                data = json.load(f)

        else:
            # No tracking file exists
            data = {}

        # Update the dictionary setting publish to False
        data[image_tag] = {"isBuilt": built, "isPublished": published}

        with open(self.tracking_file, "wt") as f:
            json.dump(data, f)

    def _build_image(self, build_dir: str, verbose=False, no_cache=False) -> str:
        """

        Args:
            build_dir:

        Returns:

        """
        client = docker.from_env()

        # Generate tags for both the named and latest versions
        base_tag = "gigantum/{}".format(os.path.basename(os.path.normpath(build_dir)))
        named_tag = "{}:{}".format(base_tag, self._generate_image_tag_suffix())

        # If a "minimal" image that could be the source for other images, you should pull, otherwise, you shouldn't
        if "minimal" in base_tag:
            pull = True
        else:
            pull = False

        if verbose:
            [print(ln[list(ln.keys())[0]], end='') for ln in client.api.build(path=build_dir,
                                                                              tag=named_tag,
                                                                              nocache=no_cache,
                                                                              pull=pull, rm=True,
                                                                              decode=True)]
        else:
            client.images.build(path=build_dir, tag=named_tag, pull=pull, nocache=no_cache)

        # Tag with latest in case images depend on each other. Will not get published.
        client.images.get(named_tag).tag(f"{base_tag}:latest")

        # Verify the desired image built successfully
        try:
            client.images.get(named_tag)
        except NotFound:
            raise ValueError("Image Build Failed!")

        return named_tag

    def _publish_image(self, image_tag: str, verbose=False) -> None:
        """Private method to push images to the logged in server (e.g hub.docker.com)

        Args:
            image_tag(str): full image tag to publish

        Returns:
            None
        """
        client = docker.from_env()

        # Split out the image and the tag
        image, tag = image_tag.split(":")

        if verbose:
            [print(ln[list(ln.keys())[0]], end='') for ln in client.api.push(image, tag=tag,
                                                                             stream=True, decode=True)]
        else:
            client.images.push(image, tag=tag)

    def build(self, image_name: str = None, verbose=False, no_cache=False) -> None:
        """Method to build all, or a single image based on the dockerfiles stored within the base-image submodule

        Args:
            image_name(str): Name of a base image to build. If omitted all are built
            verbose(bool): flag indication if output should print to the console
            no_cache(bool): flag indicating if the docker cache should be ignored

        Returns:
            None
        """
        build_dirs = []
        if not image_name:
            # Find all images to build in the base_image submodule ref
            docker_file_dir = os.path.join(resource_filename('gtmlib', 'resources'), 'submodules', 'base-images')
            build_dirs = glob.glob(os.path.join(docker_file_dir,
                                                "*"))
            build_dirs = [x for x in build_dirs if os.path.isdir(x) is True]

        else:
            possible_build_dir = os.path.join(resource_filename('gtmlib', 'resources'), 'submodules',
                                              'base-images', image_name)
            if os.path.isdir(possible_build_dir):
                build_dirs.append(possible_build_dir)
            else:
                raise ValueError("Image `{}` not found.".format(image_name))

        if not build_dirs:
            raise ValueError("No images to build")

        # Make sure minimals are always built first
        for cnt, base in enumerate(build_dirs):
            if "minimal" in base:
                build_dirs.insert(0, build_dirs.pop(cnt))

        for cnt, build_dir in enumerate(build_dirs):
            print("({}/{}) Building Base Image: {}".format(cnt+1, len(build_dirs),
                                                           os.path.basename(os.path.normpath(build_dir))))
            # Build each image
            image_tag = self._build_image(build_dir, verbose=verbose, no_cache=no_cache)

            # Update tracking file
            self._update_tracking_file(image_tag, built=True, published=False)

            print(" - Complete")
            print(" - Tag: {}".format(image_tag))

    def publish(self, image_name: str = None, verbose=False) -> None:
        """Method to publish images and update the Environment Repository

        Args:
            image_name(str): Name of a base image to build. If omitted all are built

        Returns:
            None
        """
        # Open tracking file
        if os.path.isfile(self.tracking_file):
            with open(self.tracking_file, "rt") as f:
                tracking_data = json.load(f)
        else:
            raise ValueError("You must first build images locally before publishing")

        # Prune out all but unpublished images
        tags_to_push = [x for x in list(tracking_data.keys()) if tracking_data[x]['isPublished'] is False]

        if image_name:
            # Prune out all but the image to publish
            if image_name in tags_to_push:
                tags_to_push = [image_name]
            else:
                raise ValueError("Image `{}` not found.".format(image_name))

        num_images = len(tags_to_push)
        for cnt, image_tag in enumerate(tags_to_push):
            print("({}/{}) Publishing Base Image: {}".format(cnt+1, num_images, image_tag))

            # Publish each image
            self._publish_image(image_tag, verbose)

            # TODO Update YAML def

            # Update tracking file
            self._update_tracking_file(image_tag, built=True, published=True)

            print(" - Complete")
            print(" - Tag: {}".format(image_tag))