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

### Custom / Novel Base Images

If you wish to use different bases than the "official" Gigantum bases included here or create a novel base for inclusion
in this repository (master branch is default in the Gigantum Client), you are in luck! We will generally not accept PRs
targeting special use bases, but are open to improvements and generally useful contributions. For specific use bases,
try the following workflow:

- Fork this repository
- Create a new base by copying and editing an existing base directory
  - Note that we have set XDG_CACHE_DIR to an unusual location, so that when a project runs, the cache directory is
    persistent on the host filesystem. You will likely want to delete the entire `GIGANTUM_WORKDIR` directory in any RUN
    statement that would keep files in the XDG cache (e.g., pip operations)
- Create a new repository on DockerHub for your base
- Build and publish your base using `python3 base.py <base-name> --namespace <your-dockerhub-namespace>`
- Update the base spec yaml file with the tag provided after build and publish (should start at revision 0)
- Commit changes and push to your fork on GitHub
- Update the configuration file for your Gigantum Client instance to point to your fork instead of this repository
    - In your Gigantum working directory (`~/gigantum`) create a config file override. To do this, write the following
      to `~/gigantum/.labmanager/config.yaml` (There is some extra information there because you currently have to
      specify the entire subtree for the `environment` key):

    ```
    environment:
      repo_url:
        - "https://github.com/<your-github-namespace>/base-images.git"
      iframe:
        enabled: false
        allowed_origin: localhost:10000
    ```
    - If you create different branches, you can select the branch with the following syntax:

    ```
    environment:
      repo_url:
        - "https://github.com/<your-github-namespace>/base-images.git@<branch-name>"
      iframe:
        enabled: false
        allowed_origin: localhost:10000
    ```
- Restart Gigantum Client
- Use your custom base!

### Notes on creating new versions of bases

- Use conda for everything you can - conda will not count pip-installed packages as fulfilling dependencies, and so may
  re-download and overwrite existing pip-installed packages!
- Special concerns for each IDE - generally, these will not need to change, but good to keep in mind:
  - *RStudio*: currently we override some security settings in the `rserver.conf` file. Additionally, there is a
    `user-settings` file that is copied into `/tmp` and later copied into the user's home directory at project launch.
    This is critical to set the working directory of the RStudio server to the project code directory. We also disable
    some annoying auto-save / auto-load features that are a holdover from the Bell Labs days.
  - *Jupyter*: There have been several tricky points of configuration. The first is ensuring that nbresuse is set up
    properly. This seems to have been resolved in recent versions of conda (everything is ok with a simple `conda
    install nbresuse`). Relatedly, we install a specific version of nodejs that is available as a Docker environment
    var. This ensures that re-installation of nodejs can easily pin to the same version so that jupyter labextensions
    don't need to be rebuilt for a different version. Lastly, Recent versions of Jupyterlab have enabled the extension
    configuration UI by default. This is inconsistent with how we manage the environment, so we disable it with
    `page_config.json` (a link to managing Jupyterlab settings is in the Dockerfile).
- Determining new package versions can be done in the relevant Python base. Do a `conda update --all` in the
  python3-minimal base to see what versions of nodejs, jupyter, and friends are available. Do the same in the data
  science base to determine upgraded versions for those additional packages.  R packages are installed by apt and so
  will be set to the latest versions by default. The latest version of RStudio can be found via the RStudio website.
- A somewhat tedious detail currently is that after the above step, you ALSO need to copy the yaml spec and update to
  new versions for packages. The package versions (including the Python version) should also be verified by launching a
  base image before publishing. These steps could both be automated and are described briefly in #46 (issue in this
  repo).
