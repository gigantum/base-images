# Gigantum Client Base Images

A repository to maintain Docker images for Gigantum Project environments. 

## Overview

Bases are pre-built Docker images that serve as the "base" compute environment for Gigantum Projects. When creating a
project you select a base and then can interactively customize it via the Gigantum Client UI.

`minimal` bases typically contain just the bare necessities required to run a development environment. Other bases
include additional packages to help get a user moving faster.

This repository maintains the Dockerfiles and "base specification" yaml files used by the Gigantum Client to track bases and render the UI.


## Users

If you are simply a user of the Gigantum Client, you don't need to interact with this repository. The client will
automatically checkout the repository listed in its configuration file and pull images as needed.

To get the Gigantum Client, see the [download instructions](https://gigantum.com/download).


## Development

### Contributing

Gigantum uses the [Developer Certificate of Origin](https://developercertificate.org/). 
This is lightweight approach that doesn't require submission and review of a
separate contributor agreement.  Code is signed directly by the developer using
facilities built into git.

Please see [contributing.md](contributing.md).

### Building and Publishing Updates

To build and publish images a tool is provided in `base.py`. This command line application builds and publishes
individual bases. Simply run `python3 base.py <base-name>` to build and push the image. Options:


```
$ python3 base.py -h

usage: base.py [-h] [--build-only] [--repository REPOSITORY] [--no-cache]
               base_image

A simple tool to build and publish base images to DockerHub. 

  Run `python3 base.py <base-image-name> <options>` to build and publish an image.

  Run `python3 base.py -h` to view available options

positional arguments:
  base_image            Name of the base image to build (same as the directory name)

optional arguments:
  -h, --help            show this help message and exit
  --build-only, -b      Only build the image. Do not publish after build is complete.
  --repository REPOSITORY, -r REPOSITORY
                        Push to a non-default repository. Use this option if you are an open source user and can't push to 
                        Gigantum Official repositories. Format: `namespace/repository`
  --no-cache            Boolean indicating if docker cache should be ignored

```

Remember, after the image is built and pushed you must create a new base spec yaml file. Be sure to increment the 
revision both in the filename and in the file itself. Commit and push changes to this repo to make the base available
to the client (if no yaml spec that points to the base is present, the image will not be usable).

To test, edit the Client config file to add `@branch-name` to the end of the repository URL.

Once a PR is accepted and merged to `master` the base becomes available to all users.

### Custom Base Images

If you wish to use different bases than the "official" Gigantum bases included here (master branch is default in the
Gigantum Client), you can create your own. We will not accept PRs targeting special use bases, but are open to 
improvements and generally useful contributions. For specific use bases, try the following workflow:

- Fork this repository
- Create a new base by copying and editing an existing one
- Create a new repository on DockerHub for your base
- Build and publish your base using `python3 base.py <base-name> --repository <your-namespace>/<repository-name>`
- Update the base spec yaml file with the tag provided after build and publish (should start at revision 0)
- Commit changes and push to your fork on GitHub
- Update the configuration file for your Gigantum Client instance to point to your fork instead of this repository
- Restart Gigantum
- Use your custom base!
