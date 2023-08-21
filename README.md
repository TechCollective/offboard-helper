# Manage Google Workspace data

## Notes
This project is designed to bascily run GYB (Got Your Back) in batch mode. So you can que up a bunch of 
GYB jobs and have the run one after the other.

Just install and run the script. It will ask you a few questions, then run all the runs.

## TODO/ Roadmap
* Notifications - to email, a slack channel, or an Autotask Ticket
* add GAM support
  * create the group for the backup for you.
  * change the name of the user we are backing up and add an alias to whoever is suppose to get the new emails
* add RClown support - move the archive to a Google Shared Drive for you.

## Cement Notes
Below was created by the script builder I used called Cement. Below is it's default output for a README file. I have not veted any of the information below yet. I'll try to update it once I have something stable.

I have not tested Docker, it was created by cement.


## Installation

```
$ pip install -r requirements.txt

$ python setup.py install
```

## Development

This project includes a number of helpers in the `Makefile` to streamline common development tasks.

### Environment Setup

The following demonstrates setting up and working with a development environment:

```
### create a virtualenv for development

$ make virtualenv

$ source env/bin/activate


### run offboardhelper cli application

$ offboardhelper --help


### run pytest / coverage

$ make test
```


### Releasing to PyPi

Before releasing to PyPi, you must configure your login credentials:

**~/.pypirc**:

```
[pypi]
username = YOUR_USERNAME
password = YOUR_PASSWORD
```

Then use the included helper function via the `Makefile`:

```
$ make dist

$ make dist-upload
```

## Deployments

### Docker

Included is a basic `Dockerfile` for building and distributing `Offboard Helper`,
and can be built with the included `make` helper:

```
$ make docker

$ docker run -it offboardhelper --help
```
