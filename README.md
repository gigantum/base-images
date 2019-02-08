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

usage: base.py [-h] [--build-only] [--namespace NAMESPACE] [--no-cache]
               [--generate-base-config-yaml]
               base_image

A simple tool to build and publish base images to DockerHub. 

  Run `python3 base.py <base-image-name> <options>` to build and publish an image.

  Run `python3 base.py -h` to view available options

positional arguments:
  base_image            Name of the base image to build (same as the directory name) or the string 'all' if you want to build all the images at once (this is useful when simply rebuilding bases for security updates)

optional arguments:
  -h, --help            show this help message and exit
  --build-only, -b      Only build the image. Do not publish after build is complete.
  --namespace NAMESPACE, -n NAMESPACE
                        Push to a non-default namespace. Use this option if you are an open source user and can't push to Gigantum Official repositories.
  --no-cache            Boolean indicating if docker cache should be ignored
  --generate-base-config-yaml, -g
                        Boolean indicating if base image configuration files should be auto-generated after publish operation succeeds


```

Remember, after the image is built and pushed you must create a new base spec yaml file. Be sure to increment the 
revision both in the filename and in the file itself. Commit and push changes to this repo to make the base available
to the client (if no yaml spec that points to the base is present, the image will not be usable).

To test, edit the Client config file to add `@branch-name` to the end of the repository URL.

Once a PR is accepted and merged to `master` the base becomes available to all users.

### Templating Support

Sometimes you want to reuse most of a Base dockerfile, and change just a few parameters. This can be done through 
template support and docker build args. An example of how this works can be seen with the `python3-minimal` base, 
which is built using different values for the `FROM` instruction.

To enable templating, instead of a Dockerfile in the base directory, create `dockerfile_template.json`. The base
Dockerfile should instead be written to `_template/<template_name>/Dockerfile`. Any arguments to be set at build-time 
should be set via `ARG` instructions in the Dockerfile with the values set in the associated `dockerfile_template.json`
file.

### Custom Base Images

If you wish to use different bases than the "official" Gigantum bases included here (master branch is default in the
Gigantum Client), you can create your own. We will not accept PRs targeting special use bases, but are open to 
improvements and generally useful contributions. For specific use bases, try the following workflow:

- Fork this repository
- Create a new base by copying and editing an existing base directory
- Create a new repository on DockerHub for your base
- Build and publish your base using `python3 base.py <base-name> --namespace <your-dockerhub-namespace>`
- Update the base spec yaml file with the tag provided after build and publish (should start at revision 0)
- Commit changes and push to your fork on GitHub
- Update the configuration file for your Gigantum Client instance to point to your fork instead of this repository
    - In your Gigantum working directory (`~/gigantum`) create a config file override. To do this, write the following to
    `~/gigantum/.labmanager/config.yaml`
    
    ```    
    environment:
      repo_url:
        - "https://github.com/<your-github-namespace>/base-images.git"    
    ```
     - If you create different branches, you can select the branch with the following syntax:

    ```    
    environment:
      repo_url:
        - "https://github.com/<your-github-namespace>/base-images.git@<branch-name>"    
    ```
- Restart Gigantum Client
- Use your custom base!
